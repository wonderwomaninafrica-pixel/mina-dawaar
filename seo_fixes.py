#!/usr/bin/env python3
"""Technical fixes across the site: image dimensions, breadcrumb schema,
description lengths, social image sizing, LCP preloads, sitemap dates."""
import re
import glob
import struct
from pathlib import Path

SITE = Path("/home/claude/repo")
BASE = "https://www.minadawaar.com"
TODAY = "2026-08-08"


def dims(path):
    d = Path(SITE / path).read_bytes()
    if d[:2] == b"\xff\xd8":
        i = 2
        while i < len(d):
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3):
                h, w = struct.unpack(">HH", d[i + 5:i + 9])
                return w, h
            i += 2 if (m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7) else 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", d[16:24])
    raise ValueError(path)


BREADCRUMBS = {
    "pale-room.html": ("The Pale Room", None),
    "last-thing-she-remembered.html": ("The Last Thing She Remembered", None),
    "mind-of-an-obsessed-woman.html": ("The Mind of an Obsessed Woman", None),
    "sample-pale-room.html": ("The Pale Room", "pale-room.html"),
    "sample-last-thing-she-remembered.html": ("The Last Thing She Remembered", "last-thing-she-remembered.html"),
    "sample-mind-of-an-obsessed-woman.html": ("The Mind of an Obsessed Woman", "mind-of-an-obsessed-woman.html"),
}

# Sample pages: shorter descriptions that also stop leaking plot the grid no
# longer shows.
SAMPLE_COPY = {
    "sample-pale-room.html": "The Pale Room",
    "sample-last-thing-she-remembered.html": "The Last Thing She Remembered",
    "sample-mind-of-an-obsessed-woman.html": "The Mind of an Obsessed Woman",
}


def breadcrumb_json(title, parent, page):
    items = [f'''      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Books",
        "item": "{BASE}/"
      }}''']
    pos = 2
    if parent:
        items.append(f'''      {{
        "@type": "ListItem",
        "position": {pos},
        "name": "{title}",
        "item": "{BASE}/{parent}"
      }}''')
        pos += 1
        name = "Free Sample"
    else:
        name = title
    items.append(f'''      {{
        "@type": "ListItem",
        "position": {pos},
        "name": "{name}",
        "item": "{BASE}/{page}"
      }}''')
    return ('<script type="application/ld+json">\n'
            '{\n  "@context": "https://schema.org",\n'
            '  "@type": "BreadcrumbList",\n  "itemListElement": [\n'
            + ",\n".join(items) + "\n  ]\n}\n</script>\n")


for f in sorted(glob.glob(str(SITE / "*.html"))):
    p = Path(f)
    name = p.name
    s = p.read_text(encoding="utf-8")
    orig = s

    # --- intrinsic image dimensions, so covers reserve their space on load ---
    def add_dims(m):
        tag = m.group(0)
        if "width=" in tag:
            return tag
        src = re.search(r'src="([^"]+)"', tag).group(1)
        w, h = dims(src)
        return tag[:-1].rstrip() + f' width="{w}" height="{h}">'

    s = re.sub(r"<img[^>]*>", add_dims, s)

    # --- social image dimensions where missing ---
    if "og:image:width" not in s:
        img = re.search(r'<meta property="og:image" content="[^"]*/([^"/]+)">', s)
        if img:
            w, h = dims(img.group(1))
            s = s.replace(
                img.group(0),
                img.group(0) + f'\n<meta property="og:image:width" content="{w}">'
                f'\n<meta property="og:image:height" content="{h}">',
            )

    # --- shorter, plot-free sample descriptions ---
    if name in SAMPLE_COPY:
        t = SAMPLE_COPY[name]
        desc = f"Read the opening two chapters of {t} by Mina Dawaar, free. No signup, no email, start reading in the browser."
        short = f"The opening two chapters of {t}, free to read. No signup, no email."
        s = re.sub(r'(<meta name="description" content=")[^"]*(">)', rf"\1{desc}\2", s)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', rf"\1{short}\2", s)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*(">)', rf"\1{short}\2", s)

    # --- breadcrumbs ---
    if name in BREADCRUMBS and "BreadcrumbList" not in s:
        title, parent = BREADCRUMBS[name]
        s = s.replace('<link rel="stylesheet" href="style.css">',
                      breadcrumb_json(title, parent, name)
                      + '\n<link rel="stylesheet" href="style.css">')

    # --- preload the above-the-fold hero so it stops being a late LCP ---
    if name == "index.html" and "rel=\"preload\"" not in s:
        s = s.replace('<link rel="stylesheet" href="style.css">',
                      '<link rel="preload" as="image" href="hero-pale-room-texture.jpg">\n'
                      '<link rel="preload" as="image" href="cover-pale-room.jpg">\n'
                      '<link rel="stylesheet" href="style.css">')

    if s != orig:
        p.write_text(s, encoding="utf-8")
        print("updated", name)

# --- sitemap dates ---
sm = SITE / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
sm.write_text(re.sub(r"<lastmod>[\d-]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", t), encoding="utf-8")
print("updated sitemap.xml")
