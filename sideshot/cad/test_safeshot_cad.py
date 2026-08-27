#!/usr/bin/env python3
"""Verify SS-001 quote package: single solid, STEP AP214, PDF, dims lock."""

from __future__ import annotations

import unittest
from pathlib import Path

from generate_drawing import generate_pdf
from generate_safeshot import STEM, build_safeshot, export_all, solid_metrics
from safeshot_dims import DIMS, expected_bbox, punch_projection

EXPORTS = Path(__file__).resolve().parent / "exports"


class SafeShotCadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.part = build_safeshot()
        cls.paths = export_all(cls.part, EXPORTS)
        generate_pdf(EXPORTS / f"{STEM}.pdf")

    def test_single_solid(self) -> None:
        self.assertEqual(len(self.part.val().Solids()), 1)

    def test_bbox_matches_locked_dims(self) -> None:
        metrics = solid_metrics(self.part)
        (xlo, xhi), (ylo, yhi), (zlo, zhi) = expected_bbox()
        self.assertAlmostEqual(metrics["xmin"], xlo, places=2)
        self.assertAlmostEqual(metrics["xmax"], xhi, places=2)
        self.assertAlmostEqual(metrics["ymin"], ylo, places=2)
        self.assertAlmostEqual(metrics["ymax"], yhi, places=2)
        self.assertAlmostEqual(metrics["zmin"], zlo, places=2)
        self.assertAlmostEqual(metrics["zmax"], zhi, places=2)
        self.assertAlmostEqual(punch_projection(), 9.7, places=2)

    def test_volume_and_mass_sane(self) -> None:
        metrics = solid_metrics(self.part)
        self.assertGreater(float(metrics["volume_mm3"]), 8000.0)
        self.assertLess(float(metrics["volume_mm3"]), 18000.0)
        self.assertGreater(float(metrics["mass_g_6061"]), 20.0)
        self.assertLess(float(metrics["mass_g_6061"]), 50.0)

    def test_step_is_ap214_single_file(self) -> None:
        step = Path(self.paths["step"]).read_text(encoding="utf-8", errors="replace")
        self.assertTrue(step.startswith("ISO-10303-21"))
        self.assertIn("AUTOMOTIVE_DESIGN", step)
        self.assertIn("10303 214", step)
        self.assertIn("MANIFOLD_SOLID_BREP", step)

    def test_pdf_has_shop_notes(self) -> None:
        from pypdf import PdfReader

        reader = PdfReader(str(EXPORTS / f"{STEM}.pdf"))
        text = reader.pages[0].extract_text() or ""
        for token in (
            "SS-001",
            "REV A0",
            "6061-T6",
            "50",
            "200",
            "XOMETRY",
            "eMACHINESHOP",
            "Ø11.0",
            "NO THREADS",
        ):
            self.assertIn(token, text)

    def test_dxf_and_stl_exist(self) -> None:
        self.assertGreater(Path(self.paths["stl"]).stat().st_size, 10_000)
        self.assertGreater(Path(self.paths["dxf"]).stat().st_size, 500)
        dxf = Path(self.paths["dxf"]).read_text(encoding="utf-8", errors="replace")
        self.assertIn("SECTION", dxf)


if __name__ == "__main__":
    unittest.main()
