# Crema Forge — Espresso Affiliate Starter (Step‑by‑Step)

## 1) Put the site online (Netlify: drag & drop)
1. Go to **netlify.com** → **Sign up**.
2. Click **Add new site → Deploy manually**.
3. Drag the **`site/`** folder from this starter onto Netlify.
4. You’ll get a `*.netlify.app` URL immediately.

## 2) Connect GitHub and enable the daily bot
1. Create a **GitHub** account → **New Repository** (public is fine).
2. Upload everything from this starter (including `bot/` and `.github/workflows/`).
3. Back on Netlify, **Add new site → Import from Git** and select the repo.
4. The included GitHub Action runs daily at ~07:00 AEST and updates `Deals`.

## 3) Add affiliate programs (fast wins)
- **Breville (AU/global)** via Impact: apply as a **Publisher**, property type **Content**.
- **Seattle Coffee Gear (US)**: apply via their affiliate page.
- **Commission Factory (AU network)**: join and apply to appliance/coffee retailers (e.g., Designer Appliances).

> When approved, open `bot/config.yml` and add `link_rules` for each brand to append your tracking parameters.

## 4) Paste your newsletter form
Open `site/index.html`, find “Subscribe” and paste your provider’s embed (Mailchimp/ConvertKit/beehiiv/Substack).

## 5) Publish 1 guide per week
Use the 5 drafts in `site/blog/` as templates. Add comparison tables and links to retailers you’re approved for.

## 6) Optional ads
Apply to **Google AdSense** once you have consistent traffic and a custom domain.

## Compliance tips
- Keep **Disclosure** and **Privacy** linked in the nav (already set).
- Use only permitted feeds; honor robots.txt and site terms.
- Don’t claim results; always tell users to verify price and availability.

---

### Editing `bot/config.yml` (example)

```yaml
max_items: 30
feeds:
  - name: Breville AU
    rss: https://example-breville-feed.example/rss
    source_label: Breville
    link_rules:
      - match_prefix: "https://www.breville.com/"
        append_query: "irgwc=YOUR_IMPACT_ID"
  - name: Seattle Coffee Gear
    rss: https://example-scg-feed.example/rss
    source_label: SCG
    link_rules:
      - match_prefix: "https://www.seattlecoffeegear.com/"
        append_query: "aff=YOUR_ID"
```

> Replace the `rss` with feeds you are allowed to use (brand newsrooms, blogs). Replace `YOUR_*` with the parameters the program provides.
