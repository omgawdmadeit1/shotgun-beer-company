"""SS-001 SafeShot Rev A0 — single source of dimensions (millimeters).

Shop-quote geometry for SIDESHOT Phase 1: punch + bottle opener + tab lifter.
Do not add a drinking tube (Wild Man / Krak'in prior art).
"""

from __future__ import annotations

from typing import TypedDict


class Dims(TypedDict):
    part_number: str
    revision: str
    title: str
    units: str
    material: str
    length: float
    width: float
    thick: float
    body_corner_r: float
    keyring_d: float
    keyring_from_end: float
    punch_d: float
    punch_from_end: float
    punch_shank: float
    punch_cone: float
    punch_tip_d: float
    punch_tip_r: float
    punch_root_fillet: float
    opener_hole_d: float
    opener_hole_x: float
    opener_slot_len: float
    opener_slot_w: float
    hook_len: float
    hook_w: float
    lifter_run: float
    lifter_tip_thick: float
    default_tol: float
    qty_primary: int
    qty_bid: int


DIMS: Dims = {
    "part_number": "SS-001",
    "revision": "A0",
    "title": "SafeShot Multi-Tool",
    "units": "mm",
    "material": "6061-T6 Aluminum",
    "length": 82.0,
    "width": 26.0,
    "thick": 6.35,
    "body_corner_r": 4.0,
    "keyring_d": 6.5,
    "keyring_from_end": 8.0,
    "punch_d": 11.0,
    "punch_from_end": 12.0,
    "punch_shank": 6.5,
    "punch_cone": 3.2,
    "punch_tip_d": 2.5,
    "punch_tip_r": 0.50,
    "punch_root_fillet": 1.0,
    "opener_hole_d": 14.0,
    "opener_hole_x": -2.0,
    "opener_slot_len": 12.0,
    "opener_slot_w": 8.0,
    "hook_len": 2.2,
    "hook_w": 7.0,
    "lifter_run": 14.0,
    "lifter_tip_thick": 1.60,
    "default_tol": 0.13,
    "qty_primary": 50,
    "qty_bid": 200,
}


def keyring_x(d: Dims = DIMS) -> float:
    return -d["length"] / 2.0 + d["keyring_from_end"]


def punch_x(d: Dims = DIMS) -> float:
    return d["length"] / 2.0 - d["punch_from_end"]


def punch_projection(d: Dims = DIMS) -> float:
    return d["punch_shank"] + d["punch_cone"]


def expected_bbox(d: Dims = DIMS) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Axis-aligned bbox (min, max) for X, Y, Z in mm."""
    half_l = d["length"] / 2.0
    half_w = d["width"] / 2.0
    half_t = d["thick"] / 2.0
    z_min = -half_t - punch_projection(d)
    return ((-half_l, half_l), (-half_w, half_w), (z_min, half_t))
