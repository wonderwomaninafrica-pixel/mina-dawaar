#!/usr/bin/env python3
"""Rebuild the crawlable sample readers from the current epub builds.

Takes the first two chapters of each book, splits them into reader pages, and
splices the result into the existing sample HTML so all tuned metadata,
navigation and footer markup survive untouched.
"""
import re
import html
from pathlib import Path

EPUB = Path("/home/claude/ep")
SITE = Path("/home/claude/repo")

BOOKS = [
    {
        "sample": "sample-pale-room.html",
        "src": EPUB / "THE_PALE_ROOM/EPUB/text",
        "chapters": ["ch003.xhtml", "ch004.xhtml"],
    },
    {
        "sample": "sample-last-thing-she-remembered.html",
        "src": EPUB / "The_Last_Thing_She_Remembered/EPUB/text",
        "chapters": ["ch001.xhtml", "ch002.xhtml"],
    },
    {
        "sample": "sample-mind-of-an-obsessed-woman.html",
        "src": EPUB / "The_Mind_of_an_Obsessed_Woman/EPUB/text",
        "chapters": ["ch003.xhtml", "ch004.xhtml"],
    },
]

WORDS = {1: "One", 2: "Two"}
PAGE_TARGET = 620   # break once a page passes this many characters of prose


def read_chapter(path):
    """Return (heading_number, [(css_class, inner_html), ...])."""
    raw = path.read_text(encoding="utf-8")
    body = raw.split("<body", 1)[1]
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    num = int(re.search(r"(\d+)", re.sub("<[^>]+>", "", h1.group(1))).group(1))

    paras = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.S):
        inner = " ".join(m.group(1).split())
        strong = re.fullmatch(r"<strong>(.*)</strong>", inner, re.S)
        if strong:
            paras.append(("msg", strong.group(1).strip()))
        else:
            paras.append((None, inner))
    return num, paras


def paginate(chapters):
    """Group paragraphs into pages; each chapter starts a fresh page."""
    pages = []
    for num, paras in chapters:
        current, size = [], 0
        current.append(("heading", WORDS[num]))
        for cls, text in paras:
            current.append((cls, text))
            size += len(re.sub("<[^>]+>", "", text))
            if size >= PAGE_TARGET:
                pages.append(current)
                current, size = [], 0
        if current:
            pages.append(current)
    return pages


def render(pages, end_block):
    out = ['  <div class="book" id="reader-book">']
    for i, page in enumerate(pages, 1):
        out.append(f'  <div class="book-page" data-page="{i}">')
        for cls, text in page:
            if cls == "heading":
                out.append(f'    <h2 class="chapter-heading">Chapter {text}</h2>')
            elif cls == "msg":
                out.append(f'    <p class="msg">{text}</p>')
            else:
                out.append(f"    <p>{text}</p>")
        out.append("  </div>")
    out.append(end_block.replace('data-page="__N__"', f'data-page="{len(pages) + 1}"'))
    out.append("  </div>")
    return "\n".join(out), len(pages) + 1


for book in BOOKS:
    target = SITE / book["sample"]
    doc = target.read_text(encoding="utf-8")

    chapters = [read_chapter(book["src"] / c) for c in book["chapters"]]
    assert [c[0] for c in chapters] == [1, 2], book["sample"]

    # keep the existing end page exactly as written, only renumber it
    end = re.search(
        r'  <div class="book-page end-page" data-page="\d+">.*?\n  </div>', doc, re.S
    ).group(0)
    end = re.sub(r'data-page="\d+"', 'data-page="__N__"', end, count=1)

    block, total = render(paginate(chapters), end)

    doc = re.sub(
        r'  <div class="book" id="reader-book">.*?\n  </div>\n\n  <div class="reader-controls">',
        block + '\n\n  <div class="reader-controls">',
        doc,
        flags=re.S,
    )
    doc = re.sub(
        r'(<span id="page-total">)\d+(</span>)', rf"\g<1>{total}\g<2>", doc
    )

    # Last Thing dropped from three chapters to two
    doc = doc.replace("Chapters One to Three", "Chapters One and Two")

    target.write_text(doc, encoding="utf-8")
    print(f"{book['sample']}: {total - 1} pages + end page")
