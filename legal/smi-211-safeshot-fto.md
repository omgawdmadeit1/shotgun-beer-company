# SMI-211 — SafeShot Freedom-to-Operate (Rev A0)

**Date:** 2026-08-27
**Part:** SS-001 SafeShot Multi-Tool, Rev A0
**CAD:** Linear attachment on [SMI-153](https://linear.app/smileing-goats/issue/SMI-153/commission-safeshot-cad-step-pdf-so-shops-can-quote) (`SS-001_SafeShot_RevA0.step`, AP214, single `MANIFOLD_SOLID_BREP`) + generator lock in the SIDESHOT task-tracker repo on branch `cursor/safeshot-cad-step-pdf-3af6`
**Parent:** [SMI-144](https://linear.app/smileing-goats/issue/SMI-144/trademark-search-and-filing-strategy-for-sideshot-safeshot)
**Unblocks:** [SMI-147](https://linear.app/smileing-goats/issue/SMI-147/safeshot-rfq-supplier-shortlist-for-first-50-200-units) RFQ metal

> **Not legal advice.** This is an operator claim chart against issued independent claims and the locked CAD. Counsel should sign off before first DTC shipment or if geometry changes. Literal infringement requires **every** element of a claim. Doctrine of equivalents still exists — stay off drink-through / slide / trigger / bottom-pivot architectures.

## Verdict

**Phase 1 SS-001 Rev A0 is on the clean path.**

The locked CAD is a **single-body rigid punch + crown-cap bottle opener + stay-on-tab lifter**. It does **not** literally read on:

| Patent | Owner | Expires (approx.) | Independent claim | SS-001 Rev A0 |
| --- | --- | --- | --- | --- |
| [US10,961,101 B2](https://patents.google.com/patent/US10961101B2/en) | Chug Co, LLC | ~2039-01-09 | Sliding piercing **tube** + **trigger latch** + **drink spout** / drink passage | **Miss** — solid punch, no tube, no trigger, no spout |
| [US11,731,868 B2](https://patents.google.com/patent/US11731868B2/en) | Wild Man Lab LLC | ~2042-05-13 | Bottom-pivot hook + curved pierce-and-drink + spout bore + shroud + flow apertures | **Miss** — no pivot-on-can-bottom, no spout, no shroud, no apertures |
| [US11,993,500 B2](https://patents.google.com/patent/US11993500B2/en) | Wild Man Lab LLC | ~2042-05-13 | Same family: pivot arm abutting can **bottom** + curved entry + drink-through bore | **Miss** — same gaps |

**Benson can patents** [US11,814,210](https://patents.google.com/patent/US11814210B2/en) / [US12,534,267](https://patents.google.com/patent/US12534267B2/en) do **not** hit Phase 1 **standard cans**. They only matter if we later add a twist-body + internal rod second mouth. Do not.

**Gate for RFQ:** send STEP + PDF as drawn. Do **not** add a sliding tube, trigger, drink-through spout, funnel, gasketed shroud, or bottom-pivot hook in any “v1.1.”

---

## 1. Accused article — SS-001 Rev A0 (what we actually have)

Source of truth: `sideshot/cad/safeshot_dims.py` + `generate_safeshot.py` on the CAD branch; STEP attached to SMI-153; metrics JSON:

| Feature | Locked value | FTO meaning |
| --- | --- | --- |
| Form | One manifold solid, 82.0 × 26.0 × 6.35 mm, 6061-T6 | No body-shell / sliding assembly |
| Solids | `solid_count: 1` | No tube-in-shell |
| Punch | Ø11.0 shank, 6.5 + 3.2 cone, Ø2.50 tip, R0.50 | **Solid** ogive. No central opening, no drink passage |
| Punch projection | 9.7 mm off the plate face | User punches the can, then **drinks from the can hole** |
| Bottle opener | Ø14.0 window + 2.2 × 7.0 hook lip + slot | Crown-cap **pry**, not a mouthpiece |
| Tab lifter | 14.0 mm wedge to 1.60 tip on the **keychain end** | Lifts a stay-on-tab. Does **not** hook a can bottom as a fulcrum |
| Keyring | Ø6.5 through-hole | Passive hole, not a Chug stow latch |
| Volume / mass | 13,260 mm³ / ~35.8 g | Pocket plate, not a Krak’in |

**Forbidden features confirmed absent in STEP / generator:**

- Sliding piercing tube
- Trigger / trigger latch / trigger opening / compression spring
- Drink-through spout, drink passage, central opening in the punch
- Can seal / gasket / shroud
- Bottom-pivot hook / fulcrum arm that engages the can bottom to drive a curved entry
- Flow-portion apertures
- Multi-body assembly

Use model (RFQ + CAD brief): punch sidewall → drink from the **side hole** → pop the top tab for vent. Tool is not a straw.

---

## 2. US10,961,101 B2 — Chug Co (Clark)

**Status:** Active. Assigned to Chug Co, LLC. Granted 2021-03-30. Anticipated expiration ~2039-01-09. 4th-year micro maintenance paid 2024-09-16.

**What it is:** A two-part shotgun tool: a **body shell** with a **passage** and **trigger opening**; a **piercing tube** that **slides** in that passage; a **drinking spout** at the distal end; a **drink passage** from a **central opening** in the piercing element to the spout; a **rotatable trigger latch** that holds the tube **armed**. Spring-driven pierce is claim 2.

### Claim 1 (independent) — element chart

| # | Claim element | SS-001 Rev A0 | Hit? |
| --- | --- | --- | --- |
| 1 | Body shell with outer wall, proximate end, distal end, **passage**, and **trigger opening** | Single plate. No shell, no internal passage, no trigger opening | No |
| 2 | **Piercing tube slidably positioned** within the passage | Punch is **unioned** to the plate. Cannot slide | No |
| 3 | First flange on the piercing tube | No flange, no sliding member | No |
| 4 | Piercing element with a **central opening** | Solid cone (Ø11 → Ø2.5). No lumen | No |
| 5 | Distal drinking spout; first Ø < second Ø < third Ø | Distal end is a keyring + tab wedge, not a spout; no stepped drink tube | No |
| 6 | **Drink passage** from central opening to spout | No through-path. Beverage never enters the tool | No |
| 7 | **Trigger latch rotatably coupled**, extends through trigger opening, abuts tube + flange in an **armed position** | No latch, no armed position | No |

**Literal: no.** Missing the entire slide / trigger / drink-through combination.

### Remaining claims

Claims 2–9 all depend on claim 1 (spring, whistle port, can seal, rim engagement, key-ring stow, internal ribs, latch-on-second-diameter). **None attach** if claim 1 misses.

The specification also recites a **method** of sliding the tube to armed, abutting the shell, sliding the tube through the shell, and funneling beverage through the drink passage. SS-001 is a push-punch, then mouth-on-can. Different method.

**Doctrine of equivalents (watch, not a hit):** arguing a solid punch “is” a tube, or a pry slot “is” a spout, is a stretch. Do not give them help by adding a hollow punch, a mouthpiece, or a spring/trigger “for safety.”

**Commercial cousins already on the clean path:** BeerShark, King Kobra, Chug Buddy metal 4-in-1 — punch + opener + tab, no tube. That market has been live for years next to this patent.

---

## 3. US11,731,868 B2 — Wild Man Lab (Widmann / Krak’in)

**Status:** Active. Assigned to Wild Man Lab LLC. Granted 2023-08-22. Adjusted expiration ~2042-05-13.

**What it is:** The Krak’in architecture. Pivot a **curved entry** into the can **sidewall** while a **pivot arm** hooks the **bottom** of the can as the fulcrum; drink through a **spout bore**; **shroud** sits against the wall; **plurality of flow apertures**.

### Claim 1 (independent) — element chart

| # | Claim element | SS-001 Rev A0 | Hit? |
| --- | --- | --- | --- |
| 1 | Spout comprising a **bore** | No spout. No bore | No |
| 2 | **Pivot arm** with a **curved portion that defines a fulcrum** | Tab-lifter wedge is on the opposite end of a flat plate. It is not a can-bottom fulcrum | No |
| 3 | **Shroud** extending from the spout | No shroud | No |
| 4 | **Entry portion** extending from the spout: flow portion with a **plurality of first apertures** + piercing portion | Punch is a solid cone with **zero** flow apertures | No |
| 5 | Pierces **as pivoted about the fulcrum with the pivot arm engaged with the can bottom** | Punch is a straight axial push, normal to the plate. No bottom engagement | No |
| 6 | Entry **curved downward toward the pivot arm** from shroud to piercing portion | Punch axis is straight (−Z). Not curved toward a hook | No |
| 7 | Piercing **and flow** portions **penetrate** the hole so liquid flows **into the bore** through the apertures | Liquid never enters the tool | No |
| 8 | Shroud proximate the sidewall when entry is in the hole | No shroud | No |

**Literal: no.**

### Remaining claims

2–20 are dependents (gasket, drink-via-spout, shroud concavity, gasket flaps/tabs, pivot-from-spout, aperture geometry, punch-tip-on-entry, polygonal / circular / elliptical **entry** cross-section, curved portion engages can bottom). All require claim 1. A circular **solid** punch is not a circular **entry portion with a flow portion and apertures**.

---

## 4. US11,993,500 B2 (US11,993,500 = 11,993,500) — Wild Man Lab continuation

**Status:** Active. Granted 2024-05-28. Same family / same inventor / same assignee.

**Claim 1** is the same drink-through + bottom-abut + curved entry combination, with the fulcrum language relaxed to: *“a pivot arm configured to abut a bottom surface of a beverage can”* (no “curved portion that defines a fulcrum” in the independent). Shroud, bore, plurality of apertures, curved-downward entry, drink-into-bore remain.

SS-001 still misses: spout/bore, pivot arm that abuts the **can bottom**, shroud, flow apertures, curved entry, drink-through.

**Literal: no.** Dependents (gasket, drink-via-spout, concave shroud, punch-on-entry, etc.) do not attach.

**Family watch (not in the SMI-211 must-map, do not copy):**

| Patent | Note |
| --- | --- |
| US11,518,663 | Earlier Wild Man utility — same pierce-and-drink / pivot architecture |
| USD1005777 | **Design** patent on Krak’in ornamental form. SS-001 is a flat 82×26 plate, not the Krak’in hook+spout silhouette. Keep finishes / colors / ads off orange-black Krak’in clones |
| US12,528,687 (cited 2026-01-20) | Later family member. Same architecture class. Re-check if we ever leave the rigid-punch path |

---

## 5. Litigation context (why we stay boring)

**Wild Man Lab LLC et al. v. Whaleco Inc. (d/b/a Temu), D. Del. 1:24-cv-00071**

- Filed 2024-01-18. Patents reported: 11,518,663; 11,731,868 (plus TM/copyright).
- Theory: Temu sold **Krak’in knockoffs** (same method, similar markings, orange/black).
- Terminated 2024-04-11 — stipulation of dismissal **with prejudice** (settlement; terms not public).

**Implication:** Wild Man enforces against **drink-through / pivot-hook clones**, not against BeerShark-class plates. They are live and will sue. Stay visually and mechanically off Krak’in. Do not sell a “SIDESHOT Krak” or add a funnel “for the 200-pc run.”

---

## 6. Benson cans (scope check only)

[US11,814,210](https://patents.google.com/patent/US11814210B2/en) / [US12,534,267](https://patents.google.com/patent/US12534267B2/en): twistable two-part can body + internal rod to a second mouth.

Phase 1 is **standard 12 oz cans + companion tool**. **No hit.**

Phase 2 custom can: extra score only (Langheinrich US20150183547A1 abandoned; US6,015,060 expired). Do **not** ship twist-body + internal rod.

---

## 7. What would put us back on the wrong path

Any of these on a later rev **reopens** this FTO:

1. Hollow punch / straw / funnel / mouthpiece
2. Tube that slides in a shell
3. Trigger, latch, or spring-fired pierce
4. Hook that seats on the **can bottom** so the tool pivots in
5. Gasketed shroud that seals to the sidewall for drink-through
6. Marketing that the user drinks **through the tool**
7. Krak’in-shaped CAD or orange/black clone ads (design + TM, even if utility is clear)
8. Benson second-mouth can

Tab-lifter language: it lifts the **stay-on-tab**. Never describe it as a “bottom hook,” “can hook,” or “fulcrum.”

---

## 8. RFQ / site holds (operator)

| Hold | Owner | Status after this memo |
| --- | --- | --- |
| Geometry lock | SMI-153 Rev A0 | **Cleared for quote** — do not change punch to hollow |
| First-run mark | SMI-144 / SMI-210 | Laser **SIDESHOT** only until SAFESHOT ITU is filed. Live Class 6 SAFESHOT (RN 8061021) is a different good; still keep the word off metal this run |
| Insurance | Founder | Bind product-liability **before** first DTC ship |
| Copy | Harper / site | “Cleaner round hole.” Do not claim “safer” as fact. Do not show drink-through |
| Counsel | Founder | Optional letter before scale / Amazon. Not a metal-RFQ blocker on this chart |

---

## 9. Sources

- USPTO / Google Patents: US10,961,101 B2; US11,731,868 B2; US11,993,500 B2; US11,814,210; US12,534,267
- Wild Man IP page: https://wildmandrinking.com/pages/ip
- D. Del. 1:24-cv-00071 docket (Justia / PacerMonitor) — filed 2024-01-18, dismissed with prejudice 2024-04-11
- SS-001 dims + generator + metrics on `cursor/safeshot-cad-step-pdf-3af6`
- SMI-153 Linear STEP attachment (Open CASCADE AP214, 2026-08-27)
- SMI-147 RFQ package (forbidden: drinking tube / funnel / mouthpiece)

---

## Next 3 actions for user

1. **Approve RFQ wave 1** on SMI-147 using this Rev A0 STEP + PDF (Xometry + eMachineShop). Do not wait for a counsel letter to *quote*.
2. **File SMI-209 + SMI-210** (SIDESHOT / SAFESHOT ITU) so the 50-pc run can eventually carry the tool mark.
3. **Bind liability insurance** and keep Harper off Krak’in-look ads. @Dr.Drop-it only if you want a different CAD (hollow punch, hook, tube) — that would reopen this issue.
