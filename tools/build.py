#!/usr/bin/env python3
"""Build the Happy People Rentals website.

Reads the page sources in src/pages/, the rental catalog in src/catalog.json and the
image list in src/images.json, and writes plain HTML files at the same web addresses
the live site uses (for example src/pages/giant-games.html -> giant-games/index.html).
It also writes sitemap.xml and robots.txt.

Run it after changing anything in src/:

    python3 tools/build.py

Only the Python standard library is needed.
"""
import datetime
import html
import json
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

SITE = "https://happypeoplerentals.ca"
BUSINESS = {
    "name": "Happy People Rentals",
    "phone": "343-558-5631",
    "tel": "+13435585631",
    "email": "info@happypeoplerentals.ca",
    "slogan": "Making Every Event Memorable",
    "areas": ["Ottawa", "Gatineau", "Kanata", "Orléans", "Barrhaven", "Nepean"],
    "facebook": "https://www.facebook.com/profile.php?id=61590511022603",
    "instagram": "https://www.instagram.com/happypeoplerentals/",
    "google_review": "https://g.page/r/CV8HlLW7IVr-EAE/review",
    "privacy": "https://drive.google.com/file/d/1t7P5vtDuqWNS56U4j4KlAkQVvb1xTzxV/view?usp=sharing",
    "description": (
        "Happy People Rentals rents giant yard games, inflatable games, bouncy castles, "
        "photo booths, flower walls, flower bars, tables, chairs and canopies for events "
        "in Ottawa, Gatineau and surrounding areas."
    ),
}

RENTAL_LINKS = [
    ("All rentals", "/rental-catalog/"),
    ("Giant & yard games", "/giant-games/"),
    ("Inflatable games", "/inflatable-games/"),
    ("Bouncy castle", "/bouncy-castle/"),
    ("Photo booth & flower walls", "/photo-booth/"),
    ("Flower bar", "/flower-bar/"),
    ("Tables & chairs", "/tables-chairs-for-every-celebration/"),
]
NAV = [
    ("Home", "/", None),
    ("Rentals", "/rental-catalog/", RENTAL_LINKS),
    ("Packages", "/packages/", None),
    ("Gallery", "/gallery/", None),
    ("About", "/about/", None),
    ("Contact", "/contact-us/", None),
]

IMAGES = json.load(open(os.path.join(SRC, "images.json")))
CATALOG = json.load(open(os.path.join(SRC, "catalog.json")))
ITEMS = {i["id"]: i for i in CATALOG["items"]}
esc = html.escape


def fail(msg):
    sys.exit("build error: " + msg)


# ---------------------------------------------------------------- snippets

def img(key, sizes="(max-width: 700px) 100vw, 50vw", eager=False, cls=""):
    if key not in IMAGES:
        fail(f"unknown image '{key}'")
    m = IMAGES[key]
    src = "/images/" + m["file"]
    srcset = ""
    if m.get("small"):
        srcset = f' srcset="/images/{m["small"]} 500w, {src} {m["w"]}w" sizes="{sizes}"'
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="{src}"{srcset} alt="{esc(m["alt"])}" width="{m["w"]}" '
            f'height="{m["h"]}"{load} decoding="async"{c}>')


def quote_link(name):
    return "/get-a-quote/?game=" + urllib.parse.quote_plus(name)


def price_text(item):
    return f"${item['price']}" if item.get("price") is not None else "Ask"


def card(item, heading="h3", delay=0):
    price_label = "per rental" if item.get("price") is not None else "for a price"
    return f"""<article class="game" id="{item['id']}" data-reveal style="--delay:{delay}ms">
  <div class="game__photo game__photo--product">{img(item['img'], sizes='(max-width: 620px) 100vw, 300px')}</div>
  <div class="game__body">
    <{heading} class="display d-3">{esc(item['name'])}</{heading}>
    <p>{esc(item['desc'])}</p>
    <span class="game__meta">{esc(item.get('meta', ''))}</span>
  </div>
  <div class="specs">
    <span><b>{price_text(item)}</b> {price_label}</span>
    <a href="{quote_link(item['name'])}">Add to quote</a>
  </div>
</article>"""


def cards(spec):
    """{{cards:group:giant}} or {{cards:ids:connect4,jenga}}"""
    kind, _, val = spec.partition(":")
    if kind == "group":
        items = [i for i in CATALOG["items"] if i["group"] == val]
    else:
        items = [ITEMS[x] for x in val.split(",")]
    if not items:
        fail(f"no items for cards:{spec}")
    return '<div class="games">\n' + "\n".join(card(i, delay=(n % 4) * 60) for n, i in enumerate(items)) + "\n</div>"


