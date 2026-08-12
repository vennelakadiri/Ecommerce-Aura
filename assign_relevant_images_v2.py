"""
Assign relevant product images using the Wikimedia Commons API (v2).

WHY THIS VERSION EXISTS
v1 scraped Pexels' search pages, but Pexels blocks plain scripted HTTP
requests with a 403 (bot protection), even with a normal User-Agent.
Wikimedia Commons instead exposes a genuine public JSON API meant for
exactly this kind of programmatic use - no key, no login, and it won't
block a well-behaved script that sends a descriptive User-Agent (which
is literally their documented etiquette requirement).

WHAT THIS DOES
- Reads every Product + its ProductImage row from db.sqlite3
- For each product, builds a clean search query from the product name
- Calls https://commons.wikimedia.org/w/api.php (generator=search over
  the File: namespace) to get real, real-world photo/file results with
  their titles (used as captions) and a ready-to-use thumbnail URL
  (upload.wikimedia.org - safe to hotlink)
- Scores each candidate's title against the product name + category,
  picks the best match, and avoids reusing a file already assigned to
  another product in this run
- Writes the winning thumbnail URL into ProductImage.image
- Caches query -> candidate list on disk (wikimedia_cache.json) so
  re-runs and partial runs don't refetch the same searches
- NEVER touches the store_banner table

USAGE
    python assign_relevant_images.py --category men            # one category
    python assign_relevant_images.py --category men --limit 20 # test on first 20
    python assign_relevant_images.py --all                     # entire catalog
    python assign_relevant_images.py --category men --dry-run  # preview only, no DB writes

Run this from the project root (same folder as manage.py / db.sqlite3).
Uses only the Python standard library - no pip install needed.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite3")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wikimedia_cache.json")

STOPWORDS = {
    "men", "mens", "men's", "women", "womens", "women's", "boys", "girls",
    "kids", "kid's", "unisex", "the", "a", "an", "for", "with", "and", "pack",
    "set", "style", "classic", "premium", "designer", "regular", "of",
}

API_URL = "https://commons.wikimedia.org/w/api.php"

# Wikimedia asks scripts to identify themselves - this is their documented
# etiquette, not an auth requirement. Any descriptive UA works.
HEADERS = {
    "User-Agent": "MiniprojectProductImageAssigner/1.0 (student ecommerce demo project; contact: not-provided)",
}


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def clean_query(name, gender=None, category=None):
    words = re.findall(r"[a-zA-Z]+", name.lower())
    words = [w for w in words if w not in STOPWORDS]
    if not words:
        words = re.findall(r"[a-zA-Z]+", name.lower())
    query_words = words[:4]
    if gender and gender not in ("unisex",):
        query_words = [gender] + query_words
    return " ".join(query_words)


def fetch_wikimedia_search(query, cache, max_retries=5):
    if query in cache:
        return cache[query]

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": 6,  # File: namespace
        "gsrlimit": 20,
        "gsrsearch": "%s filetype:bitmap" % query,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 600,
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)

    data = None
    for attempt in range(max_retries):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else (2 ** attempt) * 2
                print("  ... rate limited, waiting %.1fs (attempt %d/%d)" % (wait, attempt + 1, max_retries))
                time.sleep(wait)
                continue
            print("  ! fetch failed for %r: %s" % (query, e))
            cache[query] = []
            return []
        except Exception as e:
            print("  ! fetch failed for %r: %s" % (query, e))
            cache[query] = []
            return []
    if data is None:
        print("  ! giving up on %r after %d rate-limit retries" % (query, max_retries))
        cache[query] = []
        return []

    pages = data.get("query", {}).get("pages", {})
    candidates = []
    for page in pages.values():
        title = page.get("title", "")
        title = re.sub(r"^File:", "", title)
        title = re.sub(r"\.(jpg|jpeg|png|gif|svg|tif|tiff|webp)$", "", title, flags=re.I)
        imageinfo = page.get("imageinfo") or []
        if not imageinfo:
            continue
        info = imageinfo[0]
        thumb = info.get("thumburl") or info.get("url")
        if not thumb:
            continue
        candidates.append({"id": str(page.get("pageid")), "caption": title, "url": thumb})

    cache[query] = candidates
    return candidates


def score_candidate(caption, product_name, extra_terms):
    caption_words = set(re.findall(r"[a-zA-Z]+", caption.lower()))
    target_words = set(re.findall(r"[a-zA-Z]+", product_name.lower())) | set(extra_terms)
    target_words -= STOPWORDS
    if not target_words:
        return 0
    overlap = caption_words & target_words
    return len(overlap)


MIN_SCORE = 1  # require at least one real word-overlap; 0-score "matches" are noise, not relevance


def pick_best_image(candidates, product_name, extra_terms, used_ids):
    scored = []
    for c in candidates:
        if c["id"] in used_ids:
            continue
        s = score_candidate(c["caption"], product_name, extra_terms)
        scored.append((s, c))
    if not scored:
        scored = [(score_candidate(c["caption"], product_name, extra_terms), c) for c in candidates]
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best = scored[0]
    if best_score < MIN_SCORE:
        return None  # nothing genuinely relevant - better to skip than guess wrong
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", help="category slug, e.g. men, women, kids, beauty, home, accessories")
    parser.add_argument("--all", action="store_true", help="process the entire catalog")
    parser.add_argument("--limit", type=int, default=None, help="only process first N products (testing)")
    parser.add_argument("--dry-run", action="store_true", help="print planned changes, do not write to DB")
    parser.add_argument("--sleep", type=float, default=1.5, help="seconds to sleep between new API calls")
    args = parser.parse_args()

    if not args.category and not args.all:
        print("Specify --category <slug> or --all")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if args.all:
        cur.execute("""
            SELECT p.id AS product_id, p.name, p.gender, cat.slug AS category_slug,
                   pi.id AS image_id
            FROM store_product p
            JOIN store_category cat ON p.category_id = cat.id
            JOIN store_productimage pi ON pi.product_id = p.id
            ORDER BY cat.slug, p.name
        """)
    else:
        cur.execute("""
            SELECT p.id AS product_id, p.name, p.gender, cat.slug AS category_slug,
                   pi.id AS image_id
            FROM store_product p
            JOIN store_category cat ON p.category_id = cat.id
            JOIN store_productimage pi ON pi.product_id = p.id
            WHERE cat.slug = ?
            ORDER BY p.name
        """, (args.category,))

    rows = cur.fetchall()
    if args.limit:
        rows = rows[: args.limit]

    print("Processing %d product(s)..." % len(rows))

    cache = load_cache()
    used_ids = set()
    updates = []  # (image_id, new_url, product_name, caption)
    new_fetches = 0
    failures = 0

    for row in rows:
        query = clean_query(row["name"], row["gender"], row["category_slug"])
        was_cached = query in cache
        candidates = fetch_wikimedia_search(query, cache)
        if not was_cached:
            new_fetches += 1
            save_cache(cache)
            time.sleep(args.sleep)

        if not candidates:
            print("  ! no candidates for %r (query=%r) - skipping" % (row["name"], query))
            failures += 1
            continue

        best = pick_best_image(candidates, row["name"], [row["category_slug"] or ""], used_ids)
        if not best:
            print("  ! no match for %r - skipping" % row["name"])
            failures += 1
            continue

        used_ids.add(best["id"])
        updates.append((row["image_id"], best["url"], row["name"], best["caption"]))

    print("\nDone scoring. %d new API calls made, %d updates prepared, %d skipped.\n" % (new_fetches, len(updates), failures))

    for image_id, url, name, caption in updates[:30]:
        print("  %-35s -> [%s]" % (name[:33], caption[:45]))
    if len(updates) > 30:
        print("  ... and %d more" % (len(updates) - 30))

    if args.dry_run:
        print("\nDry run - no database changes made.")
        return

    for image_id, url, name, caption in updates:
        cur.execute("UPDATE store_productimage SET image = ? WHERE id = ?", (url, image_id))
    conn.commit()
    print("\nDatabase updated: %d ProductImage rows changed." % len(updates))
    print("store_banner table was not touched.")


if __name__ == "__main__":
    main()
