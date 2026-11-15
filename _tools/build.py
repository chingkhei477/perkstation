#!/usr/bin/env python3
"""
PERKSTATION static page generator.

Writes every .html page (shared header/footer/SEO head) plus robots.txt and,
when SITE_URL is set, canonical URLs, absolute social-image URLs and sitemap.xml.

Usage:  python3 _tools/build.py
Business details (email, address, withdrawal rules) live in js/config.js and
do NOT need a rebuild. Only re-run this if you change SITE_URL or page text.
"""
from pathlib import Path
import json

# --------------------------------------------------------------------------
# Set your live domain (no trailing slash), e.g. "https://www.example.com".
# Left empty -> canonical tags and sitemap are skipped (nothing guessed).
SITE_URL = ""
UPDATED = "15 November 2026"
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
BRAND = "PerkStation"

# ---------------------------------------------------------------- icons ----
P = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "cursor": '<path d="M5 3l14 7-6 2-2 6z"/><path d="M13 13l5 5"/>',
 "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 "radar": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12l6-6"/>',
 "badge": '<path d="M12 3l2.4 1.8 3 .1.9 2.9 2.2 2-1 2.8 1 2.8-2.2 2-.9 2.9-3 .1L12 21l-2.4-1.8-3-.1-.9-2.9-2.2-2 1-2.8-1-2.8 2.2-2 .9-2.9 3-.1z"/><path d="M8.5 12l2.4 2.4 4.6-4.8"/>',
 "wallet": '<path d="M4 7a2 2 0 0 1 2-2h11v4"/><path d="M4 7v11a2 2 0 0 0 2 2h14V9H6a2 2 0 0 1-2-2z"/><circle cx="16" cy="14.5" r="1.3"/>',
 "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 "ticket": '<path d="M3 8a2 2 0 0 0 2-2h14a2 2 0 0 0 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 0-2 2H5a2 2 0 0 0-2-2v-2a2 2 0 0 0 0-4z"/><path d="M14 6v12" stroke-dasharray="2 2.5"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
 "cookie": '<path d="M21 12a9 9 0 1 1-9-9 3 3 0 0 0 3 3 3 3 0 0 0 3 3 3 3 0 0 0 3 3z"/><path d="M8.5 9h.01M9 15h.01M14 14h.01"/>',
 "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
 "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17h.01"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "flag": '<path d="M5 21V4M5 4h12l-2 4 2 4H5"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
 "refresh": '<path d="M20 11a8 8 0 0 0-14.6-4.5L4 8M4 4v4h4M4 13a8 8 0 0 0 14.6 4.5L20 16M20 20v-4h-4"/>',
 "plane": '<path d="M2 12h14M12 6l8 6-8 6"/>',
}
def I(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>')

def LOGO(uid):
    return f'''<svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true">
<defs><mask id="pm-{uid}"><rect width="64" height="64" rx="16" fill="#fff"/><circle cx="0" cy="50" r="6.5" fill="#000"/><circle cx="64" cy="50" r="6.5" fill="#000"/></mask></defs>
<rect width="64" height="64" rx="16" fill="#FF5B2E" mask="url(#pm-{uid})"/>
<line x1="11" y1="50" x2="53" y2="50" stroke="#102A27" stroke-opacity=".35" stroke-width="2" stroke-dasharray="2.5 3"/>
<rect x="17" y="12" width="9" height="30" rx="4.5" fill="#FFF8EE"/>
<circle cx="34" cy="24" r="9.5" fill="none" stroke="#FFF8EE" stroke-width="8"/>
<circle cx="34" cy="24" r="2.6" fill="#102A27"/>
</svg>'''

# ---------------------------------------------------------------- shell ----
NAV = [("index.html", "Home"), ("offers.html", "Offers"), ("how-it-works.html", "How It Works"),
       ("about.html", "About Us"), ("contact.html", "Contact")]
POLICIES = [("privacy-policy.html", "Privacy Policy"), ("terms.html", "Terms &amp; Conditions"),
            ("cashback-policy.html", "Cashback Policy"), ("refund-policy.html", "Refund Policy")]

def head(file, title, desc):
    full_title = title if BRAND in title else f"{title} | {BRAND}"
    url = f"{SITE_URL}/{'' if file == 'index.html' else file}" if SITE_URL else ""
    img = f"{SITE_URL}/assets/img/og-image.png" if SITE_URL else "assets/img/og-image.png"
    canon = f'\n  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">' if url else ""
    org = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND}
    if SITE_URL:
        org["url"] = SITE_URL + "/"
        org["logo"] = SITE_URL + "/assets/img/icon-512.png"
    robots = "noindex, follow" if file == "404.html" else "index, follow"
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#102A27">
  <meta name="color-scheme" content="light">{canon}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{BRAND} — cashback on the way to every checkout">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,650;12..96,750;12..96,800&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap">
  <link rel="stylesheet" href="css/styles.css">
  <script type="application/ld+json">{json.dumps(org)}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

def header(active):
    items = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="{BRAND} home">
      {LOGO("h")}
      <span class="brand-word">PERK<span>STATION</span></span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="nav-list">
{items}
      </ul>
      <div class="nav-mobile-cta"><a class="btn btn--signal" href="offers.html">Browse offers {I("arrow")}</a></div>
    </nav>
    <div class="header-cta">
      <a class="btn btn--signal btn--sm" href="offers.html">Browse offers {I("arrow")}</a>
      <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">
        <span class="bars"><span></span><span></span><span></span></span>
      </button>
    </div>
  </div>
</header>
<main id="main">
'''

def footer():
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    pol = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in POLICIES)
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html" aria-label="{BRAND} home">{LOGO("f")}<span class="brand-word">PERK<span>STATION</span></span></a>
        <p>Cashback that travels with your shopping — clearly tracked, fairly approved and paid to you once it's confirmed.</p>
      </div>
      <div><h4>Explore</h4><ul>{nav}</ul></div>
      <div><h4>Policies</h4><ul>{pol}</ul></div>
      <div>
        <h4>Support</h4>
        <ul>
          <li><a href="contact.html">Contact form</a></li>
          <li data-cfg-show="supportEmail" hidden><a data-cfg-link="supportEmail"></a></li>
          <li data-cfg-show="phone" hidden><a data-cfg-link="phone"></a></li>
          <li data-cfg-show="address" hidden><span data-cfg="address"></span></li>
          <li><a href="how-it-works.html#missing">Missing cashback?</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> {BRAND}. All rights reserved.</p>
      <p>Cashback is paid only after the partner store confirms your purchase.</p>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{I("up")}</button>
<script src="js/config.js" defer></script>
<script src="js/offers.js" defer></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''

def page_hero(crumb, eyebrow, h1, lead, extra=""):
    return f'''<section class="page-hero">
  <div class="wrap">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li aria-current="page">{crumb}</li></ol>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>{extra}
  </div>
