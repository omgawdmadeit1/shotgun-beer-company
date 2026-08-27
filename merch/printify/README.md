# Phase 1 merch SKU list (Printify / DTC)

**Linear:** [SMI-150](https://linear.app/smileing-goats/issue/SMI-150/phase-1-merch-sku-list-via-printify-dtc)
**Status:** SKU list locked. **Do not publish.**

SafeShot revenue is not waiting on merch. PrintifyOperator publishes only after the gates below.

## Locked SKUs (2–3)

| SKU | Product | Printify blueprint | Provider | Launch variants | Retail |
|---|---|---|---|---|---|
| **SS-TEE-01** | Side Quest Tee | `12` Bella+Canvas 3001 | Printify Choice `99` (SwiftPOD `39` fallback) | Black S–3XL (`18100`–`18105`) | $32 / $34 2XL / $36 3XL |
| **SS-HAT-01** | Side Quest Dad Cap | `1447` Yupoong 6245CM | Printify Choice `99` | Black One size (`105372`) | $30 |
| **SS-KOO-01** | Side Quest Can Cooler | `951` Generic Can Cooler | Pic The Gift `92` | Regular 12oz (`78460`) | $16 |

Catalog IDs and US shipping were read live from the Printify Catalog API on 2026-08-27. No products were created.

## Why these three

- **Tee** is the brand billboard. 3001 is the Printify apparel default (retail fit, black DTG).
- **Dad cap** is the tailgate / ritual object. Embroidery holds up; keep the mark simple (no gradient).
- **Koozie** is the cheap ritual object that matches a 12oz can. First-item US ship is $5.39 — sell it as an add-on, not a loss-leader.

Held: Pillar Badge/patch (Brand T030) and Comfort Colors 1717. Not tee/hat/koozie; do not split SKUs at launch.

## Publish gates (all required)

1. Real waitlist live ([SMI-145](https://linear.app/smileing-goats/issue/SMI-145/urgent-replace-fake-waitlist-alert-with-real-email-capture)).
2. SafeShot path moving ([SMI-148](https://linear.app/smileing-goats/issue/SMI-148/safeshot-product-page-pre-order-path)).
3. **New SIDESHOT Printify shop.** Do **not** use shop `20002621` (LvlxLtd, 251 wall-art posters) or `27582906` (empty generic Shopify).
4. Real brand files ([SMI-151](https://linear.app/smileing-goats/issue/SMI-151/locate-existing-sideshot-brand-assets-not-on-this-computer)) or Joseph-approved placeholder wordmark.
5. 21+ + “drink responsibly / never force consumption” on every listing.

## Operator packet

Machine-readable contract: [`phase1-sku-catalog.json`](phase1-sku-catalog.json)

```bash
python3 merch/printify/validate_catalog.py
python3 merch/printify/test_catalog.py
```

PrintifyOperator should:

1. Open a **new** Printify shop titled `SIDESHOT`.
2. Upload print files to `POST /v1/uploads/images.json` (see `print_areas[].art_spec`).
3. `POST /v1/shops/{shop_id}/products.json` as **drafts** using the variant IDs and `printify_price_cents` in the catalog.
4. Confirm live print cost in the editor (variants endpoint does not return unit print cost).
5. Publish only after gates 1–4. Do not hang merch checkout off the SafeShot CTA.

## Art (placeholder until SMI-151)

| SKU | File | Notes |
|---|---|---|
| Tee front | 4500×5400 PNG, transparent | White **SIDESHOT** + red **Start the Side Quest** |
| Hat front | 1200×675, 2 thread colors | Wordmark only. No photos. |
| Koozie wrap | 1425×3300 | Black field, red-orange lockup, small 21+ on the seam |

Do not invent can / SafeShot photography. If Joseph drops the existing brand pack, swap files and keep the same SKUs.

## Economics (planning, not a quote)

| SKU | Print band (USD) | US ship 1st / addl | Standalone note |
|---|---|---|---|
| Tee | $14–18 (confirm in editor) | $3.99 / $2.09 | Clears ~40% after ship at $32 |
| Hat | $15–21 (public from EUR 18.23) | $4.49 / $2.09 | Tighter; $30 is the floor |
| Koozie | $4–5 (public from EUR 3.93) | $5.39 / $0.89 | Bundle. Do not discount under $14 |

## Site

This repo is the task tracker, not the live site. [https://sideshot-beer.vercel.app/shop](https://sideshot-beer.vercel.app/shop) is 404. A merch grid ships only after Vercel+GitHub ([SMI-149](https://linear.app/smileing-goats/issue/SMI-149/connect-vercel-github-so-founder-agent-can-ship-site-changes)) and must stay below SafeShot.
