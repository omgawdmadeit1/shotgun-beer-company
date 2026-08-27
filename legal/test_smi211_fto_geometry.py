#!/usr/bin/env python3
"""SMI-211 geometry lock: SS-001 Rev A0 must stay on the clean FTO path.

Reads the Linear/CAD STEP (AP214) and fails if the solid grows a sliding
tube, drink passage, or multi-body assembly. This is not a patent search —
it is a regression gate so RFQ metal cannot silently leave the claim chart.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEP_CANDIDATES = [
    ROOT / "legal" / "fixtures" / "SS-001_SafeShot_RevA0.step",
    ROOT / "sideshot" / "cad" / "exports" / "SS-001_SafeShot_RevA0.step",
    Path("/tmp/shotgun-beer-company/sideshot/cad/exports/SS-001_SafeShot_RevA0.step"),
]
METRICS_CANDIDATES = [
    ROOT / "legal" / "fixtures" / "SS-001_SafeShot_RevA0_metrics.json",
    ROOT / "sideshot" / "cad" / "exports" / "SS-001_SafeShot_RevA0_metrics.json",
    Path("/tmp/shotgun-beer-company/sideshot/cad/exports/SS-001_SafeShot_RevA0_metrics.json"),
]


def _first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.is_file():
            return path
    raise FileNotFoundError("missing SS-001 Rev A0 artifact: " + ", ".join(str(p) for p in paths))


def _first_optional(*paths: Path) -> Path | None:
    for path in paths:
        if path.is_file():
            return path
    return None


class SafeShotFtoGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.step_path = _first_existing(STEP_CANDIDATES)
        cls.metrics_path = _first_existing(METRICS_CANDIDATES)
        cls.step = cls.step_path.read_text(encoding="utf-8", errors="replace")
        cls.metrics = json.loads(cls.metrics_path.read_text(encoding="utf-8"))

    def test_step_is_ap214_single_manifold(self) -> None:
        self.assertTrue(self.step.startswith("ISO-10303-21"))
        self.assertIn("AUTOMOTIVE_DESIGN", self.step)
        self.assertIn("10303 214", self.step)
        self.assertEqual(self.step.count("MANIFOLD_SOLID_BREP"), 1)
        self.assertNotIn("NEXT_ASSEMBLY_USAGE_OCCURRENCE", self.step)

    def test_metrics_lock_single_body_bbox(self) -> None:
        self.assertTrue(self.metrics["single_body"])
        self.assertEqual(self.metrics["metrics"]["solid_count"], 1)
        self.assertEqual(self.metrics["part_number"], "SS-001")
        self.assertEqual(self.metrics["revision"], "A0")
        bbox = self.metrics["metrics"]
        self.assertAlmostEqual(float(bbox["xmin"]), -41.0, delta=0.05)
        self.assertAlmostEqual(float(bbox["xmax"]), 41.0, delta=0.05)
        self.assertAlmostEqual(float(bbox["ymin"]), -13.0, delta=0.05)
        self.assertAlmostEqual(float(bbox["ymax"]), 13.0, delta=0.05)
        # Punch projects ~9.7 mm off the 6.35 mm plate (zmin ≈ -12.875)
        self.assertLess(float(bbox["zmin"]), -12.0)
        self.assertGreater(float(bbox["zmin"]), -14.0)
        self.assertGreater(float(bbox["zmax"]), 3.0)
        self.assertLess(float(bbox["zmax"]), 4.0)

    def test_no_drink_through_or_slide_tokens_in_cad_lock(self) -> None:
        """Generator + brief on the CAD branch must keep the forbidden list."""
        brief = _first_optional(
            ROOT / "sideshot" / "SafeShot-CAD-Brief.md",
            Path("/tmp/shotgun-beer-company/sideshot/SafeShot-CAD-Brief.md"),
        )
        dims = _first_optional(
            ROOT / "sideshot" / "cad" / "safeshot_dims.py",
            Path("/tmp/shotgun-beer-company/sideshot/cad/safeshot_dims.py"),
        )
        gen = _first_optional(
            ROOT / "sideshot" / "cad" / "generate_safeshot.py",
            Path("/tmp/shotgun-beer-company/sideshot/cad/generate_safeshot.py"),
        )
        if brief is None or dims is None or gen is None:
            self.skipTest("CAD brief not checked out")
        text = brief.read_text(encoding="utf-8") + dims.read_text(encoding="utf-8") + gen.read_text(
            encoding="utf-8"
        )
        self.assertIn("Do not add a drinking tube", text)
        self.assertIn("single manifold solid", text.lower())
        for banned in (
            "drink passage",
            "drinking spout",
            "trigger latch",
            "piercing tube",
            "compression spring",
            "pivot arm",
            "bottom-pivot",
        ):
            self.assertNotIn(banned, text.lower())

    def test_punch_is_solid_cone_not_tube(self) -> None:
        gen = _first_optional(
            ROOT / "sideshot" / "cad" / "generate_safeshot.py",
            Path("/tmp/shotgun-beer-company/sideshot/cad/generate_safeshot.py"),
        )
        dims = _first_optional(
            ROOT / "sideshot" / "cad" / "safeshot_dims.py",
            Path("/tmp/shotgun-beer-company/sideshot/cad/safeshot_dims.py"),
        )
        if gen is None or dims is None:
            self.skipTest("CAD generator not checked out")
        source = gen.read_text(encoding="utf-8") + dims.read_text(encoding="utf-8")
        self.assertIn("circle(r_shank)", source)
        self.assertIn("circle(r_tip)", source)
        self.assertIn(".loft(", source)
        self.assertNotIn(".hole(d[\"punch", source)
        self.assertIn('"punch_d": 11.0', source)
        self.assertIn('"punch_tip_d": 2.5', source)


if __name__ == "__main__":
    unittest.main()
