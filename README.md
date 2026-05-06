# Celestial Chase

> *Stranded light-years from home, your only way back is written in the stars. Decode the cosmos before time runs out.*

A three-level astronomy + computer-vision coding challenge built for the CASH scavenger hunt. Each level fuses the `ephem` astronomy library with `cv2` image processing: students must read pixel data from an embedded star image **and** compute real celestial mechanics, then combine both to recover a transposition / Caesar key.

---

## Overview

Each student receives a unique challenge code (0–19) which determines:
- Their **secret word** for each level (`random.seed(code + level)` → `random.choice(words)`)
- Their **embedded image** — backgrounds, decoys, and noise are seeded per user
- Their **encoded signal** — built from the word using a key derived from real astronomy

All students share the same observation date (`2025/6/21 12:00:00 UTC`) and location (Zurich, lat `47.3769`, lon `8.5417`), so every notebook computes against the same astronomical reality. Students never see their challenge code — everything they need is embedded in the notebook.

---

## Levels

### LVL 1 — The Teal Beacon
**Theme:** You've just woken from cryo-sleep. One star glows different from the rest — *teal*.

**Image:** 400×400 starfield with a unique random background per user. Venus is marked as a 5-pixel cyan cross (BGR `[255, 255, 0]`) at its actual sky position. Several decoy near-cyan pixels are added with `R ∈ [1, 30]` so a naïve "find any cyan-ish pixel" search fails.

**Task:**
1. Find the cyan pixel (`B == 255 and G == 255 and R == 0` — decoys have `R > 0`).
2. Compute Venus's phase with `ephem` for the given date.
3. Build the key: `key = pixel_x * pixel_y + int(venus.phase)`.
4. Reconstruct the permutation with `random.Random(key).shuffle(...)` and reverse the transposition.

**Skills:** `cv2` pixel filtering, basic `ephem` body computation, transposition cipher, seeded RNG reconstruction.

---

### LVL 2 — Ghost Stars
**Theme:** The Astrophage trail leads deeper. Four planets. Four signals. None of them quite white.

**Image:** 600×600 nebula with per-user unique blobs and background stars. Four planets (Mars, Jupiter, Saturn, Mercury) are marked as 3×3 near-white patches at their sky positions. Each marker's **blue channel** encodes that planet's earth-distance (`int(planet.earth_distance * 1000) % 255`). Pure-white 3×3 decoy patches are added — students filter `B != 255` to discard them.

**Task:**
1. Find all near-white 3×3 clusters with `cv2` and locate each cluster's centre.
2. Read each centre's blue channel.
3. Compute each planet's altitude with `ephem`.
4. Match each cluster to its planet via the position formula `(x = az/360 * W, y = (90 - alt)/180 * H)`.
5. Build the key: `key = sum(blue_channel[i] + int(alt_deg[i]) for each planet)`.
6. Decode the transposition.

**Skills:** cluster detection (`scipy.ndimage.label` or manual), BGR colour-channel reading, multi-body `ephem` computation, position-based matching, key combination.

---

### LVL 3 — The Star Chart
**Theme:** Alone, 40 light-years from Earth. Mission control's final message was written in the stars themselves.

**Image:** 800×800 chart showing 15 named bright stars (Sirius, Canopus, Arcturus, Vega, Capella, Rigel, Procyon, Betelgeuse, Altair, Aldebaran, Antares, Spica, Pollux, Fomalhaut, Deneb) at their actual sky positions, all labelled. The top-N stars by altitude (where N = `len(secret_word)`) are message-bearers — each has a red-channel value `R ∈ [28, 227]` encoding a Caesar shift. Dim-red decoy pixels (`R ∈ [1, 27]`) are scattered as noise.

**Task:**
1. Compute az/alt for all 15 named stars with `ephem`.
2. Sort by altitude descending; take the top N.
3. For each top-N star, find its pixel in the chart and read the red channel (filter `B == 0 and G == 0 and R >= 28` to discard decoys).
4. Reverse the per-letter Caesar shifts: `decoded[i] = (encoded[i] - red_channels[i]) % 26`.

**Skills:** named-star catalog usage, sorting + ranking, per-letter Caesar cipher, full image-to-text decoding pipeline.

---

## Setup

### Requirements
```bash
pip install ephem nbformat opencv-python numpy scipy ipython
```

`scipy` is needed for the L2 master solution's cluster labelling. The L1 and L3 solutions only require the core stack.

### Generate notebooks
```bash
python celestialchase.py
```

This generates, for each level:
- 20 student notebooks: `celestialchase_lvl{N}_0.ipynb` … `_19.ipynb`
- 1 master solution: `celestialchase_lvl{N}_solution.ipynb`

All output goes to `notebooks/celestialchase/`.

---

## How challenge codes drive variation

| What varies | How |
|---|---|
| Secret word | `random.seed(code + level)` → `random.choice(words)` |
| Image background | `np.random.RandomState(code * K + M)` per level — unique star count, blob positions, decoy count |
| Encoded signal | Transposition (L1, L2) or per-letter Caesar (L3), keyed by astronomy + pixel data |

The *astronomy* is fixed (everyone observes from Zurich on 2025-06-21), but the *image presentation* and *secret word* differ per user. This means students cannot share solutions — even though the underlying astronomical computation is identical.

---

## File structure

```
celestialchase.py                         — challenge generator
notebooks/
  celestialchase/
    celestialchase_lvl1_0.ipynb           — student notebook, code 0, level 1
    celestialchase_lvl1_1.ipynb
    ...
    celestialchase_lvl3_19.ipynb
    celestialchase_lvl1_solution.ipynb    — master solution (level 1)
    celestialchase_lvl2_solution.ipynb
    celestialchase_lvl3_solution.ipynb
```

---

## LLM-resistance design

Each level requires **both** computer-vision **and** astronomy, combined into a single key. An LLM cannot:
- Read the embedded base64 image without executing `cv2.imdecode`
- Compute Venus's phase or Jupiter's altitude without running `ephem`
- Pattern-match the encoded word to its solution because the cipher key changes per user

A student must actually run `ephem` *and* actually inspect pixel values; reasoning alone won't recover the key.

---

## Customisation

| What | Where |
|---|---|
| Word list | `words = [...]` near top of `celestialchase.py` |
| Observation location | `OBS_LAT`, `OBS_LON` |
| Observation date | `OBS_DATE` |
| Stars used in L3 | `STAR_NAMES` inside `generate_notebook_lvl3` |
| Planets used in L2 | `planet_names` inside `generate_notebook_lvl2` |
| Number of student variants | `for i in range(20)` in `__main__` |
