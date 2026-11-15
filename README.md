# PERKSTATION — cashback website

Static, dependency-free site. Upload the whole folder to any host (Netlify, Vercel, GitHub Pages, cPanel, Hostinger…). `index.html` is the home page; `404.html` is the error page.

## Structure
```
index.html  offers.html  how-it-works.html  about.html  contact.html
privacy-policy.html  terms.html  cashback-policy.html  refund-policy.html  404.html
css/styles.css          design system (colours, type, components)
js/config.js            ← YOUR BUSINESS DETAILS (email, phone, address, withdrawal rules)
js/offers.js            ← YOUR OFFERS (genuine partner offers only)
js/main.js              navigation, offers, contact form, effects
assets/img/             logo, favicon, app icons, social-share image
favicon.ico  site.webmanifest  robots.txt
_tools/build.py         page generator (optional; only for domain/SEO or text changes)
```

## 1. Add business details — `js/config.js`
Fill in the genuine values. Empty fields are hidden automatically, and nothing is made up.
The contact form opens the visitor's email app, addressed to `supportEmail`.

## 2. Add offers — `js/offers.js`
Copy the commented example. Only https links are shown. Offers past `validTill` hide themselves.
While the list is empty, the site shows an "offers coming soon" state.

## 3. Set your domain (canonical URLs + sitemap)
Edit `SITE_URL` at the top of `_tools/build.py`, then run `python3 _tools/build.py`.
This adds canonical tags, absolute social-image URLs and `sitemap.xml`.

## Brand
- Colours: Pine `#102A27` · Signal `#FF5B2E` · Paper `#F5F1E8` · Mint `#CFE9D7` · Sun `#FFD166`
- Type: Bricolage Grotesque (display) · Instrument Sans (body) · JetBrains Mono (labels), via Google Fonts
- Motif: offers are perforated tickets, and the cashback journey is a route of stops.
