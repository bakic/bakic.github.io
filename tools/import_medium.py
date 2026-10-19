"""Import stories from a Medium export (posts/*.html) into Hugo page bundles.

Usage: python3 -I tools/import_medium.py <path to extracted posts/ dir>

The export is only read, never modified. Images are downloaded from Medium's public
image CDN into each post's folder. Only the stories listed in IMPORTS are converted.
"""
import datetime
import html
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "content" / "posts"

# Medium story id (last part of the file name) -> (category, tags)
IMPORTS = {
    "52613488d5a2": ("AWS", ["aws", "ses", "spring-boot", "security"]),
    "220063b54ce0": ("Spring Boot", ["spring-boot", "java", "configuration"]),
    "3e6e47fdb6fb": ("Java", ["java", "records"]),
    "9c39221fdd6a": ("Architecture", ["architecture", "networking"]),
    "6a01a18235f5": ("Spring Boot", ["spring", "dependency-injection", "java"]),
    "48c980ea4173": ("Java", ["java", "streams"]),
    "561c5ca6590f": ("AWS", ["aws", "s3"]),
    "f3ca6a2ef990": ("AWS", ["aws", "s3"]),
    "8d2ba4e4ef19": ("AWS", ["aws", "s3"]),
}

SLUGS = {
    "52613488d5a2": "smtp-to-aws-ses-iam-roles-spring-boot",
    "220063b54ce0": "conditionalonproperty-custom-beans-spring-boot",
    "6a01a18235f5": "dependency-injection-ways-in-spring",
    "8d2ba4e4ef19": "aws-s3-storage-classes-comparison",
    "f3ca6a2ef990": "object-versioning-in-s3",
}

TITLES = {  # fix typos in the Medium titles
    "f3ca6a2ef990": "Object Versioning in S3",
}

VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []

    @property
    def cls(self):
        return self.attrs.get("class", "")


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def find_all(node, pred):
    for c in node.children:
        if isinstance(c, Node):
            if pred(c):
                yield c
            yield from find_all(c, pred)


def text_of(node):
    if isinstance(node, str):
        return node
    if node.tag == "br":
        return "\n"
    return "".join(text_of(c) for c in node.children)


def inline(node, in_code=False):
    parts = []
    for c in node.children:
        if isinstance(c, str):
            t = c.replace("\n", " ")
            parts.append(t if in_code else t.replace("*", "\\*").replace("<", "&lt;"))
            continue
        tag = c.tag
        if tag == "br":
            parts.append("  \n")
        elif tag in ("strong", "b"):
            inner = inline(c).strip()
            parts.append(f"**{inner}**" if inner else "")
        elif tag in ("em", "i"):
            inner = inline(c).strip()
            parts.append(f"*{inner}*" if inner else "")
        elif tag == "code":
            inner = text_of(c).replace("\n", " ")
            parts.append(f"`{inner}`" if inner else "")
        elif tag == "a":
            href = c.attrs.get("data-href") or c.attrs.get("href", "")
            inner = inline(c).strip()
            parts.append(f"[{inner}]({href})" if href and inner else inner)
        elif tag == "img":
            parts.append(f"![]({c.attrs.get('src', '')})")
        else:
            parts.append(inline(c, in_code))
    return "".join(parts)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:70].rstrip("-")


def download(url, dest_dir, n):
    """Download an image; returns the local file name or None."""
    candidates = [re.sub(r"/max/\d+/", "/max/1400/", url), url]
    for u in dict.fromkeys(candidates):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data, ctype = r.read(), r.headers.get_content_type()
        except Exception:
            continue
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp", "image/svg+xml": ".svg"}.get(ctype)
        if not ext or not data:
            continue
        name = f"image-{n}{ext}"
        (dest_dir / name).write_bytes(data)
        return name
    return None