</section>
'''

# Reusable config-aware snippets
CONTACT_INLINE = ('our <a href="contact.html">Contact page</a><span data-cfg-show="supportEmail" hidden> or by '
                  'email at <a data-cfg-link="supportEmail"></a></span>')
MIN_WD = ('<span data-cfg-show="minWithdrawal" hidden>The minimum withdrawal amount is <strong data-cfg="minWithdrawal"></strong>. </span>'
          '<span data-cfg-hide="minWithdrawal">The minimum withdrawal amount is published on this page and shown to you before you request a payout. </span>')
PAYOUT = ('<span data-cfg-show="payoutMethods" hidden>Withdrawals are paid via <strong data-cfg="payoutMethods"></strong>. </span>'
          '<span data-cfg-hide="payoutMethods">Available payout methods are listed on this page and confirmed before you request a payout. </span>')

def legal(file, crumb, title, desc, lead, sections):
    toc = "".join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<section id="{sid}"><h2>{t}</h2>{html}</section>' for sid, t, html in sections)
    extra = f'<div class="meta-bar"><span>Last updated: {UPDATED}</span><span>Applies to: {BRAND} website &amp; services</span></div>'
    return (head(file, title, desc) + header(None) + page_hero(crumb, "Policy", title, lead, extra) +
            f'''<section class="section--tight" style="padding-top:0">
  <div class="wrap legal-layout">
    <aside class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{toc}</ol></aside>
    <article class="prose">{body}</article>
  </div>
</section>
<div style="height:clamp(48px,7vw,96px)"></div>
''' + footer())

CTA = f'''<section class="section--tight">
  <div class="wrap">
    <div class="cta-band reveal">
      <span class="ring" aria-hidden="true"></span>
      <div>
        <h2>Your next checkout could be a cashback stop.</h2>
        <p>Start from a PerkStation offer, shop as usual and follow your cashback from tracked to paid.</p>
      </div>
      <div class="btn-row"><a class="btn btn--light" href="offers.html">Browse offers {I("arrow")}</a></div>
    </div>
  </div>
</section>
'''

STATUSES = [
 ("tracked", "Tracked", "We've recorded your visit and the store has reported your order to us."),
 ("pending", "Pending", "The store is waiting for its return or cancellation window to close."),
 ("approved", "Approved", "The store has confirmed the order. The cashback joins your withdrawable balance."),
 ("paid", "Paid", "You requested a withdrawal and the payout has been sent to you."),
 ("declined", "Declined", "The store rejected the order — for example, it was returned, cancelled or broke the offer terms."),
]
def status_grid():
    return '<div class="status-grid">' + "".join(
        f'<div class="status-card reveal"><span class="chip chip--{k}">{t}</span><h3>{t}</h3><p>{d}</p></div>'
        for k, t, d in STATUSES) + '</div>'

ROUTE = [
 ("cursor", "Pick an offer", "Choose a partner store on PerkStation and tap Activate cashback."),
 ("bag", "Shop as usual", "You land on the store's site. Complete your purchase in the same visit."),
 ("radar", "We track it", "The store reports your order to us and it shows as Tracked, then Pending."),
 ("badge", "Store approves", "After the return window closes, the store confirms the order and it's Approved."),
 ("wallet", "Withdraw", "Once your approved balance reaches the minimum, request a payout."),
]
def route():
    return '<ol class="route">' + "".join(
        f'<li class="reveal"><span class="stop">{I(ic)}</span><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in ROUTE) + '</ol>'

def faq(items):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{q}</summary><div class="answer">{a}</div></details>' for q, a in items) + '</div>'

CATEGORIES = ["Fashion", "Electronics", "Travel", "Beauty", "Home &amp; Kitchen", "Food delivery", "Grocery", "Health", "Books", "Gifts"]

# ---------------------------------------------------------------- pages ----
def page_home():
    board = "".join(f"<li>{c}</li>" for c in CATEGORIES)
    home_faq = [
     ("What is PerkStation?", "<p>PerkStation is a cashback and rewards platform. When you visit a partner store through a PerkStation offer and buy something, the store pays us a commission. We share part of it with you as cashback.</p>"),
     ("When does cashback become withdrawable?", "<p>Only after the store confirms your order — usually once its return or cancellation period has ended. Confirmed cashback changes to <strong>Approved</strong> and becomes part of your withdrawable balance.</p>"),
     ("Why could my cashback be declined?", "<p>The most common reasons are returned or cancelled orders, coupon codes not listed on the offer, or a purchase that didn't follow the offer terms. See the <a href=\"cashback-policy.html\">Cashback Policy</a> for the full list.</p>"),
     ("Something didn't track. What now?", f"<p>Keep your order confirmation and contact us through {CONTACT_INLINE} with the store name, order ID and date. The <a href=\"how-it-works.html#missing\">missing cashback guide</a> explains what to include.</p>"),
    ]
    return head("index.html", "PerkStation — Cashback, clearly tracked from click to payout",
                "PerkStation is a cashback platform. Start from a partner offer, shop as usual and follow your cashback from tracked to approved to paid.") + header("index.html") + f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Cashback · rewards · clear tracking</span>
      <h1>Every checkout is a stop on the way to <span class="hl">cashback<svg viewBox="0 0 200 20" preserveAspectRatio="none"><path d="M2 14C50 4 150 4 198 12" stroke="currentColor" stroke-width="10" fill="none" stroke-linecap="round"/></svg></span>.</h1>
      <p class="lead">Start from a PerkStation offer, shop at the store like you normally would, and watch your cashback move from tracked to approved to paid — with every rule written in plain words.</p>
      <div class="btn-row">
        <a class="btn btn--signal" href="offers.html">Browse offers {I("arrow")}</a>
        <a class="btn btn--ghost" href="how-it-works.html">How it works</a>
      </div>
      <ul class="hero-notes">
        <li>{I("check")} Clear status at every stop</li>
        <li>{I("check")} Rules written before you shop</li>
        <li>{I("check")} Paid only on confirmed orders</li>
      </ul>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="boarding">
        <div class="boarding-top">
          <div><div class="label">From</div><div class="val">Partner store</div></div>
          {I("plane", "plane")}
          <div class="to"><div class="label">To</div><div class="val">Your wallet</div></div>
        </div>
        <div class="perf"><span class="notch-r"></span></div>
        <ol class="boarding-steps">
          <li><span class="dot">{I("cursor")}</span>Offer activated<span class="tag">Stop 01</span></li>
          <li><span class="dot">{I("radar")}</span>Order tracked<span class="tag">Stop 02</span></li>
          <li><span class="dot">{I("badge")}</span>Store approves<span class="tag">Stop 03</span></li>
          <li><span class="dot">{I("wallet")}</span>Cashback withdrawn<span class="tag">Stop 04</span></li>
        </ol>
        <div class="boarding-foot"><span>Pass · PerkStation</span><span class="barcode">{"<i></i>" * 22}</span></div>
      </div>
      <div class="stamp"><div>Cashback<br>on board<small>PERKSTATION</small></div></div>
    </div>
  </div>
</section>

<div class="board" aria-label="Shopping categories"><div class="board-track"><ul>{board}</ul><ul aria-hidden="true">{board}</ul></div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">The route</span><h2>Five stops from click to cash.</h2>
      <p class="lead">No guesswork — this is exactly how cashback moves.</p></div>
      <a class="text-link" href="how-it-works.html">Read the full guide {I("arrow")}</a>
    </div>
    {route()}
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Live offers</span><h2>Today's departures.</h2>
      <p class="lead">Genuine partner offers only. Each one shows its rate, validity and terms before you shop.</p></div>
      <a class="text-link" href="offers.html">See all offers {I("arrow")}</a>
    </div>
    <div class="offer-grid" id="offer-preview">
      <noscript><div class="empty"><h3>Offers need JavaScript</h3><p>Please enable JavaScript to see current offers.</p></div></noscript>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Cashback status</span><h2>Always know where your cashback is.</h2>
      <p class="lead">Every purchase carries one of five statuses. Here's what each means.</p></div>
    </div>
    {status_grid()}
  </div>
</section>

<section class="section section--ink">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">How we work</span>
      <p class="big-quote">Cashback should feel like a <em>ticket you can read</em> — not a maze of fine print.</p>
    </div>
    <div class="grid-2">
      <div class="panel reveal"><div class="icon-tile">{I("eye")}</div><h3>Rules up front</h3><p>Rates, exclusions and validity sit on the offer itself, before you click.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--mint">{I("radar")}</div><h3>Honest statuses</h3><p>Tracked, Pending, Approved, Paid or Declined — never a vague "processing".</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--sun">{I("shield")}</div><h3>Your data, respected</h3><p>We collect only what's needed to track and pay cashback. <a href="privacy-policy.html" style="color:inherit">Privacy Policy</a>.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--sky">{I("help")}</div><h3>Real help</h3><p>Missing cashback? Send us the order details and we'll raise it with the store.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Questions</span><h2>Before you board.</h2></div>
    <a class="text-link" href="how-it-works.html#faq">More answers {I("arrow")}</a></div>
    {faq(home_faq)}
  </div>
</section>
''' + CTA + footer()