def logos():
    keys = [k for k, v in IMAGES.items() if v["kind"] == "clientlogo"]
    cells = "\n".join(
        f'<li>{img(k, sizes="160px")}</li>' for k in keys)
    return f'<ul class="logos" role="list">\n{cells}\n</ul>'


def chips():
    names = [i["name"] for i in CATALOG["items"]] + CATALOG["extra_quote_options"]
    out = []
    for n in names:
        out.append(f'<label class="chip"><input type="checkbox" name="games[]" value="{esc(n)}"> {esc(n)}</label>')
    return '<div class="chips">\n' + "\n".join(out) + "\n</div>"


BOARD = [
    ". . . . . . .",
    ". . . . . . .",
    ". . . r9 . . .",
    ". . y6 r7 . . .",
    ". y3 r4 y5 . . .",
    "y0 r1 y2 r8 y10 . .",
]


def board():
    cells = []
    for row in BOARD:
        for c in row.split():
            if c == ".":
                cells.append("<i></i>")
            else:
                cells.append(f'<i class="{c[0]}" style="--d:{int(c[1:]) * 140}ms"></i>')
    return '<div class="board" data-board aria-hidden="true">' + "".join(cells) + "</div>"


MARQUEE_ITEMS = ["Giant Connect 4", "Giant Jenga", "Cornhole", "Ladder Toss", "Giant Tetris", "Inflatable Games",
                 "Bouncy Castle", "Photo Booth", "Flower Bar", "Table Tennis", "Foosball", "Arcade Basketball",
                 "Popcorn Machines", "Tables & Chairs", "Canopies"]
OCCASIONS = [("occ_birthday", "Birthdays"), ("occ_wedding", "Weddings"), ("occ_corporate", "Corporate events"),
             ("c_cornhole", "Team building"), ("occ_school", "School events"), ("occ_festival", "Festivals & carnivals"),
             ("g_connect4", "Family days"), ("occ_community", "Community days")]
EVENT_TAGS = ["Birthday parties", "Weddings", "Engagement parties", "Baby showers", "Graduations", "Corporate picnics",
              "Team building days", "Client appreciation", "Staff appreciation", "Conferences", "Trade shows",
              "School fun fairs", "Field days", "Prom & grad nights", "University orientation", "Church events",
              "Community BBQs", "Block parties", "Neighbourhood days", "Canada Day events", "Festivals", "Carnivals",
              "Fundraisers", "Charity galas", "Sports tournaments", "Camps & day camps", "Family reunions",
              "Retirement parties", "Housewarmings", "Backyard parties", "Holiday parties", "Movie nights"]


def marquee(arg):
    """{{marquee}} or {{marquee:brown}}; the text is repeated so the loop is seamless."""
    text = " ✦ ".join(MARQUEE_ITEMS) + " ✦ "
    cls = "marquee marquee--brown" if arg == "brown" else "marquee"
    return (f'<div class="{cls}" aria-hidden="true"><div class="marquee__track">'
            f'<span>{esc(text)}</span><span>{esc(text)}</span></div></div>')


def slider(arg):
    """{{slider:occasions}}: a row of captioned photos that slides sideways. Duplicated for the loop."""
    figs = "".join(f'<figure class="slide">{img(k, sizes="360px")}<figcaption>{esc(n)}</figcaption></figure>'
                   for k, n in OCCASIONS)
    copy = figs.replace("<figure", '<figure aria-hidden="true"')  # second copy makes the loop seamless
    return (f'<div class="slider" role="region" aria-label="Event photos" tabindex="0">'
            f'<div class="slider__track">{figs}{copy}</div></div>')


def stats(_):
    n_items = len(CATALOG["items"]) + len(CATALOG["extra_quote_options"])
    rows = [(f"{len(EVENT_TAGS)}+", "Types of events covered"), (f"{n_items}+", "Games and rentals available"),
            ("$50", "Most giant games, per rental"), ("Free", "Quote with no obligation")]
    return '<div class="stats">' + "".join(f'<div class="stat" data-reveal style="--delay:{i*60}ms"><b>{esc(v)}</b><span>{esc(l)}</span></div>'
                                           for i, (v, l) in enumerate(rows)) + "</div>"


def tags(_):
    return '<div class="tags">' + "".join(f"<span>{esc(t)}</span>" for t in EVENT_TAGS) + "</div>"