def convert(path, category, tags, sid=None):
    raw = path.read_text(encoding="utf-8")
    date = path.name[:10]
    tree = Tree()
    tree.feed(raw)

    title = html.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1)).strip()
    body = next(find_all(tree.root, lambda n: n.tag == "section" and n.attrs.get("data-field") == "body"))
    inner = next(find_all(body, lambda n: "section-inner" in n.cls))

    # heading levels actually used in the body (excluding the repeated title) -> ## ### ####
    heads = [c for c in find_all(inner, lambda n: n.tag in ("h2", "h3", "h4", "h5") and "graf--title" not in n.cls and "graf--subtitle" not in n.cls)]
    levels = sorted({int(h.tag[1]) for h in heads})
    hmap = {lv: "#" * (i + 2) for i, lv in enumerate(levels)}

    title = TITLES.get(sid, title)
    slug = SLUGS.get(sid) or slugify(title)
    bundle = OUT / slug
    bundle.mkdir(parents=True, exist_ok=True)
    img_n = [0]
    lines = []

    def block(n):
        tag = n.tag
        if tag in ("h2", "h3", "h4", "h5"):
            if "graf--title" in n.cls or "graf--subtitle" in n.cls:
                return
            t = inline(n).strip()
            if t:
                lines.append(f"{hmap[int(tag[1])]} {t}\n")
        elif tag == "p":
            t = inline(n).strip()
            if t:
                lines.append(t + "\n")
        elif tag == "blockquote":
            t = inline(n).strip().replace("\n", "\n> ")
            lines.append("> " + t + "\n")
        elif tag == "pre":
            lang = n.attrs.get("data-code-block-lang", "")
            code = html.unescape(text_of(n)).strip("\n")
            lines.append(f"```{lang}\n{code}\n```\n")
        elif tag in ("ul", "ol"):
            items = [c for c in n.children if isinstance(c, Node) and c.tag == "li"]
            for i, li in enumerate(items, 1):
                mark = f"{i}." if tag == "ol" else "-"
                lines.append(f"{mark} {inline(li).strip()}")
            lines.append("")
        elif tag == "figure":
            img = next(find_all(n, lambda x: x.tag == "img"), None)
            cap = next(find_all(n, lambda x: x.tag == "figcaption"), None)
            if img is not None:
                img_n[0] += 1
                src = img.attrs.get("src", "")
                name = download(src, bundle, img_n[0])
                if not name:
                    print(f"  ! could not download {src}")
                alt = html.unescape(text_of(cap)).strip() if cap is not None else ""
                lines.append(f"![{alt}]({name or src})\n")
                if cap is not None and inline(cap).strip():
                    lines.append(f"*{inline(cap).strip()}*\n")
            elif next(find_all(n, lambda x: x.tag == "iframe"), None) is not None:
                ifr = next(find_all(n, lambda x: x.tag == "iframe"))
                print(f"  ! embed (gist/iframe) in {path.name}: {ifr.attrs.get('src')}")
                lines.append(f"<!-- TODO embedded content: {ifr.attrs.get('src')} -->\n")
        elif tag == "hr":
            if "section-divider" not in n.cls:
                lines.append("---\n")
        elif tag in ("div", "section"):
            for c in n.children:
                if isinstance(c, Node):
                    block(c)

    for c in inner.children:
        if isinstance(c, Node):
            block(c)

    md = "\n".join(lines).strip() + "\n"
    first = next((l for l in lines if l and not l.startswith(("#", "!", "`", "-", ">", "*"))), "")
    first = re.sub(r"[`*_\[\]]|\(http[^)]*\)", "", first).replace("\n", " ").replace('"', '\\"')
    desc = (first[:152].rsplit(" ", 1)[0] + "...") if len(first) > 155 else first
    front = (
        "---\n"
        f'title: "{title.replace(chr(34), chr(92) + chr(34))}"\n'
        f"date: {date}\n"
        f'description: "{desc}"\n'
        f"categories: [{category}]\n"
        f"tags: [{', '.join(tags)}]\n"
        "draft: false\n"
        "---\n\n"
    )
    (bundle / "index.md").write_text(front + md, encoding="utf-8")
    print(f"{path.name[:60]} -> posts/{slug}/ ({date}, {img_n[0]} images)")


if __name__ == "__main__":
    src = Path(sys.argv[1])
    for f in sorted(src.glob("*.html")):
        sid = f.stem.rsplit("-", 1)[-1]
        if sid in IMPORTS:
            convert(f, *IMPORTS[sid], sid=sid)
