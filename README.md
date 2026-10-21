# Shale Network website

Source for [shalenetwork.org](https://shalenetwork.org), built with Quarto and published through GitHub Pages.

## Local editing and preview

Install [Quarto 1.5.49](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.5.49) and Python 3.9 or later. The site checker uses only Python's standard library. Run commands from this repository's root.

```sh
quarto preview --host 127.0.0.1 --port 4200 --no-browser
```

Open <http://127.0.0.1:4200>. Quarto watches source files and updates the local preview; press Ctrl+C to stop it. Review desktop and mobile layouts before publishing.

Page content is in `.qmd` files. Site navigation and build settings are in `_quarto.yml`; shared styles and images are under `assets/`. Keep historical news dated and distinguish completed work from proposed activities. Update the statistics date only when the displayed totals have been reconfirmed.

## Content and image sources

The homepage describes national expansion as ongoing. Its Pennsylvania map illustrates one published study, not the database’s full geographic coverage. Keep this distinction when updating the page.

Xiumei Ma and Mahnaz Sepehrmanesh’s portraits come from the [Wen Group people page](https://jaywen.com/people.html). The education page uses an existing TeenShale Network field photograph with a dated link to its archive entry. Keep image descriptions and source context when replacing visuals.

## Check before publication

```sh
quarto render
python3 scripts/check_site.py _site
```

The checker reads rendered HTML and checks local `href`, `src`, `poster`, SVG references, object files, and HTML fragment IDs. Absolute links using either Shale Network domain or its GitHub Pages hostname are treated as internal. It makes no network requests. External destinations, form submissions, JavaScript-generated links, CSS image references, and scientific claims still require review.

Do not commit `_site/`, `.quarto/`, private proposal material, review evidence, or credentials. Review the source diff before committing. Render output is generated during publication.

## Automatic publication

[Quarto Publish](.github/workflows/publish.yml) uses Quarto 1.5.49 to render and check pull requests and pushes to `main`. A failed render or internal-link check stops publication. Pull requests are checked without publishing.

A successful **push to `main`** publishes the checked output to `gh-pages`. A manual workflow run publishes only when `main` is selected. GitHub Pages then deploys `gh-pages` at the custom domain in `CNAME`. Workflows for the same branch run sequentially to avoid overlapping publications; a newer queued run may replace an older queued run.

Local edits, previews, commits, and pulls do not publish the site. A GitHub sync publishes only if it pushes a change to `main`. After an approved push, check both the Quarto Publish workflow and GitHub's Pages deployment, then verify the live page.

For publication troubleshooting, see the [Quarto GitHub Pages guide](https://quarto.org/docs/publishing/github-pages.html). Keep GitHub Pages configured to serve `gh-pages` from the branch root, and retain `CNAME` in the rendered site. Do not change repository settings or run `quarto publish` while preparing a local-only review.