def page_offers():
    return head("offers.html", "Cashback Offers",
                "Browse genuine PerkStation cashback offers from partner stores. Every offer shows its cashback rate, validity and terms before you shop.") + header("offers.html") + page_hero(
        "Offers", "Offers", "Pick a store. Activate. Shop.",
        "Every offer here is a genuine partner deal, with its rate, validity and terms shown up front. Activate it right before you shop so the store can track your order.") + f'''
<section class="section--tight" style="padding-top:0">
  <div class="wrap">
    <div id="offer-tools">
      <div class="toolbar">
        <label class="search"><span class="sr-only">Search offers</span>{I("search")}<input id="offer-search" type="search" placeholder="Search stores or categories" autocomplete="off"></label>
        <label><span class="sr-only">Sort offers</span>
          <select class="select" id="offer-sort"><option value="featured">Featured first</option><option value="rate">Highest rate</option><option value="az">Store A–Z</option></select>
        </label>
      </div>
      <div class="chips" id="offer-chips" role="group" aria-label="Filter by category" style="margin-bottom:22px"></div>
      <p class="result-count" id="offer-count" aria-live="polite"></p>
    </div>
    <div class="offer-grid" id="offer-grid">
      <noscript><div class="empty"><h3>Offers need JavaScript</h3><p>Please enable JavaScript to browse offers.</p></div></noscript>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Before you click</span><h2>Make sure your cashback tracks.</h2></div></div>
    <div class="grid-3">
      <div class="panel reveal"><div class="icon-tile">{I("cookie")}</div><h3>Allow cookies</h3><p>Tracking relies on the store's cookies. Turn off ad-blockers and avoid private/incognito windows for the visit.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--mint">{I("clock")}</div><h3>Buy in the same visit</h3><p>Complete checkout right after activating. If you leave and return later, activate the offer again.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--sun">{I("ticket")}</div><h3>Only listed coupons</h3><p>Coupon codes not shown on the offer can cancel tracking. When in doubt, check the offer terms.</p></div>
    </div>
  </div>
</section>
''' + CTA + footer()


