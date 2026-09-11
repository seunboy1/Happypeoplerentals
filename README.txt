HAPPY PEOPLE RENTALS — WEBSITE PACKAGE
======================================

Built with plain HTML, CSS and JavaScript. No build step, no npm, no database.
The only server-side piece is send-form.php (PHP mail), which Hostinger runs natively.


1. WHAT TO UPLOAD
-----------------
Upload the CONTENTS of this folder into your Hostinger public_html directory:

  Happy People Rentals.dc.html   <- home page
  Catalog.dc.html                <- rentals
  Packages.dc.html
  About.dc.html
  Contact.dc.html
  Quote.dc.html
  SiteHeader.dc.html             <- shared nav (required)
  SiteFooter.dc.html             <- shared footer (required)
  support.js                     <- runtime (required)
  send-form.php                  <- form handler
  media/hero.mp4                 <- hero video
  images/                        <- photos (see section 3)

Optional but recommended: rename "Happy People Rentals.dc.html" to index.html so the
site loads at happypeoplerentals.ca with no filename. If you do, also update the
"Home" links inside SiteHeader.dc.html and SiteFooter.dc.html to point at index.html.


2. FORMS (Hostinger PHP)
------------------------
send-form.php handles both the Quote form and the Contact form.

Before going live, open send-form.php and check the two settings at the top:

  $TO   = 'info@happypeoplerentals.ca';      // where enquiries arrive
  $FROM = 'website@happypeoplerentals.ca';   // must be a real mailbox on your domain

In Hostinger: hPanel -> Emails -> create the "website@" mailbox if it does not exist.
Hostinger blocks mail() from addresses that are not hosted on your own domain, so
$FROM must be your domain — not gmail.com.

Both forms POST JSON to send-form.php and it emails you a plain-text summary with
Reply-To set to the sender, so you can reply directly from your inbox.
A hidden honeypot field catches most spam bots.

To test: submit the Contact form on the live site, then check the inbox. If nothing
arrives, check hPanel -> Emails -> Email Logs.


3. IMAGES — ONE MANUAL STEP
---------------------------
I cannot download files from your live site, so the images/ folder is empty.
The pages are already coded to load "images/<filename>" first and fall back to the
live happypeoplerentals.ca URL if the local file is missing — so the site works
either way, but local files are faster and survive your old site being taken down.

Download these 20 files and drop them into images/ keeping the exact filenames:

  https://happypeoplerentals.ca/wp-content/uploads/2026/06/Giant-Connect-4-1024x1011.jpg
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/Giant-Jenga-1-1024x768.jpg
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/Cornhole.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/Ladder-Toss.jpg
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-13-2026-12_02_58-AM-1.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-13-2026-12_08_32-AM-1.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-12-2026-07_24_31-PM-1.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-12-2026-07_30_27-PM-1.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-15-2026-02_43_28-PM-1.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-15-2026-02_40_14-PM-2.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/virgil-cayasa-lskYDE0WKJg-unsplash-5-684x1024.jpg
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-8-2026-03_06_26-PM-1-1024x768.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/ChatGPT-Image-Aug-14-2026-06_46_57-PM-1-1024x768.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/meritt-thomas-6d6bTwUDTE0-unsplash-1-1-683x1024.jpg
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/ping-pong.jpeg
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/ChatGPT-Image-Aug-14-2026-06_54_01-PM-1024x768.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/foosball.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/06/ChatGPT-Image-Jun-26-2026-10_56_06-PM-1-1024x683.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/ChatGPT-Image-Aug-12-2026-02_31_00-PM-1024x585.png
  https://happypeoplerentals.ca/wp-content/uploads/2026/08/ChatGPT-Image-Aug-14-2026-05_10_33-PM-1024x525.png

Easiest route: hPanel -> File Manager on the old site, or the WordPress Media Library
(Media -> Library -> select -> Download). Filenames must match exactly, including case.


4. VIDEO
--------
hero.mp4 is 18.6 MB. That plays fine over Hostinger, but for faster loading on phones
consider compressing it to around 5-8 MB (HandBrake, "Fast 1080p30" preset) and also
adding a poster image so something shows before the video starts.


5. WHAT IS STILL OPEN
---------------------
- No pricing anywhere. Add numbers or "from $X" ranges when you are ready.
- No gallery page yet.
- Confirm the Facebook page URL in SiteFooter.dc.html and Contact.dc.html.
- Social links point to @happypeoplerentals on Instagram.


Questions: this package is static files. Anything can be edited in a text editor —
copy, prices, phone numbers — then re-uploaded.
