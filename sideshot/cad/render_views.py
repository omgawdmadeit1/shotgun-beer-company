#!/usr/bin/env python3
"""Orthographic PNG previews from the exported STL (verification only)."""

from __future__ import annotations

import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from generate_safeshot import EXPORT_DIR, STEM


def read_stl_triangles(path: Path) -> list[tuple[tuple[float, float, float], ...]]:
    data = path.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:200]:
        raise ValueError("ASCII STL not supported")
    count = struct.unpack_from("<I", data, 80)[0]
    tris: list[tuple[tuple[float, float, float], ...]] = []
    offset = 84
    for _ in range(count):
        nums = struct.unpack_from("<12fH", data, offset)
        v1 = (nums[3], nums[4], nums[5])
        v2 = (nums[6], nums[7], nums[8])
        v3 = (nums[9], nums[10], nums[11])
        tris.append((v1, v2, v3))
        offset += 50
    return tris


def render(tris: list[tuple[tuple[float, float, float], ...]], elev: float, azim: float, dest: Path) -> None:
    fig = plt.figure(figsize=(6, 4.5), dpi=140)
    ax = fig.add_subplot(111, projection="3d")
    mesh = Poly3DCollection(tris, alpha=1.0)
    mesh.set_facecolor("#d8d8d8")
    mesh.set_edgecolor("#222222")
    mesh.set_linewidth(0.05)
    ax.add_collection3d(mesh)
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    ax.auto_scale_xyz(xs, ys, zs)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.tight_layout(pad=0.1)
    fig.savefig(dest, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    stl = EXPORT_DIR / f"{STEM}.stl"
    tris = read_stl_triangles(stl)
    render(tris, 90, -90, EXPORT_DIR / f"{STEM}_view_top.png")
    render(tris, 0, -90, EXPORT_DIR / f"{STEM}_view_front.png")
    render(tris, 0, 0, EXPORT_DIR / f"{STEM}_view_right.png")
    render(tris, 22, -55, EXPORT_DIR / f"{STEM}_view_iso.png")
    print(f"rendered {len(tris)} triangles")


if __name__ == "__main__":
    main()