def page_how():
    how_faq = [
     ("Does PerkStation cost anything to use?", "<p>Using PerkStation offers does not add anything to the price you pay at the store. Cashback is funded from the commission the store pays us.</p>"),
     ("How long does approval take?", "<p>It depends on the store. Most stores confirm orders only after their return or cancellation period ends, and then pass the confirmation to us. Where a store shares an expected timeline, we show it in the offer terms.</p>"),
     ("Can a Pending cashback still be declined?", "<p>Yes. Pending means the store hasn't confirmed the order yet. If the order is returned, cancelled or doesn't meet the offer terms, the store may decline it.</p>"),
     ("Do I earn cashback on the full order value?", "<p>Usually cashback is calculated on the amount the store counts as eligible — typically after discounts and excluding taxes, shipping, gift cards and wallet top-ups. The offer terms say what qualifies.</p>"),
     ("Can I use my own coupon code?", "<p>Only coupons shown on the PerkStation offer are safe to use. Other codes can override tracking, and the store may decline the cashback.</p>"),
     ("What if the store changes the cashback rate?", "<p>The rate that applies is the one shown on the offer when you activated it, as long as the store honours it. If a store revises a rate retrospectively, we follow what the store confirms and explain any change to you.</p>"),
    ]
    elig = '''<ul class="check-list">
<li>You started from a PerkStation offer and completed the purchase in the same visit.</li>
<li>Cookies were allowed and no ad-blocker or private browsing blocked tracking.</li>
<li>You used only coupons listed on the offer (or none).</li>
<li>The products and payment method are eligible under the offer terms.</li>
<li>The order was not returned, exchanged or cancelled, fully or partly.</li>
</ul>'''
    inelig = '''<ul class="check-list x-list">
<li>Orders placed without activating the offer, or in a different visit.</li>
<li>Gift cards, wallet top-ups, taxes, shipping and other excluded items (unless the offer says otherwise).</li>
<li>Returned, cancelled or exchanged items.</li>
<li>Orders using coupons, cashback or rewards from another source not allowed by the offer.</li>
<li>Fraudulent, duplicate, bulk or reseller orders.</li>
</ul>'''
    return head("how-it-works.html", "How Cashback Works — Tracking, Eligibility, Approval & Withdrawal",
                "Learn how PerkStation cashback is tracked, which purchases are eligible, how stores approve orders and how to withdraw your approved cashback.") + header("how-it-works.html") + page_hero(
        "How It Works", "How it works", "Your cashback, stop by stop.",
        "Here's how cashback is tracked, what makes a purchase eligible, how approval works, and when you can withdraw.") + f'''
<section class="section--tight section--ink">
  <div class="wrap">{route()}</div>
</section>

<section class="section" id="tracking">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">01 · Tracking</span>
      <h2>How we know you shopped.</h2>
      <p class="lead">When you tap <strong>Activate cashback</strong>, we send you to the store through a tracked link. The store, or its affiliate network, records that your visit came from PerkStation.</p>
      <p>When you buy something, the store reports the order to us — usually within a few hours, sometimes up to a few days. It then shows in your activity as <strong>Tracked</strong> and then <strong>Pending</strong>. The amount may first appear as an estimate and is finalised when the store confirms.</p>
    </div>
    <div class="stations reveal">
      <div class="station-row"><span class="code">DO</span><div><h3>Activate right before you shop</h3><p>Open the store from PerkStation each time, then check out in that visit.</p></div></div>
      <div class="station-row"><span class="code">DO</span><div><h3>Keep your order confirmation</h3><p>You'll need the order ID and date if anything goes missing.</p></div></div>
      <div class="station-row"><span class="code">AVOID</span><div><h3>Ad-blockers &amp; private windows</h3><p>They can block the cookies the store uses to credit us.</p></div></div>
      <div class="station-row"><span class="code">AVOID</span><div><h3>Switching sites mid-way</h3><p>Visiting another cashback, coupon or price site before checkout can overwrite tracking.</p></div></div>
    </div>
  </div>
</section>

<section class="section section--paper2" id="eligibility">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">02 · Eligibility</span><h2>What qualifies for cashback.</h2>
    <p class="lead">Each offer may add its own conditions. These general rules apply to every offer.</p></div></div>
    <div class="grid-2">
      <div class="panel reveal"><div class="icon-tile icon-tile--mint">{I("check")}</div><h3>Eligible when</h3>{elig}</div>
      <div class="panel reveal"><div class="icon-tile">{I("info")}</div><h3>Not eligible</h3>{inelig}</div>
    </div>
  </div>
</section>

<section class="section" id="approval">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">03 · Approval</span><h2>Who approves it and when.</h2>
    <p class="lead">The store approves cashback, not PerkStation. It confirms that the order is final — not returned, not cancelled and within the offer terms — and passes that to us. We then mark it <strong>Approved</strong>.</p></div></div>
    {status_grid()}
    <div class="note mt-3 reveal"><strong>Why it takes time:</strong> stores usually wait for their return or cancellation window to close before confirming. That's why cashback can stay Pending for a while. Where a store shares an expected approval time, we show it in the offer terms.</div>
  </div>
</section>

<section class="section section--ink" id="withdrawal">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">04 · Withdrawal</span>
      <h2>Getting your cashback out.</h2>
      <p class="lead">Only <strong>Approved</strong> cashback can be withdrawn. Tracked and Pending amounts aren't withdrawable yet.</p>
      <p class="muted">{MIN_WD}{PAYOUT}</p>
    </div>
    <div class="stations reveal" style="color:var(--ink)">
      <div class="station-row"><span class="code">01</span><div><h3>Reach the minimum</h3><p>Your approved balance must reach the minimum withdrawal amount.</p></div></div>
      <div class="station-row"><span class="code">02</span><div><h3>Check your payout details</h3><p>Make sure your payout details are correct — payments sent to details you gave us can't be recalled.</p></div></div>
      <div class="station-row"><span class="code">03</span><div><h3>Request and receive</h3><p>We review the request for security and send the payout. Its status changes to Paid.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap anatomy">
    <div class="reveal">
      <span class="ex-label">Example layout — not a real offer</span>
      <article class="ticket" style="--accent:#102A27" aria-label="Example offer card layout">
        <div class="ticket-head"><div class="monogram" aria-hidden="true">S</div><div><h3 class="ticket-store">Store name</h3><span class="ticket-cat">Category</span></div></div>
        <div class="ticket-rate"><span class="amt"><span class="ph">Rate</span><small>cashback</small></span></div>
        <p class="ticket-desc">What qualifies for this offer.</p>
        <div class="perf" aria-hidden="true"><span class="notch-r"></span></div>
        <div class="ticket-foot"><div class="ticket-meta"><span>Valid till · date</span><span>Terms apply</span></div>
        <div class="ticket-actions"><span class="terms-toggle" style="display:inline-flex;align-items:center">Terms</span><span class="btn btn--signal btn--sm">Activate cashback</span></div></div>
      </article>
    </div>
    <div class="reveal">
      <span class="eyebrow">Reading an offer</span>
      <h2>Every ticket tells you everything.</h2>
      <ol class="callouts">
        <li><div><strong>Store &amp; category</strong><span>The partner store you'll be sent to.</span></div></li>
        <li><div><strong>Cashback rate</strong><span>A percentage of the eligible order value, or a fixed amount.</span></div></li>
        <li><div><strong>Validity</strong><span>The last date the offer applies. "Ongoing" means no fixed end date was given.</span></div></li>
        <li><div><strong>Terms</strong><span>Exclusions, allowed coupons and any store-specific timelines.</span></div></li>
        <li><div><strong>Activate cashback</strong><span>Opens the store through a tracked link. Shop in that same visit.</span></div></li>
      </ol>
    </div>
  </div>
</section>

<section class="section section--paper2" id="missing">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Missing cashback</span>
      <h2>Didn't track? Here's what to do.</h2>
      <p class="lead">Wait at least 72 hours after your purchase. Stores can take that long to report orders. If it still isn't showing, send us a claim.</p>
      <div class="btn-row"><a class="btn" href="contact.html">Raise a missing cashback claim {I("arrow")}</a></div>
    </div>
    <div class="panel reveal">
      <h3>Include in your claim</h3>
      <ul class="check-list">
        <li>Store name and order date</li>
        <li>Order ID and the order amount</li>
        <li>A screenshot or copy of the order confirmation</li>
        <li>The email address you use with PerkStation</li>
      </ul>
      <p class="muted mb-0">We pass claims to the store or its affiliate network. The final decision rests with the store.</p>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">FAQ</span><h2>Common questions.</h2></div></div>
    {faq(how_faq)}
  </div>
</section>
''' + CTA + footer()


