#!/usr/bin/env python3
"""Check rendered HTML links, fragments, and referenced local assets offline."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import quote, unquote, urljoin, urlsplit


SITE_HOSTS = {"www.shalenetwork.org", "shalenetwork.org", "shalenetwork.github.io"}
SITE_URL = "https://www.shalenetwork.org/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.base = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "base":
            if self.base is None:
                self.base = attrs.get("href")
            return
        for attr in ("href", "src", "poster", "xlink:href"):
            if attrs.get(attr):
                self.links.append((attrs[attr], self.getpos()[0]))
        if tag == "object" and attrs.get("data"):
            self.links.append((attrs["data"], self.getpos()[0]))

    handle_startendtag = handle_starttag


def check_site(root):
    root = root.resolve()
    if not (root / "index.html").is_file():
        return [f"{root}: missing index.html; run quarto render first."], 0

    pages = {path.resolve(): Page(path) for path in sorted(root.rglob("*.html"))}
    errors = set()
    for source, page in pages.items():
        relative = source.relative_to(root).as_posix()
        source_url = urljoin(SITE_URL, quote(relative))
        base_url = urljoin(source_url, page.base) if page.base else source_url
        for link, line in page.links:
            url = urlsplit(urljoin(base_url, link.strip()))
            if url.scheme not in ("http", "https") or url.hostname not in SITE_HOSTS:
                continue
            target = (root / unquote(url.path).lstrip("/")).resolve()
            if not target.is_relative_to(root):
                errors.add(f"{relative}:{line}: path escapes site directory: {link}")
                continue
            if target.is_dir():
                target /= "index.html"
            elif not target.exists() and not target.suffix:
                target = target.with_suffix(".html")
            if not target.is_file():
                errors.add(f"{relative}:{line}: missing target: {link}")
                continue
            fragment = unquote(url.fragment)
            # Browsers resolve text fragments independently of element IDs.
            fragment = fragment.split(":~:text=", 1)[0]
            if fragment and target in pages and fragment not in pages[target].ids:
                errors.add(f"{relative}:{line}: missing fragment: {link}")
    return sorted(errors), len(pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", type=Path, default=Path("_site"))
    args = parser.parse_args()
    errors, count = check_site(args.site)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAILED: {len(errors)} broken internal references.", file=sys.stderr)
        return 1
    print(f"PASS: internal links, HTML fragments, and referenced assets in {count} HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
