#!/usr/bin/env python3
"""ASME-style shop PDF for SS-001 SafeShot Rev A0. Dimensions match safeshot_dims."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from generate_safeshot import EXPORT_DIR, STEM
from safeshot_dims import DIMS, Dims, keyring_x, punch_projection, punch_x

PDF_PATH = EXPORT_DIR / f"{STEM}.pdf"


def _title_block(c: canvas.Canvas, w: float, h: float, d: Dims) -> None:
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.rect(8 * mm, 8 * mm, w - 16 * mm, h - 16 * mm)
    c.setLineWidth(0.4)
    c.rect(8 * mm, 8 * mm, w - 16 * mm, 28 * mm)
    c.line(w - 95 * mm, 8 * mm, w - 95 * mm, 36 * mm)
    c.line(w - 95 * mm, 22 * mm, w - 8 * mm, 22 * mm)
    c.line(w - 50 * mm, 8 * mm, w - 50 * mm, 36 * mm)
    c.setFont("Helvetica", 7)
    c.drawString(10 * mm, 32 * mm, "SIDESHOT BEER CO.  |  PHASE 1 TOOL  |  SMI-153")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(10 * mm, 24 * mm, d["title"].upper())
    c.setFont("Helvetica", 8)
    c.drawString(10 * mm, 18 * mm, f"P/N {d['part_number']}   REV {d['revision']}   2026-08-27")
    c.drawString(10 * mm, 13 * mm, f"MATERIAL: {d['material']}    UNITS: MILLIMETRES    THIRD ANGLE")
    c.setFont("Helvetica", 7)
    c.drawString(w - 93 * mm, 32 * mm, "QTY (QUOTE)")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(w - 93 * mm, 25 * mm, f"{d['qty_primary']}  +  bid {d['qty_bid']}")
    c.setFont("Helvetica", 7)
    c.drawString(w - 48 * mm, 32 * mm, "PROCESS")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(w - 48 * mm, 25 * mm, "CNC MILL")
    c.setFont("Helvetica", 7)
    c.drawString(w - 93 * mm, 18 * mm, "FINISH")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(w - 93 * mm, 11 * mm, "AS-MACHINED / Type II black")
    c.drawString(w - 48 * mm, 18 * mm, "DEFAULT TOL")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(w - 48 * mm, 11 * mm, f"±{d['default_tol']:.2f}  (ISO 2768-m)")


def _notes(c: canvas.Canvas, d: Dims) -> None:
    notes = [
        "1. INTERPRET PER ASME Y14.5-2018. SINGLE SOLID. NO THREADS. NO BENDS.",
        "2. BREAK SHARP EDGES 0.2–0.4 EXCEPT PUNCH TIP AND OPENER HOOK WORKING EDGES.",
        "3. PUNCH TIP Ø2.50 WITH R0.50 MIN — CONTROLLED BLUNT. DO NOT SHARPEN TO A NEEDLE.",
        "4. PUNCH CREATES ~Ø11 CLEAN ROUND HOLE IN 12 oz ALUMINUM CAN WALL (0.10 mm TYP).",
        "5. BOTTLE OPENER: Ø14 WINDOW + 2.2 HOOK LIP FOR CROWN CAP. TAB LIFTER: 14 WEDGE TO 1.60 TIP.",
        "6. FIRST ARTICLE AS-MACHINED. PRODUCTION: TYPE II CLASS 2 BLACK ANODIZE (QUOTE BOTH).",
        "7. OPTIONAL 2nd OP: LASER MARK “SIDESHOT” + “21+” ON TOP FACE. NOT IN SOLID.",
        "8. DO NOT ADD TUBE / STRAW / DRINKING-CHANNEL FEATURES (PRIOR ART / LIABILITY).",
        "9. THIS IS A BEVERAGE ACCESSORY. NOT A WEAPON. 21+ USE ONLY AFTER PRODUCT-LIABILITY COVER.",
        "10. UPLOAD THIS PDF + THE STEP TO XOMETRY AND eMACHINESHOP. FOUNDER SENDS RFQ — NO INVENTED QUOTES.",
    ]
    c.setFont("Helvetica", 6.4)
    y = 38 * mm
    for line in notes:
        c.drawString(10 * mm, y, line)
        y += 3.3 * mm


def _dim(c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float, text: str, offset: float) -> None:
    c.setStrokeColorRGB(0.1, 0.1, 0.1)
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(0.3)
    c.setFont("Helvetica", 7)
    if abs(y1 - y2) < 0.2:
        y = y1 + offset
        c.line(x1, y1, x1, y)
        c.line(x2, y2, x2, y)
        c.line(x1, y, x2, y)
        c.drawCentredString((x1 + x2) / 2.0, y + 1.4, text)
    else:
        x = x1 + offset
        c.line(x1, y1, x, y1)
        c.line(x2, y2, x, y2)
        c.line(x, y1, x, y2)
        c.saveState()
        c.translate(x + 1.6, (y1 + y2) / 2.0)
        c.rotate(90)
        c.drawCentredString(0, 0, text)
        c.restoreState()


def _draw_top(c: canvas.Canvas, ox: float, oy: float, scale: float, d: Dims) -> None:
    L, W = d["length"] * scale, d["width"] * scale
    r = d["body_corner_r"] * scale
    c.setLineWidth(0.7)
    c.roundRect(ox, oy, L, W, r, stroke=1, fill=0)
    kx = ox + (keyring_x(d) + d["length"] / 2.0) * scale
    ky = oy + W / 2.0
    c.circle(kx, ky, (d["keyring_d"] / 2.0) * scale, stroke=1, fill=0)
    hx = ox + (d["opener_hole_x"] + d["length"] / 2.0) * scale
    c.circle(hx, ky, (d["opener_hole_d"] / 2.0) * scale, stroke=1, fill=0)
    slot_cx = hx - (d["opener_hole_d"] / 2.0 + d["opener_slot_len"] / 2.0 - 1.5) * scale
    sl, sw = d["opener_slot_len"] * scale, d["opener_slot_w"] * scale
    c.roundRect(slot_cx - sl / 2.0, ky - sw / 2.0, sl, sw, sw / 2.0, stroke=1, fill=0)
    hook_x = hx + (d["opener_hole_d"] / 2.0 - d["hook_len"]) * scale
    c.rect(hook_x, ky - (d["hook_w"] / 2.0) * scale, d["hook_len"] * scale, d["hook_w"] * scale, stroke=1, fill=0)
    px = ox + (punch_x(d) + d["length"] / 2.0) * scale
    c.setDash(1, 1)
    c.circle(px, ky, (d["punch_d"] / 2.0) * scale, stroke=1, fill=0)
    c.setDash()
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ox, oy + W + 6, "TOP")
    _dim(c, ox, oy, ox + L, oy, f"{d['length']:.1f}", -8)
    _dim(c, ox, oy, ox, oy + W, f"{d['width']:.1f}", -8)
    _dim(c, px - (d["punch_d"] / 2.0) * scale, oy + W, px + (d["punch_d"] / 2.0) * scale, oy + W, f"Ø{d['punch_d']:.1f} PUNCH", 8)
    _dim(c, kx - (d["keyring_d"] / 2.0) * scale, oy + W, kx + (d["keyring_d"] / 2.0) * scale, oy + W, f"Ø{d['keyring_d']:.1f}", 14)


def _draw_front(c: canvas.Canvas, ox: float, oy: float, scale: float, d: Dims) -> None:
    L = d["length"] * scale
    T = d["thick"] * scale
    proj = punch_projection(d) * scale
    r = d["body_corner_r"] * scale
    c.setLineWidth(0.7)
    c.rect(ox, oy + proj, L, T, stroke=1, fill=0)
    px = ox + (punch_x(d) + d["length"] / 2.0) * scale
    shank = d["punch_shank"] * scale
    cone = d["punch_cone"] * scale
    half = (d["punch_d"] / 2.0) * scale
    tip = (d["punch_tip_d"] / 2.0) * scale
    top = oy + proj
    c.line(px - half, top, px - half, top - shank)
    c.line(px + half, top, px + half, top - shank)
    c.line(px - half, top - shank, px - tip, top - shank - cone)
    c.line(px + half, top - shank, px + tip, top - shank - cone)
    c.line(px - tip, top - shank - cone, px + tip, top - shank - cone)
    c.line(ox, top, ox + d["lifter_run"] * scale, top)
    c.line(ox, top + T - d["lifter_tip_thick"] * scale, ox, top)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ox, oy + proj + T + 6, "FRONT")
    _dim(c, ox + L, top, ox + L, top + T, f"{d['thick']:.2f}", 8)
    _dim(c, px + half + 2, top, px + half + 2, top - proj, f"{punch_projection(d):.1f}", 10)
    c.setFont("Helvetica", 6)
    c.drawString(ox + 2, top + T - 8, f"R{d['body_corner_r']:.0f} CORNERS")
    _ = r


def _draw_right(c: canvas.Canvas, ox: float, oy: float, scale: float, d: Dims) -> None:
    W = d["width"] * scale
    T = d["thick"] * scale
    proj = punch_projection(d) * scale
    half = (d["punch_d"] / 2.0) * scale
    tip = (d["punch_tip_d"] / 2.0) * scale
    top = oy + proj
    c.setLineWidth(0.7)
    c.rect(ox, top, W, T, stroke=1, fill=0)
    cx = ox + W / 2.0
    shank = d["punch_shank"] * scale
    cone = d["punch_cone"] * scale
    c.line(cx - half, top, cx - half, top - shank)
    c.line(cx + half, top, cx + half, top - shank)
    c.line(cx - half, top - shank, cx - tip, top - shank - cone)
    c.line(cx + half, top - shank, cx + tip, top - shank - cone)
    c.line(cx - tip, top - shank - cone, cx + tip, top - shank - cone)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ox, top + T + 6, "RIGHT")
    _dim(c, cx - tip, oy, cx + tip, oy, f"Ø{d['punch_tip_d']:.2f}  R{d['punch_tip_r']:.2f}", -7)


def generate_pdf(path: Path = PDF_PATH, d: Dims = DIMS) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    page = landscape(A4)
    c = canvas.Canvas(str(path), pagesize=page)
    w, h = page
    c.setTitle(f"{d['part_number']} {d['title']} Rev {d['revision']}")
    c.setAuthor("SIDESHOT Beer Co.")
    _title_block(c, w, h, d)
    _notes(c, d)
    scale = 2.15
    _draw_top(c, 22 * mm, 118 * mm, scale, d)
    _draw_front(c, 22 * mm, 72 * mm, scale, d)
    _draw_right(c, 210 * mm, 72 * mm, scale, d)
    iso = EXPORT_DIR / f"{STEM}_view_iso.png"
    if iso.exists():
        c.drawImage(str(iso), 200 * mm, 118 * mm, width=80 * mm, height=55 * mm, preserveAspectRatio=True, mask="auto")
        c.setFont("Helvetica-Bold", 8)
        c.drawString(200 * mm, 175 * mm, "ISOMETRIC (REF)")
    c.setFont("Helvetica", 6)
    c.drawRightString(w - 10 * mm, h - 12 * mm, "SS-001 REV A0  |  QUOTE PACKAGE  |  NOT FOR CONSTRUCTION UNTIL FOUNDER RELEASE")
    c.showPage()
    c.save()
    magic = path.read_bytes()[:5]
    if magic != b"%PDF-":
        raise RuntimeError("PDF missing %PDF- header")
    return path


def main() -> None:
    dest = generate_pdf()
    print(dest)


if __name__ == "__main__":
    main()