def page_about():
    return head("about.html", "About Us",
                "PerkStation is a cashback and rewards platform built on clear tracking, plain-language rules and payouts on confirmed orders.") + header("about.html") + page_hero(
        "About Us", "About PerkStation", "Cashback, with the route on the ticket.",
        "PerkStation exists to make cashback easy to understand — what you can earn, when it's confirmed and how you get paid.") + f'''
<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div class="reveal">
      <h2>What we do</h2>
      <p class="lead">PerkStation partners with online stores and affiliate networks. When you shop through a PerkStation offer, the store pays us a commission for the referral. We share part of it with you as cashback.</p>
      <p>You don't pay anything extra for this. The price at the store is the same; the cashback comes from the commission. Cashback becomes yours once the store confirms the purchase.</p>
    </div>
    <div class="reveal">
      <div class="panel">
        <span class="eyebrow">The name</span>
        <p class="big-quote" style="font-size:clamp(1.4rem,2.6vw,1.9rem)">A station is where journeys are <em>clear</em>: you see the route, the stops and where you'll arrive.</p>
        <p class="mt-2 mb-0">That's how we think cashback should work — every step visible, from the moment you click to the moment you're paid.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Our principles</span><h2>What you can hold us to.</h2></div></div>
    <div class="grid-3">
      <div class="panel reveal"><div class="icon-tile">{I("eye")}</div><h3>Transparency</h3><p>Offer rates, exclusions and statuses are shown plainly. If a store declines cashback, we tell you why when the store gives a reason.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--mint">{I("flag")}</div><h3>Genuine offers only</h3><p>We list only offers we've confirmed with partner stores or networks. No made-up deals, no fake urgency.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--sun">{I("lock")}</div><h3>Privacy by default</h3><p>We collect only the data needed to track and pay cashback, and we never sell your personal data.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--sky">{I("users")}</div><h3>Fair to everyone</h3><p>Clear rules protect shoppers and stores. Misuse and fraud are not allowed, so cashback stays possible for everyone.</p></div>
      <div class="panel reveal"><div class="icon-tile">{I("help")}</div><h3>Helpful support</h3><p>A missing or declined cashback is followed up with the store. You'll always get a straight answer.</p></div>
      <div class="panel reveal"><div class="icon-tile icon-tile--mint">{I("refresh")}</div><h3>Always improving</h3><p>Our policies are written to be read. When they change, we update the date at the top of each page.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Get in touch</span><h2>Questions, partnerships or feedback?</h2>
    <p class="lead">Shoppers, stores and affiliate partners can all reach us through the contact page.</p></div>
    <div class="btn-row reveal"><a class="btn btn--signal" href="contact.html">Contact us {I("arrow")}</a><a class="btn btn--ghost" href="how-it-works.html">How it works</a></div>
  </div>
</section>
''' + footer()


