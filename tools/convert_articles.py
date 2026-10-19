"""One-off converter: published/*.md -> content/posts/<slug>/index.md (Hugo page bundles).

Adds front-matter, drops the leading H1 (the theme renders the title), copies images
next to each post with lowercase names, and rewrites image links to relative paths.
Source files are only read, never modified.
"""
import datetime
import os
import re
import shutil
import unicodedata
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "published"
OUT = Path(__file__).resolve().parents[1] / "content" / "posts"

# source file (relative to published/) -> (tags, extra image dirs to search)
ARTICLES = {
    "A Closer Look at Annotations in Java.md": ["java", "annotations"],
    "A Deep Dive into flatMap() operation of the Stream API in  Java with examples.md": ["java", "streams"],
    "High availability VS Fault Tolerance VS Disaster Recovery.md": ["aws", "architecture", "resilience"],
    "Sealed Classes in Java.md": ["java", "sealed-classes"],
    "The Evolution of the Switch Statement in Java From Basic to Pattern Matching.md": ["java", "pattern-matching"],
    "The most used stream operations in Java with Examples.md": ["java", "streams"],
    "async logging.md": ["java", "logging", "performance"],
    "spring boot profiles best practices.md": ["spring-boot", "java", "configuration"],
    "sns-sms/sns sms.md": ["aws", "sns", "messaging"],
    "../presigned urls/Title Leveraging Pre-Signed URLs in Amazon S3 Secure File Upload and Download.md": ["aws", "s3", "security"],
    "../openapi/openapi-documentation.md": ["spring-boot", "openapi", "rest-api"],
}

IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r'<img\s+[^>]*?src="([^"]+)"[^>]*?(?:alt="([^"]*)")?[^>]*?/?>')

CATEGORY = {
    "High availability VS Fault Tolerance VS Disaster Recovery.md": "Architecture",
    "sns-sms/sns sms.md": "AWS",
    "spring boot profiles best practices.md": "Spring Boot",
    "../presigned urls/Title Leveraging Pre-Signed URLs in Amazon S3 Secure File Upload and Download.md": "AWS",
    "../openapi/openapi-documentation.md": "Spring Boot",
}  # everything else is "Java"

TITLES = {
    "spring boot profiles best practices.md": "Spring Boot Profiles Best Practices",
    "sns-sms/sns sms.md": "How to Send SMS messages using AWS SNS and Java: A Step-by-Step Guide",
    # match the titles used on Medium
    "The Evolution of the Switch Statement in Java From Basic to Pattern Matching.md": "Switch Statement in Java: From Basic to Pattern Matching",
    "async logging.md": "Optimizing Java Application Performance with Asynchronous Logging in Logback",
    "A Deep Dive into flatMap() operation of the Stream API in  Java with examples.md": "A Deep Dive into the flatMap Operation of the Stream API in Java with Examples",
}

# real publication dates from Medium (otherwise the file modification time is used)
DATES = {
    "High availability VS Fault Tolerance VS Disaster Recovery.md": "2023-03-20",
    "sns-sms/sns sms.md": "2023-08-02",
    "spring boot profiles best practices.md": "2023-08-05",
    "A Closer Look at Annotations in Java.md": "2023-11-06",
    "A Deep Dive into flatMap() operation of the Stream API in  Java with examples.md": "2023-08-10",
    "Sealed Classes in Java.md": "2023-08-07",
    "The Evolution of the Switch Statement in Java From Basic to Pattern Matching.md": "2023-08-29",
    "The most used stream operations in Java with Examples.md": "2023-08-12",
    "async logging.md": "2023-11-19",
    "../presigned urls/Title Leveraging Pre-Signed URLs in Amazon S3 Secure File Upload and Download.md": "2023-10-09",
    "../openapi/openapi-documentation.md": "2024-05-12",
}

SLUGS = {
    "A Deep Dive into flatMap() operation of the Stream API in  Java with examples.md": "flatmap-stream-api-java",
    "The Evolution of the Switch Statement in Java From Basic to Pattern Matching.md": "switch-statement-in-java-pattern-matching",
    "../presigned urls/Title Leveraging Pre-Signed URLs in Amazon S3 Secure File Upload and Download.md": "presigned-urls-aws-s3",
    "../openapi/openapi-documentation.md": "openapi-documentation-spring-rest-api",
    "async logging.md": "asynchronous-logging-logback",
    "sns-sms/sns sms.md": "send-sms-with-aws-sns",
}


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:70].rstrip("-")


def first_paragraph(body):
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if block and not block.startswith(("#", "!", "```", "|", "-", "*")):
            text = re.sub(r"[`*_\[\]]", "", block).replace("\n", " ")
            return (text[:152].rsplit(" ", 1)[0] + "...") if len(text) > 155 else text
    return ""


def find_image(name, src_dir):
    base = name.replace("\\", "/").split("/")[-1]
    for d in (src_dir, SRC, SRC.parent):
        p = d / base
        if p.exists():
            return p
    return None


def convert(rel, tags):
    src = SRC / rel
    raw = src.read_text(encoding="utf-8")
    lines = raw.splitlines()
    title = None
    for i, line in enumerate(lines):
        m = re.match(r"^#{1,2}\s+(.*\S)\s*$", line)
        if m:
            title = m.group(1).replace("*", "").strip()
            del lines[i]
            break
    if not title:
        title = src.stem
    body = "\n".join(lines).strip() + "\n"

    title = TITLES.get(rel, title)
    slug = SLUGS.get(rel) or slugify(title)
    bundle = OUT / slug
    bundle.mkdir(parents=True, exist_ok=True)

    def fix_image(m):
        alt, target = m.group(1), m.group(2).strip()
        found = find_image(target, src.parent)
        if not found:
            print(f"  ! missing image {target} in {rel}")
            return m.group(0)
        new_name = found.name.lower().replace(" ", "-")
        shutil.copyfile(found, bundle / new_name)
        return f"![{alt or new_name.rsplit('.', 1)[0]}]({new_name})"

    body = HTML_IMG_RE.sub(lambda m: f"![{m.group(2) or ''}]({m.group(1)})", body)
    body = IMG_RE.sub(fix_image, body)
    date = DATES.get(rel) or datetime.datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d")
    safe_title = title.replace('"', '\\"')
    desc = first_paragraph(body).replace('"', '\\"')
    front = (
        "---\n"
        f'title: "{safe_title}"\n'
        f"date: {date}\n"
        f'description: "{desc}"\n'
        f"categories: [{CATEGORY.get(rel, 'Java')}]\n"
        f"tags: [{', '.join(tags)}]\n"
        "draft: false\n"
        "---\n\n"
    )
    (bundle / "index.md").write_text(front + body, encoding="utf-8")
    print(f"{rel} -> posts/{slug}/ ({date})")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for rel, tags in ARTICLES.items():
        convert(rel, tags)
