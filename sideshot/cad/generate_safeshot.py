#!/usr/bin/env python3
"""Build SS-001 SafeShot Rev A0 and export shop-ready CAD.

Exports a single-body STEP (AP214 via Open CASCADE), STL (geometry samples),
DXF (top section), and JSON metadata. PDF drawing is generated separately.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cadquery as cq

from safeshot_dims import DIMS, Dims, expected_bbox, keyring_x, punch_projection, punch_x

EXPORT_DIR = Path(__file__).resolve().parent / "exports"
STEM = f"{DIMS['part_number']}_SafeShot_Rev{DIMS['revision']}"


def _lifter_wedge(d: Dims) -> cq.Workplane:
    half_l = d["length"] / 2.0
    half_t = d["thick"] / 2.0
    tip_z = -half_t + (d["thick"] - d["lifter_tip_thick"])
    wedge = (
        cq.Workplane("XZ")
        .moveTo(-half_l, -half_t)
        .lineTo(-half_l + d["lifter_run"], -half_t)
        .lineTo(-half_l, tip_z)
        .close()
        .extrude(d["width"])
        .translate((0.0, -d["width"] / 2.0, 0.0))
    )
    return wedge


def _punch_solid(d: Dims) -> cq.Workplane:
    px = punch_x(d)
    half_t = d["thick"] / 2.0
    shank_end = -half_t - d["punch_shank"]
    tip_z = shank_end - d["punch_cone"]
    r_shank = d["punch_d"] / 2.0
    r_tip = d["punch_tip_d"] / 2.0
    punch = (
        cq.Workplane("XY")
        .workplane(offset=-half_t)
        .transformed(offset=(px, 0.0, 0.0))
        .circle(r_shank)
        .extrude(-d["punch_shank"])
    )
    cone = (
        cq.Workplane("XY")
        .workplane(offset=shank_end)
        .transformed(offset=(px, 0.0, 0.0))
        .circle(r_shank)
        .workplane(offset=-d["punch_cone"])
        .circle(r_tip)
        .loft(combine=True)
    )
    solid = punch.union(cone)
    try:
        solid = solid.faces("<Z").fillet(d["punch_tip_r"])
    except Exception as exc:  # noqa: BLE001 — fillet is optional shop note if kernel rejects
        print(f"warn: punch tip fillet skipped ({exc})", file=sys.stderr)
    return solid


def build_safeshot(d: Dims = DIMS) -> cq.Workplane:
    """Single manifold solid. Millimeter units. No assembly, no suppressed features."""
    body = cq.Workplane("XY").box(d["length"], d["width"], d["thick"])
    body = body.edges("|Z").fillet(d["body_corner_r"])

    body = (
        body.faces(">Z")
        .workplane()
        .center(keyring_x(d), 0.0)
        .hole(d["keyring_d"])
    )

    body = (
        body.faces(">Z")
        .workplane()
        .center(d["opener_hole_x"], 0.0)
        .hole(d["opener_hole_d"])
    )
    slot_x = d["opener_hole_x"] - d["opener_hole_d"] / 2.0 - d["opener_slot_len"] / 2.0 + 1.5
    body = (
        body.faces(">Z")
        .workplane()
        .center(slot_x, 0.0)
        .slot2D(d["opener_slot_len"], d["opener_slot_w"], 0)
        .cutThruAll()
    )

    hook_x = d["opener_hole_x"] + d["opener_hole_d"] / 2.0 - d["hook_len"] / 2.0
    hook = (
        cq.Workplane("XY")
        .transformed(offset=(hook_x, 0.0, 0.0))
        .box(d["hook_len"], d["hook_w"], d["thick"])
    )
    body = body.union(hook)
    body = body.cut(_lifter_wedge(d))

    part = body.union(_punch_solid(d))
    try:
        part = part.edges(cq.NearestToPointSelector((punch_x(d), 0.0, -d["thick"] / 2.0))).fillet(
            d["punch_root_fillet"]
        )
    except Exception as exc:  # noqa: BLE001
        print(f"warn: punch root fillet skipped ({exc})", file=sys.stderr)

    solids = part.val().Solids()
    if len(solids) != 1:
        raise RuntimeError(f"expected 1 solid, got {len(solids)} — quoting engines reject multi-body")
    return part


def solid_metrics(part: cq.Workplane) -> dict[str, float | int]:
    solid = part.val()
    bbox = solid.BoundingBox()
    volume = float(solid.Volume())
    density_g_mm3 = 0.00270  # 6061-T6
    return {
        "xmin": round(bbox.xmin, 3),
        "xmax": round(bbox.xmax, 3),
        "ymin": round(bbox.ymin, 3),
        "ymax": round(bbox.ymax, 3),
        "zmin": round(bbox.zmin, 3),
        "zmax": round(bbox.zmax, 3),
        "volume_mm3": round(volume, 2),
        "mass_g_6061": round(volume * density_g_mm3, 2),
        "solid_count": 1,
    }


def assert_quote_ready(part: cq.Workplane, d: Dims = DIMS) -> dict[str, float | int]:
    metrics = solid_metrics(part)
    (xlo, xhi), (ylo, yhi), (zlo, zhi) = expected_bbox(d)
    tol = 1.25
    checks = {
        "xmin": (metrics["xmin"], xlo),
        "xmax": (metrics["xmax"], xhi),
        "ymin": (metrics["ymin"], ylo),
        "ymax": (metrics["ymax"], yhi),
        "zmin": (metrics["zmin"], zlo),
        "zmax": (metrics["zmax"], zhi),
    }
    for name, (got, want) in checks.items():
        if abs(float(got) - want) > tol:
            raise AssertionError(f"{name} {got} not within {tol} mm of {want}")
    if not (5000.0 < float(metrics["volume_mm3"]) < 20000.0):
        raise AssertionError(f"volume {metrics['volume_mm3']} mm3 outside expected range")
    return metrics


def export_all(part: cq.Workplane, out_dir: Path = EXPORT_DIR) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "step": out_dir / f"{STEM}.step",
        "stl": out_dir / f"{STEM}.stl",
        "dxf": out_dir / f"{STEM}_top.dxf",
        "json": out_dir / f"{STEM}_metrics.json",
    }
    cq.exporters.export(part, str(paths["step"]))
    cq.exporters.export(part, str(paths["stl"]))
    section = part.section(0.0)
    cq.exporters.export(section, str(paths["dxf"]))
    header = paths["step"].read_text(encoding="utf-8", errors="replace")[:80]
    if "ISO-10303-21" not in header:
        raise RuntimeError("STEP export missing ISO-10303-21 header")
    metrics = assert_quote_ready(part)
    payload = {
        "part_number": DIMS["part_number"],
        "revision": DIMS["revision"],
        "material": DIMS["material"],
        "units": "mm",
        "qty_primary": DIMS["qty_primary"],
        "qty_bid": DIMS["qty_bid"],
        "step_standard": "AP214 (Open CASCADE)",
        "single_body": True,
        "metrics": metrics,
    }
    paths["json"].write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SafeShot shop CAD")
    parser.add_argument("--out", type=Path, default=EXPORT_DIR)
    args = parser.parse_args()
    part = build_safeshot()
    written = export_all(part, args.out)
    print(json.dumps(written, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