def page_contact():
    return head("contact.html", "Contact Us",
                "Contact PerkStation support about missing cashback, withdrawals, your account or partnerships.") + header("contact.html") + page_hero(
        "Contact", "Contact", "Talk to the station desk.",
        "Missing cashback, a withdrawal question or a partnership idea — send us the details and we'll get back to you.") + f'''
<section class="section" style="padding-top:0">
  <div class="wrap contact-grid">
    <div class="panel reveal">
      <h2 style="font-size:1.6rem">Send a message</h2>
      <p class="muted">Fields marked optional can be left blank. For missing cashback, include the order ID.</p>
      <form class="form" id="contact-form" novalidate>
        <div class="form-row">
          <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required><p class="err" role="alert"></p></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><p class="err" role="alert"></p></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-topic">Topic</label>
            <select id="f-topic" name="topic" required>
              <option value="">Choose a topic</option>
              <option>Missing cashback</option>
              <option>Declined cashback</option>
              <option>Withdrawal / payout</option>
              <option>Account &amp; privacy</option>
              <option>Store partnership</option>
              <option>Other</option>
            </select><p class="err" role="alert"></p></div>
          <div class="field"><label for="f-order">Order ID / store <span class="opt">(optional)</span></label><input id="f-order" name="order" type="text"></div>
        </div>
        <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required></textarea><p class="err" role="alert"></p></div>
        <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <label class="consent"><input type="checkbox" name="consent" id="f-consent"> <span>I agree that PerkStation may use these details to respond to my request, as described in the <a href="privacy-policy.html">Privacy Policy</a>.</span></label>
        <p class="err" id="consent-err" hidden style="color:#B02E27;font-weight:550;margin:-8px 0 0">Please tick the box so we can reply to you.</p>
        <div><button class="btn btn--signal" type="submit">Send message {I("arrow")}</button></div>
        <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
      </form>
    </div>
    <aside class="reveal">
      <div class="panel">
        <h3>Support details</h3>
        <ul class="info-list mt-2">
          <li data-cfg-show="supportEmail" hidden><span class="icon-tile">{I("mail")}</span><div><div class="k">Email</div><div class="v"><a data-cfg-link="supportEmail"></a></div></div></li>
          <li data-cfg-show="phone" hidden><span class="icon-tile icon-tile--mint">{I("phone")}</span><div><div class="k">Phone</div><div class="v"><a data-cfg-link="phone"></a></div></div></li>
          <li data-cfg-show="address" hidden><span class="icon-tile icon-tile--sun">{I("pin")}</span><div><div class="k">Address</div><div class="v" data-cfg="address"></div></div></li>
          <li data-cfg-show="supportHours" hidden><span class="icon-tile icon-tile--sky">{I("clock")}</span><div><div class="k">Support hours</div><div class="v" data-cfg="supportHours"></div></div></li>
          <li data-cfg-hide="supportEmail,phone,address"><span class="icon-tile">{I("info")}</span><div><div class="k">Coming soon</div><div class="v">Our support contact details will be published here shortly.</div></div></li>
        </ul>
      </div>
      <div class="panel mt-2">
        <h3>Quick help</h3>
        <ul class="check-list mb-0">
          <li><a href="how-it-works.html#missing">Missing cashback guide</a></li>
          <li><a href="how-it-works.html#withdrawal">How withdrawals work</a></li>
          <li><a href="cashback-policy.html">Cashback Policy</a></li>
        </ul>
      </div>
    </aside>
  </div>
</section>
''' + footer()


def page_404():
    return head("404.html", "Page not found", "This page isn't on the PerkStation route.") + header(None) + f'''
<section class="section center">
  <div class="wrap">
    <span class="eyebrow">Error 404</span>
    <h1>Wrong platform.</h1>
    <p class="lead" style="margin:0 auto 28px">The page you're looking for isn't on this route. It may have moved, or the link may be mistyped.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--signal" href="index.html">Back to home {I("arrow")}</a><a class="btn btn--ghost" href="offers.html">Browse offers</a></div>
  </div>
</section>
''' + footer()

# ------------------------------------------------------------- policies ----
def page_privacy():
    S = [
     ("intro", "Introduction", f"<p>This Privacy Policy explains how {BRAND} (\"we\", \"us\") collects, uses, shares and protects personal information when you use our website and cashback services. By using {BRAND}, you agree to the practices described here.</p>"),
     ("collect", "Information we collect", """<h3>Information you give us</h3><ul>
<li><strong>Account and contact details</strong> — such as your name, email address and phone number.</li>
<li><strong>Payout details</strong> — the details needed to send your withdrawals.</li>
<li><strong>Support messages</strong> — what you send us, including order IDs and screenshots for missing cashback claims.</li></ul>
<h3>Information collected automatically</h3><ul>
<li><strong>Click and tracking data</strong> — when you activate an offer, we record the time, the store and a unique click reference so the store can credit your purchase.</li>
<li><strong>Transaction data from stores</strong> — order reference, order value, commission and status, as reported by stores or affiliate networks. We do not receive your card or bank details from stores.</li>
<li><strong>Device and usage data</strong> — browser type, device, IP address and pages visited, used for security and to improve the site.</li></ul>"""),
     ("use", "How we use information", """<ul>
<li>To track purchases and credit, approve and pay cashback.</li>
<li>To respond to your requests and handle missing cashback claims.</li>
<li>To prevent fraud, misuse and duplicate claims, and to keep the service secure.</li>
<li>To send service messages about your cashback or account.</li>
<li>To send offers or updates, only where you have agreed. You can opt out at any time.</li>
<li>To meet legal, tax and accounting obligations.</li></ul>"""),
     ("cookies", "Cookies and tracking", """<p>Cashback depends on cookies. When you activate an offer, the store or its affiliate network sets a cookie so the purchase can be linked back to PerkStation. We also use essential cookies to run the site.</p>
<p>You can control cookies in your browser settings. If you block them, cashback may not track.</p>"""),
     ("share", "How we share information", """<p>We do not sell your personal information. We share it only when needed:</p><ul>
<li><strong>Partner stores and affiliate networks</strong> — click references and order details needed to track and confirm purchases or investigate missing cashback.</li>
<li><strong>Payment providers</strong> — the details needed to send your withdrawal.</li>
<li><strong>Service providers</strong> — hosting, email and security providers acting on our instructions.</li>
<li><strong>Legal requirements</strong> — when required by law, or to protect our users, our service or others from fraud or harm.</li></ul>"""),
     ("retention", "Data retention", "<p>We keep personal information only as long as needed for the purposes above. This includes keeping transaction records for as long as tax, accounting or legal rules require. When we no longer need it, we delete or anonymise it.</p>"),
     ("security", "Security", "<p>We use reasonable technical and organisational measures to protect your information, including encrypted connections. No method of transmission or storage is completely secure, so we can't guarantee absolute security. Keep your account details private.</p>"),
     ("rights", "Your choices and rights", f"<p>You can ask to access, correct or delete your personal information, withdraw consent to marketing, or close your account. Some information may be kept where the law requires it. To make a request, contact us through {CONTACT_INLINE}.</p>"),
     ("children", "Children", f"<p>{BRAND} is not intended for anyone under 18. We do not knowingly collect personal information from children. If you believe a child has given us information, please contact us and we will delete it.</p>"),
     ("links", "Third-party sites", "<p>Offers take you to partner stores' websites. Those sites have their own privacy policies, and we are not responsible for how they handle your information. Please review them before you share details.</p>"),
     ("changes", "Changes to this policy", "<p>We may update this policy from time to time. The \"Last updated\" date at the top shows the latest version. Significant changes will be highlighted on the site.</p>"),
     ("contact", "Contact", f"<p>For privacy questions or requests, reach us through {CONTACT_INLINE}.<span data-cfg-show=\"address\" hidden> Postal address: <span data-cfg=\"address\"></span>.</span></p>"),
    ]
    return legal("privacy-policy.html", "Privacy Policy", "Privacy Policy",
                 "How PerkStation collects, uses, shares and protects your personal information when you use our cashback services.",
                 "What we collect, why we collect it, and the choices you have.", S)