SNIPPETS = {
    "marquee": marquee,
    "slider": slider,
    "stats": stats,
    "tags": tags,
    "count": lambda _: str(len(CATALOG["items"]) + len(CATALOG["extra_quote_options"])),
    "phone": lambda _: BUSINESS["phone"],
    "tel": lambda _: BUSINESS["tel"],
    "email": lambda _: BUSINESS["email"],
    "review": lambda _: BUSINESS["google_review"],
    "img": lambda a: img(*a.split("|")[:1], eager="eager" in a.split("|")[1:]),
    "cards": cards,
    "logos": lambda _: logos(),
    "chips": lambda _: chips(),
    "board": lambda _: board(),
    "price": lambda a: price_text(ITEMS[a]),
}


def expand(body):
    def sub(m):
        name, _, arg = m.group(1).partition(":")
        if name not in SNIPPETS:
            fail(f"unknown snippet {{{{{m.group(1)}}}}}")
        return SNIPPETS[name](arg)
    return re.sub(r"\{\{\s*([^}]+?)\s*\}\}", sub, body)


# ---------------------------------------------------------------- layout

# The logo is kept exactly as it appears on the current design.
LOGO_HEADER = """<a href="/" style="display:flex; align-items:center; gap:12px; text-decoration:none;" aria-label="Happy People Rentals home">
        <span style="width:34px; height:34px; border-radius:50%; background:#F7B916; display:flex; align-items:center; justify-content:center; font-size:19px; line-height:1; color:#3F3413;" aria-hidden="true">☺</span>
        <span style="display:flex; flex-direction:column; line-height:0.9; font-family:Anton, sans-serif; text-transform:uppercase; color:#FFF8EC;">
          <span style="font-size:clamp(15px,2.2vw,19px);">Happy People</span>
          <span style="font-size:clamp(9px,1.2vw,11px); letter-spacing:0.4em; color:#F7B916;">Rentals</span>
        </span>
      </a>"""

LOGO_FOOTER = """<div style="display:flex; align-items:center; gap:12px;">
        <span style="width:38px; height:38px; border-radius:50%; background:#F7B916; display:flex; align-items:center; justify-content:center; font-size:21px; color:#3F3413;" aria-hidden="true">☺</span>
        <span style="display:flex; flex-direction:column; line-height:0.9; font-family:Anton, sans-serif; text-transform:uppercase; color:#FFF8EC;">
          <span style="font-size:19px;">Happy People</span>
          <span style="font-size:10px; letter-spacing:0.4em; color:#F7B916;">Rentals</span>
        </span>
      </div>"""


def header(path, overlay):
    items = []
    for label, href, sub in NAV:
        current = ' aria-current="page"' if href == path else ""
        if sub:
            active = " is-current" if path in [h for _, h in sub] else ""
            mark = ' aria-current="page"'
            links = "".join(
                f'<li><a href="{h}"{mark if h == path else ""}>{esc(l)}</a></li>'
                for l, h in sub)
            items.append(
                f'<li class="has-sub{active}"><a href="{href}"{current}>{esc(label)}</a>'
                f'<ul class="sub">{links}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{current}>{esc(label)}</a></li>')
    spacer = "" if overlay else '\n<div class="header-spacer"></div>'
    return f"""<header class="site-header" data-header>
  <div class="site-header__bar">
      {LOGO_HEADER}
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="nav-list">{''.join(items)}</ul>
      <a href="/get-a-quote/" class="btn btn--yellow">Get a quote</a>
    </nav>
    <button type="button" class="burger" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu" data-burger><span></span><span></span><span></span></button>
  </div>
</header>{spacer}
<div class="quick-bar">
  <a href="tel:{BUSINESS['tel']}" class="btn btn--ghost">Call {BUSINESS['phone']}</a>
  <a href="/get-a-quote/" class="btn btn--yellow">Get a quote</a>
</div>"""


