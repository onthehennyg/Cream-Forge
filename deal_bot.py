import os, json, datetime, urllib.parse
import feedparser, yaml
from jinja2 import Template

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(ROOT, "..", "site"))
DEALS_JSON = os.path.join(SITE_DIR, "deals.json")
DEALS_HTML = os.path.join(SITE_DIR, "deals.html")

DEFAULT_CONFIG = {
    "max_items": 30,
    "feeds": [
        {"name": "Example", "rss": "https://example.com/feed", "source_label": "Example", "link_rules": []}
    ]
}

DEALS_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Deals — Crema Forge</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <img src="assets/logo.svg" alt="Crema Forge logo" />
    <nav>
      <a href="index.html">Home</a>
      <a href="deals.html">Deals</a>
      <a href="blog/index.html">Blog</a>
      <a href="disclaimer.html">Disclosure</a>
      <a href="privacy.html">Privacy</a>
    </nav>
  </header>
  <main>
    <h1>Latest Deals</h1>
    <ul class="list">
      {% for d in deals %}
      <li><a href="{{ d.link }}" rel="nofollow sponsored">{{ d.title }}</a> <small class="muted">({{ d.source }})</small></li>
      {% endfor %}
    </ul>
    <p><small class="muted">Always check stock/price at the retailer’s site.</small></p>
  </main>
  <footer>&copy; 2025 Crema Forge.</footer>
</body>
</html>"""

def load_config():
    path = os.path.join(ROOT, "config.yml")
    if not os.path.exists(path):
        return DEFAULT_CONFIG
    with open(path, "r") as f:
        return yaml.safe_load(f) or DEFAULT_CONFIG

def apply_rules(link, rules):
    for r in rules or []:
        pref = r.get("match_prefix")
        q = r.get("append_query")
        if pref and q and link and link.startswith(pref):
            parts = urllib.parse.urlparse(link)
            existing = urllib.parse.parse_qs(parts.query, keep_blank_values=True)
            key = q.split("=")[0]
            if key not in existing:
                sep = "&" if parts.query else "?"
                link = link + sep + q
    return link

def fetch_items(cfg):
    items = []
    for feed in cfg.get("feeds", []):
        parsed = feedparser.parse(feed["rss"])
        for e in parsed.entries[: cfg.get("max_items", 30)]:
            title = e.get("title", "Untitled")
            link = apply_rules(e.get("link"), feed.get("link_rules", []))
            items.append({"title": title.strip(), "link": link, "source": feed.get("source_label", feed.get("name", "Feed"))})
    # dedupe
    seen, uniq = set(), []
    for it in items:
        if it["link"] in seen: 
            continue
        seen.add(it["link"])
        uniq.append(it)
    return uniq[: cfg.get("max_items", 30)]

def write_outputs(deals):
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(DEALS_JSON, "w") as f:
        json.dump({"generated_at": datetime.datetime.utcnow().isoformat() + "Z", "deals": deals}, f, indent=2)
    tpl = Template(DEALS_TEMPLATE)
    with open(DEALS_HTML, "w") as f:
        f.write(tpl.render(deals=deals))

def main():
    cfg = load_config()
    deals = fetch_items(cfg)
    write_outputs(deals)
    print(f"Wrote {len(deals)} deals")

if __name__ == "__main__":
    main()