def page_terms():
    S = [
     ("acceptance", "Acceptance of terms", f"<p>These Terms &amp; Conditions (\"Terms\") govern your use of the {BRAND} website and cashback services. By using {BRAND}, you agree to these Terms together with our <a href=\"privacy-policy.html\">Privacy Policy</a>, <a href=\"cashback-policy.html\">Cashback Policy</a> and <a href=\"refund-policy.html\">Refund Policy</a>. If you do not agree, please do not use the service.</p>"),
     ("service", "The service", f"<p>{BRAND} shows offers from partner stores. When you visit a store through a {BRAND} offer and make an eligible purchase, the store may pay us a commission, part of which we share with you as cashback. {BRAND} is not the seller of any product or service bought from a partner store.</p>"),
     ("eligibility", "Who can use PerkStation", "<ul><li>You must be at least 18 years old.</li><li>You must provide accurate information and keep it up to date.</li><li>One account per person. Accounts may not be shared, sold or transferred.</li></ul>"),
     ("account", "Your account", "<p>You are responsible for keeping your login details secure and for all activity under your account. Tell us promptly if you suspect unauthorised use.</p>"),
     ("cashback", "Cashback", "<p>Cashback is credited only for eligible purchases that the store tracks and confirms, as described in the <a href=\"cashback-policy.html\">Cashback Policy</a>. Rates shown are set by agreements with stores and may change without notice. Tracked and Pending cashback is not yet earned and may be adjusted or declined.</p>"),
     ("withdrawals", "Withdrawals", f"<p>Only Approved cashback can be withdrawn. {MIN_WD}{PAYOUT}You must give correct payout details. We are not responsible for payments sent to incorrect details you provided. We may verify your identity or review activity before releasing a payout.</p>"),
     ("conduct", "Acceptable use", """<p>You agree not to:</p><ul>
<li>Create multiple or fake accounts, or use someone else's details.</li>
<li>Generate artificial clicks, self-referrals or purchases intended only to earn cashback and then return.</li>
<li>Use bots, scripts or tools to manipulate tracking.</li>
<li>Place bulk, reseller or business orders where the offer excludes them.</li>
<li>Interfere with the website's security or operation.</li></ul>
<p>If we reasonably suspect misuse or fraud, we may hold, adjust or cancel cashback and suspend or close the account involved.</p>"""),
     ("stores", "Partner stores", "<p>Your purchase is a contract between you and the store. Products, delivery, pricing, returns, warranties and customer service are the store's responsibility. Questions about an order should go to the store.</p>"),
     ("ip", "Intellectual property", f"<p>The {BRAND} name, logo, design and content belong to {BRAND} or its licensors. Store names and trademarks belong to their owners and are used only to identify offers.</p>"),
     ("liability", "Disclaimers and limitation of liability", f"<p>The service is provided \"as is\". We do our best to keep offers accurate and tracking reliable, but we cannot guarantee that every purchase will track or be approved, because tracking and approval depend on stores and third-party networks. To the extent permitted by law, {BRAND} is not liable for indirect or consequential losses, and our total liability for any claim relating to cashback is limited to the cashback amount in question.</p>"),
     ("termination", "Suspension and closure", "<p>You may close your account at any time. We may suspend or close accounts that break these Terms. When an account is closed in good standing, Approved cashback that meets the withdrawal requirements can still be withdrawn. Cashback linked to fraud or misuse may be forfeited.</p>"),
     ("changes", "Changes to these Terms", "<p>We may update these Terms from time to time. The \"Last updated\" date shows the current version. Continuing to use the service after changes means you accept them.</p>"),
     ("law", "Governing law", "<p><span data-cfg-show=\"governingLaw\" hidden>These Terms are governed by <span data-cfg=\"governingLaw\"></span>.</span><span data-cfg-hide=\"governingLaw\">These Terms are governed by the laws applicable where " + BRAND + " is registered, and disputes are subject to the courts of that place.</span> We encourage you to contact us first so we can try to resolve any issue informally.</p>"),
     ("contact", "Contact", f"<p>Questions about these Terms? Contact us through {CONTACT_INLINE}.</p>"),
    ]
    return legal("terms.html", "Terms", "Terms &amp; Conditions",
                 "The terms that govern use of the PerkStation website and cashback services, including accounts, cashback, withdrawals and acceptable use.",
                 "The rules for using PerkStation, written as plainly as we can.", S)


