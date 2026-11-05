HAPPY PEOPLE RENTALS — WEBSITE PACKAGE
======================================

Plain HTML, CSS and a little JavaScript. No WordPress, no database.
The only server-side piece is send-form.php (PHP mail), which Hostinger runs natively.

Every page uses the same web address as the current WordPress site, so Google
keeps the rankings those pages already have:

  /                                          Home
  /rental-catalog/                           Rental Catalog (all items and prices)
  /giant-games/                              Giant & yard games
  /inflatable-games/                         Inflatable games
  /bouncy-castle/                            Bouncy castle
  /photo-booth/                              Photo booth & flower walls
  /flower-bar/                               Flower bar & umbrellas
  /tables-chairs-for-every-celebration/      Tables & chairs
  /gallery/                                  Gallery
  /about/                                    About
  /contact-us/                               Contact
  /get-a-quote/                              Get a quote
  /packages/                                 Packages (new page)

Old WordPress addresses that are gone (/home/, /rentals/, /shop/ and the old
sitemap files) are redirected to the right new page by .htaccess.


1. WHAT TO UPLOAD
-----------------
Upload these to Hostinger's public_html folder:

  index.html  404.html  site.css  site.js  send-form.php
  .htaccess  robots.txt  sitemap.xml
  images/  media/
  about/  bouncy-castle/  contact-us/  flower-bar/  gallery/  get-a-quote/
  giant-games/  inflatable-games/  packages/  photo-booth/  rental-catalog/
  tables-chairs-for-every-celebration/

Do NOT upload: src/  tools/  uploads/  netlify.toml  README.md  README.txt
(.htaccess also blocks src/, tools/ and uploads/ in case they are uploaded by mistake.)

.htaccess starts with a dot, so some file managers hide it. In Hostinger's File
Manager, turn on "Show hidden files" to check it is there.


2. REPLACING THE WORDPRESS SITE
-------------------------------
1. In Hostinger, make a full backup of the current website first.
   Before deleting anything, look in public_html for a file named like
   google1234abcd.html (Google Search Console verification). Keep it in
   public_html, or Search Console will lose access. If Search Console was
   verified through a WordPress plugin (Site Kit or All in One SEO), verify it
   again afterwards using "HTML file" or "Domain" in Search Console settings.
2. Move the WordPress files out of public_html (for example into a folder called
   old-wordpress outside public_html), or delete them after the backup.
   The old .htaccess must be replaced by the new one.
3. Upload the files listed above into public_html.
4. Check these in a browser:
     https://happypeoplerentals.ca/               shows the new homepage
     https://happypeoplerentals.ca/home/          lands on the homepage
     https://happypeoplerentals.ca/rentals/       lands on the Rental Catalog
     https://happypeoplerentals.ca/anything-made-up/   shows the "page not found" page
     https://www.happypeoplerentals.ca/           lands on https://happypeoplerentals.ca/
5. Send a test message from the Contact page and a test quote request (section 3).
6. In Google Search Console, open Sitemaps, remove the old sitemap.xml entry if
   it is listed, and submit https://happypeoplerentals.ca/sitemap.xml again.
   Then use "URL inspection" on the homepage and click "Request indexing".

The All in One SEO plugin is no longer needed: every page now carries its own
title, description, social sharing tags and Google business information.


3. FORMS (Hostinger PHP)
------------------------
send-form.php handles both the quote form and the contact form. Open it and check
the two settings at the top:

  $TO   = 'info@happypeoplerentals.ca';      // where enquiries arrive
  $FROM = 'website@happypeoplerentals.ca';   // must be a real mailbox on your domain

In hPanel -> Emails, create the "website@" mailbox if it does not exist.
Hostinger blocks mail() from addresses that are not on your own domain.

The page shows "Request sent" only when the email really went out. If sending
fails, visitors see a message asking them to call or email instead.

Note: the WordPress site's quote page uses a Google Form. The new quote form sends
an email instead. If you prefer to keep the Google Form, tell your web person.


4. CHANGING TEXT, PRICES OR PHOTOS
----------------------------------
The pages are generated from the files in src/:

  src/catalog.json     every rental item: name, price, description, photo
  src/pages/*.html     the text of each page, with its Google title and description
  src/images.json      every photo's file name and its description for Google (alt text)

After editing, run this in a terminal from the project folder:

    python3 tools/build.py

It rewrites the HTML pages, sitemap.xml and robots.txt, and warns if a Google title
or description is too long. Then upload the changed files.

To change a price, edit the "price" number in src/catalog.json and run the build.
The new price appears on every page that shows the item, and in the information
Google reads.

To add a photo: shrink it (no wider than 1000 pixels, saved as .webp or .jpg), give
it a clear file name such as giant-jenga-backyard-party-ottawa.webp, put it in
images/, and add an entry to src/images.json with a description of what it shows.


5. STILL TO CHECK BEFORE LAUNCH
-------------------------------
- Packages page: the three packages (The Backyard, The Block Party, The Field Day)
  came from the earlier website design and are not on the live site. Confirm they
  are real offers, or edit src/pages/packages.html.
- Prices left blank on the live site show "Ask for a price": cocktail table, red
  carpet, popcorn machine, cotton candy machine, garbage bin. Add prices in
  src/catalog.json when ready.
- The homepage video and some product photos are AI-generated or stock images.
  Replacing them with photos from your own events will build more trust.
