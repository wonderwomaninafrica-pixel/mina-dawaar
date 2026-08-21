#!/usr/bin/env python3
"""Create sample reader pages for the two unpublished titles.

Same shell as the three published samples, minus everything that assumes a
retail listing: no Offer node, no Kindle button, and the breadcrumb stops at
the sample because these titles have no book page yet.
"""
from pathlib import Path

SITE = Path("/home/claude/repo")
BASE = "https://www.minadawaar.com"

BOOKS = [
    {
        "slug": "sample-good-mother.html",
        "title": "The Good Mother",
        "plain": "The Good Mother",
        "cover": "cover-good-mother.jpg",
        "w": 1023, "h": 1537,
    },
    {
        "slug": "sample-remembering-it-wrong.html",
        "title": "You&rsquo;re Remembering It Wrong",
        "plain": "You're Remembering It Wrong",
        "cover": "cover-remembering-it-wrong.jpg",
        "w": 1023, "h": 1537,
    },
    {
        "slug": "sample-perfect-patient.html",
        "title": "The Perfect Patient",
        "plain": "The Perfect Patient",
        "cover": "cover-perfect-patient.jpg",
        "w": 1023, "h": 1537,
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Read a Free Sample: {title} &mdash; Mina Dawaar</title>
<meta name="description" content="Read the opening two chapters of {plain} by Mina Dawaar, free. An early look at a forthcoming novel. No signup, no email.">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{base}/{slug}">
<link rel="icon" type="image/png" href="favicon.png">
<meta name="theme-color" content="#100E0B">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Mina Dawaar">
<meta property="og:title" content="Read a Free Sample: {title}">
<meta property="og:description" content="The opening two chapters of a forthcoming novel, free to read. No signup, no email.">
<meta property="og:url" content="{base}/{slug}">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="{base}/{cover}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Read a Free Sample: {title}">
<meta name="twitter:description" content="The opening two chapters of a forthcoming novel, free to read. No signup, no email.">
<meta name="twitter:image" content="{base}/{cover}">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "{plain}",
  "url": "{base}/{slug}",
  "image": "{base}/{cover}",
  "author": {{
    "@type": "Person",
    "@id": "{base}/#author",
    "name": "Mina Dawaar",
    "url": "{base}/"
  }},
  "genre": "Psychological Suspense",
  "inLanguage": "en",
  "bookFormat": "https://schema.org/EBook",
  "workExample": {{
    "@type": "Book",
    "@id": "{base}/{slug}",
    "name": "{plain}: Free Sample (Chapters One and Two)",
    "url": "{base}/{slug}",
    "isAccessibleForFree": true,
    "inLanguage": "en",
    "bookFormat": "https://schema.org/EBook"
  }}
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Books",
        "item": "{base}/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "{plain}",
        "item": "{base}/{slug}"
      }}
  ]
}}
</script>

<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="grain"></div>

<nav class="site-nav on-dark-top">
  <a href="index.html#collection" class="nav-mark nav-mark-big">MINA DAWAAR</a>
  <ul class="nav-links">
    <li><a href="index.html#collection">Home</a></li>
    <li><a href="index.html#collection">Books</a></li>
    <li><a href="index.html#about">About the Author</a></li>
    <li><a href="index.html#contact">Contact</a></li>
  </ul>
  <button class="nav-toggle" aria-label="Open menu"><span></span></button>
</nav>

<section class="reader">
  <div class="reader-head">
    <a href="index.html#collection" class="back-link">&larr; All Novels</a>
    <h1 class="book-title-visible">{title}</h1>
    <p class="book-hook">A free sample: Chapters One and Two. Coming soon.</p>
  </div>

  <div class="book" id="reader-book">
  <div class="book-page end-page" data-page="1">
    <p>The sample ends here. This novel has not been released yet.</p>
    <div class="book-actions">
      <a href="index.html#contact" class="btn solid">Join the List for Release News</a>
      <a href="index.html#collection" class="btn">All Novels</a>
    </div>
  </div>
  </div>

  <div class="reader-controls">
    <button class="pager" id="prev-page" aria-label="Previous page" disabled>&larr;</button>
    <span class="reader-progress"><span id="page-now">1</span><span class="sep">/</span><span id="page-total">1</span></span>
    <button class="pager" id="next-page" aria-label="Next page">&rarr;</button>
  </div>
  <p class="reader-hint">Use the arrows or your keyboard to turn the page</p>
</section>

<footer class="site-footer">
  <div class="footer-inner">
    <span>&copy; 2026 Mina Dawaar</span>
    <div class="footer-links">
      <a href="index.html#collection">All Novels</a>
      <a href="index.html#contact">Contact</a>
    </div>
  </div>
</footer>

<script src="script.js"></script>
</body>
</html>
"""

for b in BOOKS[:1]:
    (SITE / b["slug"]).write_text(
        TEMPLATE.format(base=BASE, **b), encoding="utf-8"
    )
    print("created", b["slug"])
