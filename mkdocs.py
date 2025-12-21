#!/usr/bin/env python3

import re
import shutil
import sys
import webbrowser
from pathlib import Path

import markdown

PACKAGE = "Django Vanilla Extract"
ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR / "docs"
HTML_DIR = ROOT_DIR / "html"
PAGE_TEXT = (DOCS_DIR / "template.html").read_text()
SUFFIX = ".html"

MAIN_HEADER = '<li class="main"><a href="#{{ anchor }}">{{ title }}</a></li>'
SUB_HEADER = '<li><a href="#{{ anchor }}">{{ title }}</a></li>'
CODE_LABEL = (
    r'<a class="github" href="https://github.com/dakrauth/django-vanilla-extract'
    + r'/tree/master/vanilla_extract/\1"><span class="label label-info">\1</span></a>'
)


def replace(text, *pairs):
    for a, b in pairs:
        text = text.replace(a, b)

    return text


def convert_text(filename, text, prev_url, next_url):
    toc = ""
    description = "Django, CBV, GCBV, Generic class based views"
    for line in text.splitlines():
        main_title = None
        if line.startswith("# "):
            title = line[2:].strip()
            template = MAIN_HEADER
            description = description + ", " + title
        elif line.startswith("## "):
            title = line[3:].strip()
            template = SUB_HEADER
        else:
            continue

        main_title = title or main_title
        anchor = replace(
            title.lower(),
            (" ", "-"),
            (":-", "-"),
            ("'", ""),
            ("?", ""),
            (".", ""),
        )
        template = template.replace("{{ title }}", title)
        template = template.replace("{{ anchor }}", anchor)
        toc += f"{template}\n"

    subtitle = (
        "Beautifully simple class based views" if filename == "index.md" else main_title
    )
    main_title = f"{PACKAGE} - {subtitle}"
    content = markdown.markdown(text, extensions=["toc"])
    output = replace(
        PAGE_TEXT,
        ("{{ content }}", content),
        ("{{ toc }}", toc),
        ("{{ base_url }}", f"file://{HTML_DIR}/"),
        ("{{ suffix }}", SUFFIX),
        ("{{ index }}", "index.html"),
        ("{{ title }}", main_title),
        ("{{ description }}", description),
        ("{{ page_id }}", filename[:-3]),
    )
    if prev_url:
        output = replace(
            output, ("{{ prev_url }}", prev_url), ("{{ prev_url_disabled }}", "")
        )
    else:
        output = replace(
            output, ("{{ prev_url }}", "#"), ("{{ prev_url_disabled }}", "disabled")
        )

    if next_url:
        output = output.replace("{{ next_url }}", next_url)
        output = output.replace("{{ next_url_disabled }}", "")
    else:
        output = output.replace("{{ next_url }}", "#")
        output = output.replace("{{ next_url_disabled }}", "disabled")

    output = re.sub(r'a href="([^"]*)\.md"', r'a href="\1%s"' % SUFFIX, output)
    output = re.sub(
        r"<pre><code>:::bash",
        r'<pre class="prettyprint lang-bsh">',
        output,
    )
    output = re.sub(r"<pre>", r'<pre class="prettyprint lang-py">', output)
    return re.sub(r'<a class="github" href="([^"]*)"></a>', CODE_LABEL, output)


def build_relative_urls(path_list):
    prev_map = {}
    next_map = {}
    for idx, path in enumerate(path_list):
        rel = "../" * path.count("/")
        if idx > 0:
            prev_map[path] = rel + path_list[idx - 1][:-3] + SUFFIX

        if idx < len(path_list) - 1:
            next_map[path] = rel + path_list[idx + 1][:-3] + SUFFIX

    return prev_map, next_map


def mkdocs():
    # Hacky, but what the hell, it'll do the job
    prev_map, next_map = build_relative_urls(
        [
            "index.md",
            "api/base-views.md",
            "api/model-views.md",
            "migration/base-views.md",
            "migration/model-views.md",
            "topics/frequently-asked-questions.md",
            "topics/django-braces-compatibility.md",
            "topics/django-extra-views-compatibility.md",
            "topics/release-notes.md",
        ]
    )

    for dirpath, _dirnames, filenames in DOCS_DIR.walk():
        relative_dir = dirpath.relative_to(DOCS_DIR)
        build_dir = HTML_DIR / relative_dir
        build_dir.mkdir(exist_ok=True)

        for filename in filenames:
            path = dirpath / filename
            if not filename.endswith(".md"):
                if relative_dir:
                    shutil.copy(path, build_dir / filename)
                continue

            relative_url = str(relative_dir / filename)
            output = convert_text(
                filename,
                Path(path).read_text(),
                prev_map.get(relative_url),
                next_map.get(relative_url),
            )
            Path(build_dir / f"{filename[:-3]}.html").write_text(output)


def main():
    mkdocs()
    if "-p" in sys.argv:
        webbrowser.open_new_tab(f"file://{HTML_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
