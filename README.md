# Ruhi Dairy (vijaya_dairy)

A Django storefront for Ruhi Dairy — product browsing with pack-size
variants, a session-based cart, and the Django admin for catalog management.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/

The included `db.sqlite3` already has sample products. To manage them via
the admin, create a superuser first:

```bash
python manage.py createsuperuser
```

## Deploying to Railway or Render

The project is already set up for this: production settings read from
environment variables, static files are served by WhiteNoise, and the
database switches to Postgres automatically when `DATABASE_URL` is set.

**One important limitation on both platforms' free tiers:** the filesystem
is *ephemeral* — anything written to disk (including `db.sqlite3` and
files uploaded to `media/`) is wiped on every redeploy or restart. That's
why the steps below have you attach a real Postgres database. Product
*images*, though, are baked into this zip under `media/products/`, so
they'll deploy along with the code and don't need special handling unless
you plan to upload new ones from the admin later — if you do, add an
object storage add-on (e.g. Cloudinary or S3) at that point.

### Railway

1. Push this project to a GitHub repo (create one, `git init`, commit, push).
2. On [railway.app](https://railway.app), **New Project → Deploy from GitHub repo**, pick the repo.
3. **New → Database → PostgreSQL** in the same project. Railway sets
   `DATABASE_URL` on your web service automatically.
4. On the web service, go to **Variables** and add:
   - `SECRET_KEY` — generate one locally with
     `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = the domain Railway gives you, e.g.
     `ruhidairy-production.up.railway.app` (check **Settings → Networking**
     for the generated domain, or add it after the first deploy)
5. Railway auto-detects Python and uses the `Procfile` — the `release`
   line runs migrations, then `web` starts `gunicorn`. Nothing else to
   configure.
6. After the first deploy, open a shell (Railway → your service → **Shell**)
   and run `python manage.py createsuperuser` to get into `/admin/`.

### Render

1. Push this project to a GitHub repo.
2. On [render.com](https://render.com), **New → Web Service**, connect the repo.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   Start command: `gunicorn vijaya_dairy.wsgi`
   (Render doesn't use `Procfile` by default, so set these fields directly
   in the dashboard — or delete these two lines and let it read `Procfile`
   if you enable that option under settings.)
4. **New → PostgreSQL** to create a free database, then copy its
   **Internal Database URL** into the web service's environment as
   `DATABASE_URL`.
5. Under **Environment**, add `SECRET_KEY`, `DEBUG=False`, and
   `ALLOWED_HOSTS` (Render's `.onrender.com` domain, shown once the
   service is created).
6. After deploy, use the **Shell** tab to run
   `python manage.py createsuperuser`.

### Either platform — before you push

```bash
# sanity-check locally with production-like settings
DEBUG=False SECRET_KEY=test ALLOWED_HOSTS=localhost python manage.py check --deploy
```

Copy `.env.example` to `.env` if you want to test these variables locally
first (`pip install python-dotenv` isn't wired in — Railway/Render inject
the variables directly, so `.env` is only a reference for what to set in
each dashboard).

## What was fixed in this pass

- **Products page was showing "No products found" for every visitor.**
  The view passed a `products` queryset to the template, but the template
  looped over a `product_groups` variable that was never defined — so the
  loop always fell into its `{% empty %}` branch. The template now loops
  over `products` and reads product-level fields (`name`, `category`,
  `description`, `image`) from the `Product`, and pack size / price /
  stock from each `ProductVariant`, matching the actual models.
- **Cart quantity +/- and remove links pointed at the wrong ID.** They
  used `item.product.id`, but `cart/increase/`, `cart/decrease/`, and
  `cart/remove/` expect a *variant* ID. Fixed to `item.variant.id`.
- **Cart page showed a blank pack size and price.** It read
  `item.product.pack_size` / `item.product.price`, but those fields were
  moved to `ProductVariant` in migration 0003. Fixed to
  `item.variant.pack_size` / `item.variant.price`.
- **Broken images on the home page.** Process photos were referenced at
  `/media/dairy/process/...`, but the files actually live at
  `/media/process/...`. Also fixed a typo'd filename
  (`milk-cooilng.jpg` → `milk-cooling.jpg`) that didn't match what the
  template asked for.
- **Home page fetched featured products but never displayed them.** The
  `home` view builds a `products` queryset that had no matching section
  in the template. Added a "Popular Picks" section so that data is
  actually used.
- **`selectVariant()` JS referenced a per-variant image** (`data-image`,
  `.dataset.image`) that doesn't exist — `ProductVariant` has no `image`
  field, only `Product` does. Removed the dead image-swap code and
  renamed `data-product-id` to `data-variant-id` for clarity, since it
  was always a variant ID despite the name.
- **`settings.py` had an invalid `MAILERS` setting** (not a real Django
  setting — the correct name is `EMAIL_BACKEND`) and a duplicate
  `STATIC_URL` definition. Both cleaned up.
- **Removed the committed `venv/` folder** (~85 MB, Windows-only
  binaries) and `__pycache__/` directories from the project, and added
  `requirements.txt` + `.gitignore` so the environment is reproducible
  without shipping it.
- **Made the project deployable to Railway/Render**: `settings.py` now
  reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL` from
  environment variables (falling back to safe local-dev defaults),
  added WhiteNoise for static files and `dj-database-url` +
  `psycopg2-binary` for Postgres, and added a `Procfile`, `runtime.txt`,
  and `.env.example`.

## Project structure

```
manage.py
vijaya_dairy/     # project settings, URLs
dairy/            # app: models, views, admin, migrations
templates/        # base.html, home.html, products.html, cart.html
static/           # css/style.css, js/script.js
media/            # product & site images
```