def footer():
    rentals = "".join(f'<a href="{h}">{esc(l)}</a>' for l, h in RENTAL_LINKS)
    year = datetime.date.today().year
    return f"""<footer class="site-footer">
  <div class="site-footer__grid">
    <div class="site-footer__col" style="gap:16px; max-width:340px;">
      {LOGO_FOOTER}
      <p style="font-family:Georgia, serif; font-style:italic; font-size:20px; line-height:1.3; color:#F7B916;">{BUSINESS['slogan']}</p>
      <p>Giant yard games, inflatables, photo booths, tables, chairs and canopies for events in Ottawa, Gatineau and surrounding areas.</p>
    </div>
    <div class="site-footer__col">
      <h2 class="site-footer__h">Get in touch</h2>
      <a href="tel:{BUSINESS['tel']}">{BUSINESS['phone']}</a>
      <a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a>
      <a href="{BUSINESS['instagram']}" rel="noopener">Instagram @happypeoplerentals</a>
      <a href="{BUSINESS['facebook']}" rel="noopener">Facebook: HP Rentals</a>
      <a href="{BUSINESS['google_review']}" rel="noopener">Review us on Google</a>
    </div>
    <div class="site-footer__col">
      <h2 class="site-footer__h">Rentals</h2>
      {rentals}
    </div>
    <div class="site-footer__col">
      <h2 class="site-footer__h">Company</h2>
      <a href="/about/">About us</a>
      <a href="/gallery/">Gallery</a>
      <a href="/packages/">Packages</a>
      <a href="/contact-us/">Contact</a>
      <a href="/get-a-quote/">Get a free quote</a>
      <span style="color:rgba(255,248,236,0.6); line-height:1.55;">Serving {', '.join(BUSINESS['areas'][:-1])} and {BUSINESS['areas'][-1]}.</span>
    </div>
  </div>
  <div class="site-footer__base">
    <span>© {year} Happy People Rentals. All rights reserved.</span>
    <a href="{BUSINESS['privacy']}" rel="noopener">Privacy policy</a>
  </div>
</footer>"""


# ---------------------------------------------------------------- structured data

def abs_url(path):
    return SITE + path


def business_node():
    prices = [i["price"] for i in CATALOG["items"] if i.get("price") is not None]
    return {
        "@type": "LocalBusiness",
        "@id": SITE + "/#business",
        "name": BUSINESS["name"],
        "url": SITE + "/",
        "logo": {"@type": "ImageObject", "url": SITE + "/images/happy-people-rentals-logo.png"},
        "image": SITE + "/images/" + IMAGES["hero"]["file"],
        "description": BUSINESS["description"],
        "slogan": BUSINESS["slogan"],
        "telephone": "+1-343-558-5631",
        "email": BUSINESS["email"],
        "priceRange": f"${min(prices)}–${max(prices)}",
        "currenciesAccepted": "CAD",
        "address": {"@type": "PostalAddress", "addressLocality": "Ottawa",
                    "addressRegion": "ON", "addressCountry": "CA"},
        "areaServed": [{"@type": "City", "name": n} for n in BUSINESS["areas"]],
        "sameAs": [BUSINESS["facebook"], BUSINESS["instagram"]],
    }


def service_node(page, url):
    svc = page["service"]
    node = {
        "@type": "Service",
        "@id": url + "#service",
        "name": svc["name"],
        "serviceType": svc.get("type", svc["name"]),
        "url": url,
        "provider": {"@id": SITE + "/#business"},
        "areaServed": [{"@type": "City", "name": n} for n in BUSINESS["areas"]],
    }
    ids = []
    for spec in svc.get("items", []):
        if spec.startswith("group:"):
            ids += [i["id"] for i in CATALOG["items"] if i["group"] == spec[6:]]
        else:
            ids.append(spec)
    if ids:
        offers = []
        for i in ids:
            it = ITEMS[i]
            offer = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": it["name"],
                                                         "description": it["desc"]}}
            if it.get("price") is not None:
                offer.update({"price": str(it["price"]), "priceCurrency": "CAD"})
            offers.append(offer)
        node["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": svc["name"], "itemListElement": offers}
    return node


def faq_node(body, url):
    pairs = re.findall(
        r'<div class="faq-item">\s*<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>', body, re.S)
    if not pairs:
        return None
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {"@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": strip(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in pairs]}


def schema(page, url, body):
    graph = [business_node(), {
        "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
        "name": BUSINESS["name"], "inLanguage": "en-CA", "publisher": {"@id": SITE + "/#business"}}]
    webpage = {
        "@type": page.get("pagetype", "WebPage"), "@id": url + "#webpage", "url": url,
        "name": page["title"], "description": page["description"],
        "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"},
        "inLanguage": "en-CA",
        "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/images/" + IMAGES[page.get("image", "hero")]["file"]},
    }
    if page["path"] != "/":
        trail = [("Home", "/")] + [tuple(x) for x in page.get("trail", [])] + [(page["crumb"], page["path"])]
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "name": name, "item": abs_url(p)}
            for n, (name, p) in enumerate(trail)]})
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
    graph.append(webpage)
    if page.get("service"):
        graph.append(service_node(page, url))
    faq = faq_node(body, url)
    if faq:
        graph.append(faq)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return data.replace("</", "<\\/")


