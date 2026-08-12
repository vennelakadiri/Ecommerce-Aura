"""
Assign relevant product images by scraping Pexels' public search results.

WHAT THIS DOES
- Reads every Product + its ProductImage row from db.sqlite3
- For each product, builds a clean search query from the product name
- Fetches https://www.pexels.com/search/<query>/ (public page, no API key)
- Parses out real photo IDs + their alt-text captions
- Scores each candidate photo's caption against the product name + category
  + gender, picks the best match, and avoids reusing a photo already
  assigned to another product in this run
- Writes the winning https://images.pexels.com/... URL into ProductImage.image
- Caches query -> candidate list on disk (pexels_cache.json) so re-runs
  and partial runs don't refetch the same searches
- NEVER touches the store_banner table

WHY SCRAPING INSTEAD OF THE OFFICIAL API
Pexels' official API needs a free key. This avoids that requirement
entirely by reading the same public search page a browser would load.
Be reasonable with request volume (this script sleeps between requests).

USAGE
    python assign_relevant_images.py --category men            # one category
    python assign_relevant_images.py --category men --limit 20 # test on first 20
    python assign_relevant_images.py --all                     # entire catalog
    python assign_relevant_images.py --category men --dry-run  # preview only, no DB writes

Run this from the project root (same folder as manage.py / db.sqlite3).
Requires: pip install requests
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

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite3")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pexels_cache.json")

STOPWORDS = {
    "men", "mens", "men's", "women", "womens", "women's", "boys", "girls",
    "kids", "kid's", "unisex", "the", "a", "an", "for", "with", "and", "pack",
    "set", "style", "classic", "premium", "designer", "regular", "casual",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
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


def fetch_pexels_search(query, cache):
    if query in cache:
        return cache[query]

    url = "https://www.pexels.com/search/%s/" % urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print("  ! fetch failed for %r: %s" % (query, e))
        cache[query] = []
        return []

    # Pattern: <a href="/photo/<slug>-<id>/" ...>CAPTION TEXT</a>
    # and the matching download link images.pexels.com/photos/<id>/...
    photo_links = re.findall(r'/photo/([a-z0-9\-]+)-(\d+)/', html)
    seen_ids = {}
    for slug, pid in photo_links:
        if pid not in seen_ids:
            caption = slug.replace("-", " ")
            seen_ids[pid] = caption

    candidates = [
        {"id": pid, "caption": caption}
        for pid, caption in seen_ids.items()
    ]
    cache[query] = candidates
    return candidates


def score_candidate(caption, product_name, extra_terms):
    caption_words = set(caption.lower().split())
    target_words = set(re.findall(r"[a-zA-Z]+", product_name.lower())) | set(extra_terms)
    target_words -= STOPWORDS
    if not target_words:
        return 0
    overlap = caption_words & target_words
    return len(overlap)


def pick_best_image(candidates, product_name, extra_terms, used_ids):
    scored = []
    for c in candidates:
        if c["id"] in used_ids:
            continue
        s = score_candidate(c["caption"], product_name, extra_terms)
        scored.append((s, c))
    if not scored:
        # allow reuse if every candidate is exhausted
        scored = [(score_candidate(c["caption"], product_name, extra_terms), c) for c in candidates]
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def pexels_image_url(photo_id):
    return "https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg?auto=compress&cs=tinysrgb&w=600&h=600&fit=crop" % (photo_id, photo_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", help="category slug, e.g. men, women, kids, beauty, home, accessories")
    parser.add_argument("--all", action="store_true", help="process the entire catalog")
    parser.add_argument("--limit", type=int, default=None, help="only process first N products (testing)")
    parser.add_argument("--dry-run", action="store_true", help="print planned changes, do not write to DB")
    parser.add_argument("--sleep", type=float, default=1.0, help="seconds to sleep between new Pexels fetches")
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

    for row in rows:
        query = clean_query(row["name"], row["gender"], row["category_slug"])
        was_cached = query in cache
        candidates = fetch_pexels_search(query, cache)
        if not was_cached:
            new_fetches += 1
            save_cache(cache)
            time.sleep(args.sleep)

        if not candidates:
            print("  ! no candidates for %r (query=%r) - skipping" % (row["name"], query))
            continue

        best = pick_best_image(candidates, row["name"], [row["category_slug"] or ""], used_ids)
        if not best:
            print("  ! no match for %r - skipping" % row["name"])
            continue

        used_ids.add(best["id"])
        url = pexels_image_url(best["id"])
        updates.append((row["image_id"], url, row["name"], best["caption"]))

    print("\nDone scoring. %d new Pexels searches performed, %d updates prepared.\n" % (new_fetches, len(updates)))

    for image_id, url, name, caption in updates[:30]:
        print("  %-40s -> [%s] %s" % (name[:38], caption[:30], url))
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
