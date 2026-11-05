# Happy People Rentals

Website for [Happy People Rentals](https://happypeoplerentals.ca), a party and yard game rental business serving Ottawa, Gatineau and surrounding areas.

## How it's built

- Plain HTML pages, one shared stylesheet (`site.css`) and a small script (`site.js`). No framework, no database.
- Pages live at the same addresses as the WordPress site they replace (for example `/giant-games/`), so existing Google rankings carry over.
- `send-form.php` emails the quote and contact forms (PHP `mail()` on Hostinger).
- `.htaccess` redirects old WordPress addresses, forces `https://happypeoplerentals.ca`, and sets caching.

Each page includes its own title, meta description, canonical URL, Open Graph tags and schema.org structured data (LocalBusiness, Service with prices, BreadcrumbList and FAQPage).

## Editing

Page text, prices and photos are kept in `src/`:

| File | What it holds |
| --- | --- |
| `src/catalog.json` | Every rental item with its price, description and photo |
| `src/pages/*.html` | Each page's text, Google title and description |
| `src/images.json` | Photo file names and alt text |

After changing anything in `src/`, rebuild the pages (Python 3, standard library only):

```bash
python3 tools/build.py
```

This regenerates the HTML pages, `sitemap.xml` and `robots.txt`.

## Deploying

See `README.txt` for the list of files to upload to Hostinger and the steps for replacing the WordPress site.

## License

See `LICENSE`.