def breadcrumbs(page):
    if page["path"] == "/" or page.get("no_crumbs"):
        return ""
    trail = [("Home", "/")] + [tuple(x) for x in page.get("trail", [])]
    parts = "".join(f'<li><a href="{p}">{esc(n)}</a></li>' for n, p in trail)
    parts += f'<li aria-current="page">{esc(page["crumb"])}</li>'
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol class="wrap">{parts}</ol></nav>'


def render(page, body):
    path = page["path"]
    url = abs_url(path)
    overlay = page.get("overlay", False)
    og_meta = IMAGES[page.get("image", "hero")]
    og_file, og_w, og_h, og_type = og_meta["file"], og_meta["w"], og_meta["h"], "image/webp"
    og_jpg = "og/" + og_file.replace(".webp", ".jpg")
    if os.path.exists(os.path.join(ROOT, "images", og_jpg)):
        # JPG share image, shown by every social app
        og_file, og_w, og_h, og_type = og_jpg, 1200, 630, "image/jpeg"
    og_img = SITE + "/images/" + og_file
    og_alt = esc(og_meta["alt"])
    robots = "noindex, follow" if page.get("noindex") else "index, follow, max-image-preview:large"
    canonical = "" if page.get("noindex") else f'\n<link rel="canonical" href="{url}">'
    preload = page.get("preload", "")
    if preload:
        preload = f'\n<link rel="preload" as="image" href="/images/{IMAGES[preload]["file"]}" fetchpriority="high">'
    body = expand(body)
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<meta name="robots" content="{robots}">{canonical}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Happy People Rentals">
<meta property="og:locale" content="en_CA">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="{og_type}">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta property="og:image:alt" content="{og_alt}">
<meta property="article:publisher" content="{BUSINESS['facebook']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{og_img}">
<meta name="twitter:image:alt" content="{og_alt}">
<meta name="theme-color" content="#3F3413">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bowlby+One&family=Figtree:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/site.css">{preload}
<script type="application/ld+json">
{schema(page, url, body)}
</script>
<script src="/site.js" defer></script>
</head>
<body{' class="has-hero"' if overlay else ''}>
<script>document.body.classList.add('js')</script>
<a class="skip" href="#main">Skip to content</a>
{header(path, overlay)}
<main id="main">
{breadcrumbs(page)}
{body.strip()}
</main>
{footer()}
</body>
</html>
"""


# ---------------------------------------------------------------- build

def out_file(path):
    if path.endswith(".html"):
        return os.path.join(ROOT, path.lstrip("/"))
    return os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")


def main():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*", text, re.S)
        if not m:
            fail(f"{name} has no settings block at the top")
        page = json.loads(m.group(1))
        for key in ("path", "title", "description"):
            if key not in page:
                fail(f"{name} is missing '{key}'")
        if page["path"] != "/" and "crumb" not in page:
            fail(f"{name} is missing 'crumb'")
        if len(page["title"]) > 65:
            print(f"warning: {name} title is {len(page['title'])} characters (aim for 60 or fewer)")
        if not 110 <= len(page["description"]) <= 165:
            print(f"warning: {name} description is {len(page['description'])} characters (aim for 120-160)")
        html_out = render(page, text[m.end():])
        if "{{" in html_out:
            fail(f"{name} has an unfinished {{{{...}}}} snippet")
        dest = out_file(page["path"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(html_out)
        # photos on the page, listed in the sitemap so they can appear in Google Images
        main_html = html_out.split('<main id="main">', 1)[-1].split("</main>", 1)[0]
        page["_images"] = list(dict.fromkeys(re.findall(r'<img src="(/images/[^"]+)"', main_html)))
        pages.append(page)
        print(f"wrote {os.path.relpath(dest, ROOT)}")

    today = datetime.date.today().isoformat()
    urls = []
    for p in sorted(pages, key=lambda p: (p["path"] != "/", p["path"])):
        if p.get("noindex") or p["path"].endswith(".html"):
            continue
        imgs = "".join(f"\n    <image:image><image:loc>{SITE}{i}</image:loc></image:image>" for i in p["_images"])
        urls.append(f"  <url>\n    <loc>{abs_url(p['path'])}</loc>\n    <lastmod>{today}</lastmod>{imgs}\n  </url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        "User-agent: *\nDisallow: /src/\nDisallow: /tools/\nDisallow: /send-form.php\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n")
    n_img = sum(len(p["_images"]) for p in pages if not p.get("noindex"))
    print(f"wrote sitemap.xml ({len(urls)} pages, {n_img} images) and robots.txt")


if __name__ == "__main__":
    main()
