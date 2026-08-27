#!/usr/bin/env python3
"""Validate the locked Phase 1 Printify SKU catalog (SMI-150)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CATALOG_PATH = Path(__file__).with_name("phase1-sku-catalog.json")
REQUIRED_SKUS = ("SS-TEE-01", "SS-HAT-01", "SS-KOO-01")
FORBIDDEN_SHOPS = {20002621, 27582906}
REQUIRED_BLUEPRINTS = {
    "SS-TEE-01": 12,
    "SS-HAT-01": 1447,
    "SS-KOO-01": 951,
}
REQUIRED_VARIANTS = {
    "SS-TEE-01": {18100, 18101, 18102, 18103, 18104, 18105},
    "SS-HAT-01": {105372},
    "SS-KOO-01": {78460},
}


def load_catalog(path: Path = CATALOG_PATH) -> dict:
    return json.loads(path.read_text())


def validate(catalog: dict) -> list[str]:
    errors: list[str] = []

    if catalog.get("publish_blocked") is not True:
        errors.append("publish_blocked must be true until waitlist + SafeShot + dedicated shop + art")
    if catalog.get("status") != "sku_list_locked_do_not_publish":
        errors.append("status must remain sku_list_locked_do_not_publish for this packet")

    footer = catalog.get("compliance_footer") or ""
    if "21+" not in footer or "Drink responsibly" not in footer:
        errors.append("compliance_footer must include 21+ and Drink responsibly")

    blocked_shops = {int(s["id"]) for s in catalog.get("do_not_use_shops") or []}
    missing_shops = FORBIDDEN_SHOPS - blocked_shops
    if missing_shops:
        errors.append(f"do_not_use_shops missing {sorted(missing_shops)}")

    skus = catalog.get("skus") or []
    ids = [s.get("sku") for s in skus]
    if ids != list(REQUIRED_SKUS):
        errors.append(f"locked SKU order/set must be {REQUIRED_SKUS}, got {ids}")

    for sku in skus:
        code = sku.get("sku")
        desc = (sku.get("description") or "") + " " + (sku.get("listing_title") or "")
        if "21+" not in desc:
            errors.append(f"{code} listing/description missing 21+")
        if sku.get("blueprint_id") != REQUIRED_BLUEPRINTS.get(code):
            errors.append(f"{code} blueprint_id must be {REQUIRED_BLUEPRINTS.get(code)}")
        enabled = set(sku.get("enabled_variant_ids") or [])
        expected = REQUIRED_VARIANTS.get(code) or set()
        if enabled != expected:
            errors.append(f"{code} enabled_variant_ids {enabled} != {expected}")
        prices = sku.get("printify_price_cents") or {}
        for vid in expected:
            if str(vid) not in {str(k) for k in prices}:
                errors.append(f"{code} missing printify_price_cents for variant {vid}")
            else:
                cents = int(prices[str(vid)])
                if cents < 1400:
                    errors.append(f"{code} variant {vid} retail {cents} cents is below the $14 floor")
        if not sku.get("print_areas"):
            errors.append(f"{code} missing print_areas")
        if "SIDESHOT" not in (sku.get("title") or ""):
            errors.append(f"{code} title must carry SIDESHOT")
        if "Side Quest" not in (sku.get("title") or "") and "Side Quest" not in (
            sku.get("listing_title") or ""
        ):
            errors.append(f"{code} must carry Side Quest language")

    return errors


def main() -> int:
    catalog = load_catalog()
    errors = validate(catalog)
    if errors:
        print("CATALOG INVALID")
        for err in errors:
            print(f"- {err}")
        return 1
    print("CATALOG OK")
    print(f"skus: {', '.join(s['sku'] for s in catalog['skus'])}")
    print("publish_blocked: true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
