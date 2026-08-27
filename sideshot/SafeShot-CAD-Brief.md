# SafeShot CAD Brief — SS-001 Rev A0

**Status:** Quote-ready geometry locked 2026-08-27 (SMI-153).  
**Replaces:** missing founder-machine brief at `/workspace/sideshot/SafeShot-CAD-Brief.md` (written 21 Aug 2026, not in this repo).

## Product

SIDESHOT SafeShot™ — Phase 1 revenue tool. **Punch + bottle opener + tab lifter.**  
Clean round side hole for shotgunning a standard 12 oz aluminum can. Pocket / keychain form.

**Do not add** a drinking tube, straw, or flow channel (Wild Man / Krak'in prior art + Delaware litigation). Can-maker NRE is Phase 3 — out of scope.

## Locked geometry (mm)

| Feature | Value |
| --- | --- |
| Overall body | 82.0 × 26.0 × 6.35 |
| Corner radii | R4.0 |
| Punch | Ø11.0, 9.7 projection (6.5 shank + 3.2 cone) |
| Punch tip | Ø2.50 with R0.50 min (controlled blunt — not a needle) |
| Bottle opener | Ø14.0 window + 2.2 × 7.0 hook lip |
| Tab lifter | 14.0 wedge to 1.60 tip thickness |
| Keyring | Ø6.5, 8.0 from lifter end |
| Default tolerance | ±0.13 (ISO 2768-m) |

Single manifold solid. No threads. No bends. Units millimetres.

## Material / process / qty

- **Material:** 6061-T6 aluminum
- **Process:** CNC mill (3-axis, flip for punch)
- **Finish:** as-machined first article; quote Type II Class 2 black anodize as production alt
- **Qty:** **50** primary, also bid **200** (1000 is overseas zinc price-check only — after CAD lock, not this upload)
- **Mass (calc):** ~35.8 g
- **Optional 2nd op:** laser mark SIDESHOT + 21+ on top face (not in solid)

## Shop files

All generated from `sideshot/cad/` (CadQuery 2.8):

| File | Use |
| --- | --- |
| `cad/exports/SS-001_SafeShot_RevA0.step` | **Upload this** — AP214, single body |
| `cad/exports/SS-001_SafeShot_RevA0.pdf` | **Upload this** — dims, notes, qty |
| `cad/exports/SS-001_SafeShot_RevA0.stl` | 3D-print 5–20 geometry samples only |
| `cad/exports/SS-001_SafeShot_RevA0_top.dxf` | Reference 2D section |

Rebuild: `cd sideshot/cad && python3 generate_safeshot.py && python3 render_views.py && python3 generate_drawing.py && python3 test_safeshot_cad.py`

## Shop path (founder)

1. Review STEP in any free viewer (e.g. [Autodesk Viewer](https://viewer.autodesk.com/), [CAD Assistant](https://www.opencascade.com/products/cad-assistant/)).
2. Upload STEP + PDF to [Xometry](https://www.xometry.com/) Instant Quote and [eMachineShop](https://www.emachineshop.com/). See `SafeShot-Shop-Upload.md`.
3. Configure 6061-T6, CNC, qty 50, also 200. As-machined + anodize alt.
4. Paste real quotes back on SMI-147 / SMI-153. **Do not invent prices.**

Name flag (not a manufacturing stop): SAFESHOT is a live USPTO Class 6 mark (reg 8061021). Clearance on SMI-144.
