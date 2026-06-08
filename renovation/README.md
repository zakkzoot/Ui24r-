# Renovation — Max-ROI Refresh (no construction)

**⬇ [`Renovation_Plan.pdf`](Renovation_Plan.pdf)** — full deliverable in one file (cover, mood board, all before/after boards, written plan + ROI).

Virtual restyle of the apartment to lift rental value with minimal spend.

- **`RENOVATION_PLAN.md`** — strategy, room-by-room moves, budget & ROI.
- **`moodboard/moodboard.png`** — palette, materials, strategy, budget board.
- **`renders/compare_*.jpg`** — labelled **before / after** for 4 rooms.
- **`renders/reno_*.jpg`** — the restyled "after" images.
- **`originals/`** — source listing photos.
- **`restyle.py` · `compare.py` · `moodboard.py`** — generators (Python + Pillow).

The "after" images are concept visualisations: curtains, upholstery and
bedding were recoloured to a cohesive neutral palette and the photos
brightened, simulated directly from the listing photos. Re-run with:

```bash
pip install pillow numpy
python3 restyle.py && python3 compare.py && python3 moodboard.py && python3 build_pdf.py
```
