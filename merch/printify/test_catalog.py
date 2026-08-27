#!/usr/bin/env python3
"""Tests for the SMI-150 Printify Phase 1 SKU catalog."""

import copy
import json
import unittest
from pathlib import Path

from validate_catalog import CATALOG_PATH, REQUIRED_SKUS, load_catalog, validate


class CatalogContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_file_is_valid_json(self):
        json.loads(CATALOG_PATH.read_text())

    def test_locked_catalog_passes(self):
        self.assertEqual(validate(self.catalog), [])

    def test_three_skus_tee_hat_koozie(self):
        types = [s["product_type"] for s in self.catalog["skus"]]
        self.assertEqual(types, ["tee", "hat", "koozie"])
        self.assertEqual([s["sku"] for s in self.catalog["skus"]], list(REQUIRED_SKUS))

    def test_does_not_publish_to_wall_art_shop(self):
        forbidden = {s["id"] for s in self.catalog["do_not_use_shops"]}
        self.assertIn(20002621, forbidden)
        self.assertTrue(self.catalog["publish_blocked"])

    def test_does_not_block_safeshot(self):
        self.assertIn("SafeShot", self.catalog["do_not_block"])
        self.assertIn("SMI-148", self.catalog["do_not_block"])

    def test_reject_if_publish_unblocked(self):
        bad = copy.deepcopy(self.catalog)
        bad["publish_blocked"] = False
        self.assertTrue(any("publish_blocked" in e for e in validate(bad)))

    def test_reject_missing_21_plus(self):
        bad = copy.deepcopy(self.catalog)
        bad["skus"][0]["description"] = "cool shirt"
        bad["skus"][0]["listing_title"] = "cool shirt"
        self.assertTrue(any("21+" in e for e in validate(bad)))

    def test_reject_wrong_blueprint(self):
        bad = copy.deepcopy(self.catalog)
        bad["skus"][2]["blueprint_id"] = 636
        self.assertTrue(any("blueprint_id" in e for e in validate(bad)))

    def test_art_specs_present(self):
        for sku in self.catalog["skus"]:
            spec = sku["print_areas"][0]["art_spec"]
            self.assertGreater(len(spec), 40)


if __name__ == "__main__":
    unittest.main()