def page_cashback():
    table = '''<div class="table-wrap"><table>
<thead><tr><th>Status</th><th>What it means</th><th>Withdrawable?</th></tr></thead><tbody>
<tr><td><span class="chip chip--tracked">Tracked</span></td><td>The store has reported your order to us.</td><td>No</td></tr>
<tr><td><span class="chip chip--pending">Pending</span></td><td>Waiting for the store to confirm, usually after its return or cancellation window.</td><td>No</td></tr>
<tr><td><span class="chip chip--approved">Approved</span></td><td>Confirmed by the store and added to your balance.</td><td>Yes</td></tr>
<tr><td><span class="chip chip--paid">Paid</span></td><td>Withdrawn and sent to your payout details.</td><td>—</td></tr>
<tr><td><span class="chip chip--declined">Declined</span></td><td>Rejected by the store (returned, cancelled or ineligible).</td><td>No</td></tr>
</tbody></table></div>'''
    S = [
     ("overview", "Overview", f"<p>This Cashback Policy explains how cashback on {BRAND} is earned, tracked, approved, declined and withdrawn. It forms part of our <a href=\"terms.html\">Terms &amp; Conditions</a>. Individual offers may add conditions, and the offer's own terms apply where they are more specific.</p>"),
     ("earn", "How cashback is earned", "<ol><li>Activate an offer on PerkStation, which opens the store through a tracked link.</li><li>Complete your purchase on the store's site in the same visit.</li><li>The store reports the order and later confirms whether it is final.</li><li>Confirmed cashback becomes Approved and can be withdrawn once you reach the minimum.</li></ol>"),
     ("tracking", "Tracking", "<p>Tracking relies on cookies and the store's or affiliate network's systems. Orders usually appear within 72 hours but may take longer. To help tracking work:</p><ul><li>allow cookies and turn off ad-blockers for the visit;</li><li>avoid private or incognito windows;</li><li>don't visit other cashback, coupon or price-comparison sites before checkout;</li><li>use only coupons listed on the offer.</li></ul>"),
     ("statuses", "Cashback statuses", table),
     ("eligibility", "Eligible and excluded purchases", """<p>Cashback is normally calculated on the eligible order value — typically after discounts and excluding taxes, shipping, service fees and gift-wrap. Unless an offer says otherwise, these are excluded:</p><ul>
<li>gift cards, vouchers, wallet top-ups and recharges where excluded by the store;</li>
<li>returned, exchanged or cancelled orders (fully or partly);</li>
<li>orders using coupons or rewards from another source not allowed by the offer;</li>
<li>orders placed without activating the offer, or in a later visit;</li>
<li>bulk, reseller, business or fraudulent orders.</li></ul>"""),
     ("approval", "Approval timeline", "<p>The store decides whether an order qualifies. Most stores confirm orders only after their return or cancellation period ends and their own checks are complete. Approval time differs by store. Where a store shares an expected timeline, we show it in the offer terms. PerkStation cannot approve cashback before the store confirms it.</p>"),
     ("adjustments", "Adjustments and declines", "<p>The cashback amount may change if the store adjusts the order — for example, after a partial return or a price change. If an order is returned or cancelled, or breaks the offer terms, the store may decline it. If cashback has already been paid and the store later reverses it, we may deduct that amount from your future cashback.</p>"),
     ("missing", "Missing cashback claims", f"<p>If a purchase hasn't appeared 72 hours after you placed it, contact us through {CONTACT_INLINE}. Include the store name, order ID, order date, order amount and a copy of the order confirmation. Raise claims as soon as possible — many stores accept claims only within a limited period. We pass claims to the store or network, whose decision is final.</p>"),
     ("withdrawal", "Withdrawal", f"<p>Only Approved cashback can be withdrawn. {MIN_WD}{PAYOUT}We may verify your identity or account activity before sending a payout. Make sure your payout details are correct. Payments sent to details you gave us cannot be recalled.</p>"),
     ("expiry", "Inactive accounts", "<p>If we ever introduce an expiry rule for unused balances, we will announce it on this page and give advance notice before it applies to you.</p>"),
     ("misuse", "Misuse and fraud", "<p>We may hold, adjust or cancel cashback, and suspend accounts, where we reasonably suspect fraud, manipulation of tracking, multiple accounts or other abuse described in the <a href=\"terms.html#conduct\">Terms</a>.</p>"),
     ("changes", "Changes to this policy", "<p>Rates and rules can change. The version in force when the store confirms your purchase applies. The \"Last updated\" date shows the current version.</p>"),
    ]
    return legal("cashback-policy.html", "Cashback Policy", "Cashback Policy",
                 "How PerkStation cashback is tracked, which purchases are eligible, how stores approve orders, missing cashback claims and withdrawals.",
                 "Exactly how cashback is tracked, approved, declined and withdrawn.", S)


def page_refund():
    S = [
     ("scope", "What this policy covers", f"<p>{BRAND} does not sell products or services. We are a cashback platform that refers you to partner stores. This Refund Policy explains what happens to cashback when an order is refunded, returned or cancelled, and how payout errors are handled.</p>"),
     ("purchases", "Refunds for purchases", "<p>Your purchase is made with the partner store, so refunds, returns, replacements and cancellations are handled entirely by that store under its own policies. Please contact the store directly about any product, payment or delivery issue. PerkStation cannot issue refunds for store purchases.</p>"),
     ("effect", "How refunds affect cashback", """<ul>
<li><strong>Full return or cancellation</strong> — the cashback for that order is declined.</li>
<li><strong>Partial return</strong> — the cashback is reduced to match the value you kept, as confirmed by the store.</li>
<li><strong>Exchange</strong> — stores often treat exchanges as a return, so the original cashback may be declined.</li>
<li><strong>Refund after payout</strong> — if a store reverses an order after its cashback was paid to you, we may deduct that amount from your future cashback.</li></ul>"""),
     ("payouts", "Payout errors", f"<p>If a withdrawal fails or is returned because of a technical problem on our side, we will retry the payout or return the amount to your balance. If you think a payout amount is wrong, contact us through {CONTACT_INLINE} with the details, and we will investigate and correct any error we find. Payouts sent to incorrect details you provided cannot be recovered by us.</p>"),
     ("fees", "Fees", f"<p>{BRAND} does not charge you to activate offers. If we ever introduce a paid feature, its price and refund terms will be shown clearly before you pay.</p>"),
     ("contact", "Contact", f"<p>Questions about this policy? Reach us through {CONTACT_INLINE}.</p>"),
    ]
    return legal("refund-policy.html", "Refund Policy", "Refund Policy",
                 "How refunds, returns and cancellations at partner stores affect PerkStation cashback, and how payout errors are handled.",
                 "How store refunds and returns affect your cashback.", S)

# ---------------------------------------------------------------- build ----
PAGES = {
 "index.html": page_home, "offers.html": page_offers, "how-it-works.html": page_how,
 "about.html": page_about, "contact.html": page_contact, "privacy-policy.html": page_privacy,
 "terms.html": page_terms, "cashback-policy.html": page_cashback, "refund-policy.html": page_refund,
 "404.html": page_404,
}

def main():
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn(), encoding="utf-8")
    robots = "User-agent: *\nAllow: /\n"
    sm = ROOT / "sitemap.xml"
    if SITE_URL:
        urls = "".join(f"  <url><loc>{SITE_URL}/{'' if n == 'index.html' else n}</loc></url>\n"
                       for n in PAGES if n != "404.html")
        sm.write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
        robots += f"\nSitemap: {SITE_URL}/sitemap.xml\n"
    elif sm.exists():
        sm.unlink()
    (ROOT / "robots.txt").write_text(robots)
    print("Built", len(PAGES), "pages", "(with canonical + sitemap)" if SITE_URL else "(set SITE_URL for canonical + sitemap)")

if __name__ == "__main__":
    main()
