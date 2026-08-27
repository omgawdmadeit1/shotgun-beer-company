# SS-001 SafeShot CAD generator

Parametric CadQuery model. One dimension table (`safeshot_dims.py`) drives the solid, STEP, DXF, and PDF.

```bash
pip install -r requirements.txt
python3 generate_safeshot.py
python3 render_views.py
python3 generate_drawing.py
python3 test_safeshot_cad.py
```

Exports land in `exports/`. Do not hand-edit STEP/PDF — change dims and regenerate.
