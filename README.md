# bakic.github.io

Abdelbaki's blog on Java, Spring Boot, AWS and software architecture, live at **https://bakic.github.io**.

It is a [Hugo](https://gohugo.io) site with a custom theme, hosted on GitHub Pages. Every push to `main` rebuilds and publishes it through GitHub Actions. The articles are plain markdown files in this repo.

## Add a new article

1. Create the post (the folder name becomes the URL, `/posts/<folder>/`):
   ```bash
   hugo new content posts/my-article-slug/index.md
   ```
2. Fill in the front-matter at the top of `index.md`:

   | Field | What it does |
   |---|---|
   | `title` | Page title and the headline in the teal band |
   | `date` | Publication date, shown on the article and used to sort the lists |
   | `description` | One sentence used for search engines and link previews |
   | `categories` | **One** of `Java`, `AWS`, `Spring Boot`, `Architecture`. Each category is a section on the home page, so a new one creates a new section. |
   | `tags` | Free-form, lowercase, e.g. `[aws, s3, security]`. They appear on the Tags page. |
   | `draft` | `true` keeps it out of the published site |

3. Put images in the same folder as `index.md` and reference them by file name: `![alt text](diagram.png)`. Use lowercase names without spaces.
4. Preview it, with drafts visible:
   ```bash
   hugo server -D     # http://localhost:1313, reloads as you save
   ```
5. Set `draft: false`, then publish:
   ```bash
   git add -A && git commit -m "Add <article title>" && git push
   ```
   The site is updated within one to two minutes. If it isn't, check the **Actions** tab of the repo for the failed step.

The table of contents on the left of each article is built from the `##` and `###` headings, and only appears on articles longer than about 600 words. Use `##` for sections and `###` for subsections. The title is already the page headline, so don't start the body with a `#` heading.

## Publishing on Medium as well

Publish on the blog first, then use Medium's **Import a story** with the blog URL. Medium sets the canonical link to the blog automatically, so search engines treat the blog as the original. For stories already on Medium, set it by hand: story, **⋯**, **More settings**, **Advanced settings**, **Customize canonical link**. Stories published under a publication (for example Stackademic) may not allow this.

## Project layout

```
content/posts/<slug>/index.md   one folder per article, with its images next to it
layouts/                        page templates (home, article, lists, tags, 404)
assets/css/main.css             all styling and the colour palette
assets/css/fonts.css            @font-face rules for the self-hosted fonts
assets/css/highlight.css        code syntax colours (light and dark)
static/fonts/                   Bricolage Grotesque, Source Serif 4, JetBrains Mono
static/js/post.js               the Copy button on code blocks
archetypes/default.md           the template used by `hugo new`
hugo.toml                       site title, taxonomies, markup settings
.github/workflows/hugo.yml      build and deploy to GitHub Pages
tools/                          one-off import scripts (see below)
```

## Design

- **Palette.** A mint-tinted page with a deep-teal band behind the header, the title and the footer, and one teal accent for links. The colours are variables at the top of `assets/css/main.css`, in a light set and a dark set that follows the visitor's system setting.
- **Type.** Bricolage Grotesque for headlines and interface text, Source Serif 4 for article body text, JetBrains Mono for code. The fonts are self-hosted, so visitors' browsers make no requests to Google.
- **Motion.** The home headline settles from condensed to normal width once on load. It is switched off for visitors who prefer reduced motion.

## Run it locally

```bash
brew install hugo          # needs the "extended" edition; the workflow pins 0.168.0
git clone https://github.com/bakic/bakic.github.io.git
cd bakic.github.io
hugo server -D
```

## Deployment

`.github/workflows/hugo.yml` installs Hugo, builds with `hugo --gc --minify` and publishes the result with GitHub Pages. It sets the site URL itself, so no `baseURL` edits are needed. The repository must be public, with **Settings, Pages, Source** set to **GitHub Actions**. To upgrade Hugo, change `HUGO_VERSION` in the workflow, and test the same version locally.

## Custom domain (optional)

Create `static/CNAME` containing the domain, point a DNS `CNAME` record for `www` (and the `A` records GitHub documents for the apex domain) at GitHub Pages, then enter the domain under **Settings, Pages**. Turn on **Enforce HTTPS** once the certificate is ready.

## The import scripts in `tools/`

These were used once, to build the first set of posts, and are not needed for day-to-day writing:

- `convert_articles.py` converted the original markdown drafts into posts, with generated front-matter and relocated images.
- `import_medium.py` converted stories from a Medium account export (the `posts/` folder of the zip) into posts and downloaded their images.

Both read from folders outside this repo, so they won't run elsewhere without editing the paths. Delete them if you don't want them.
