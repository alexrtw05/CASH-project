# Celestial Chase

> *Stranded light-years from home, your only way back is written in the stars. Decode the cosmos before time runs out.*

A three-level astronomy + computer-vision coding challenge built for the CASH scavenger hunt. Each level fuses the `ephem` astronomy library with `cv2` image processing: students must read pixel data from an embedded star image **and** compute real celestial mechanics, then combine both to recover a cipher key. The cipher progresses from a per-letter Caesar (L1) to an XOR-hex stream cipher (L2), and finally to an XOR-hex with a per-byte combined key (L3).

---

## Overview

Each student receives a unique challenge code (0–19) which determines:
- Their **secret word** for each level (`random.seed(code + level)` → `random.choice(words)`)
- Their **embedded image** — backgrounds, decoys, and noise are seeded per user
- Their **encoded signal** — built from the word using a key derived from astronomy + a per-image quantity

All students share the same observation date (`2025/6/21 12:00:00 UTC`) and location (Zurich, lat `47.3769`, lon `8.5417`), so every notebook computes against the same astronomical reality. Students never see their challenge code — everything they need is embedded in the notebook. Two students with the same secret word still produce different ciphertexts because each level mixes a per-image fingerprint into the key.

---

## Levels

### LVL 1 — The Teal Beacon
**Theme:** You've just woken from cryo-sleep. One star glows different from the rest — *teal*.

**Image:** 400×400 starfield with a unique random background per user. Venus is marked as a 5-pixel cyan cross (BGR `[255, 255, 0]`) at its actual sky position. Several decoy near-cyan pixels are added with `R ∈ [1, 30]` so a naïve "find any cyan-ish pixel" search fails.

**Cipher:** per-letter Caesar shift. Each letter at position `i` is shifted by `(shift_base + i*7) % 26`, where `shift_base = (pixel_x + pixel_y + venus_phase + decoy_sum) % 26`. The position-dependent `i*7` term means brute-forcing all 26 shifts on the whole word does *not* recover the plaintext.

**Task:**
1. Find the cyan pixel (`B == 255 and G == 255 and R == 0` — decoys have `R > 0`).
2. Sum the red-channel values of the decoy near-cyan pixels (`B == 255 and G == 255 and 0 < R < 50`) → `decoy_sum`.
3. Compute Venus's phase with `ephem` for the given date.
4. Build `shift_base` and reverse the per-letter Caesar.

**Skills:** `cv2` pixel filtering, mask reduction, basic `ephem` body computation, Caesar cipher with position-dependent shifts.

---

### LVL 2 — Ghost Stars
**Theme:** The Astrophage trail leads deeper. Four planets. Four signals. None of them quite white.

**Image:** 600×600 nebula with per-user unique blobs and background stars. Four planets (Mars, Jupiter, Saturn, Mercury) are marked as 3×3 near-white patches at their sky positions. Each marker's **blue channel** encodes that planet's earth-distance (`int(planet.earth_distance * 1000) % 255`). Pure-white 3×3 decoy clusters are added — students filter `B != 255` to find the real markers, and count the pure-white clusters separately.

**Cipher:** XOR stream cipher with hex output. Each plaintext byte is XOR'd with `(base_key + i*23) & 0xFF`, where `base_key = (planet_sum + decoy_count) & 0xFF`. The output is hex (e.g. `2d0a18fac4a6`) — visually opaque, no letter-frequency or anagram cues.

**Task:**
1. Find the four real planet markers and read each centre's blue channel.
2. Count the pure-white decoy clusters → `decoy_count` (use `scipy.ndimage.label`).
3. Compute each planet's altitude with `ephem`, match each cluster to its planet via the position formula.
4. Build `planet_sum = sum(blue_channel + altitude_deg for each planet)`.
5. Build `base_key` and XOR-decode the hex string byte-by-byte.

**Skills:** cluster detection, BGR colour-channel reading, multi-body `ephem` computation, position-based matching, byte/hex/XOR mechanics.

---

### LVL 3 — The Star Chart
**Theme:** Alone, 40 light-years from Earth. Mission control's final message was written in the stars themselves.

**Image:** 800×800 chart showing 15 named bright stars (Sirius, Canopus, Arcturus, Vega, Capella, Rigel, Procyon, Betelgeuse, Altair, Aldebaran, Antares, Spica, Pollux, Fomalhaut, Deneb) at their actual sky positions, all labelled. The top-N stars by altitude (where N = `len(secret_word)`) are message-bearers — each has a red-channel value `R ∈ [28, 227]` derived deterministically from `hashlib.md5(name + code)`. Dim-red decoy pixels (`R ∈ [1, 27]`) are scattered as noise.

**Cipher:** XOR-hex with a **per-byte combined key**. For position `i` in the message, the key byte is `(red_channel_i + altitude_deg_i) & 0xFF` where `i` indexes the i-th star in altitude rank. This is the hardest level: any single ranking error or missed pixel corrupts that byte and only that byte, so debugging is harder than a single-key cipher.

**Task:**
1. Compute az/alt for all 15 named stars with `ephem`.
2. Sort by altitude descending; take the top N.
3. For each top-N star, find its pixel in the chart and read the red channel (filter `B == 0 and G == 0 and R >= 28` to discard decoys).
4. For each byte of the hex message, compute `(red_channel_i + altitude_i) & 0xFF` and XOR-decode.

**Skills:** named-star catalog usage, ranking + ordering, per-byte combined-key XOR cipher, full image-to-text decoding pipeline.

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
| Encoded signal | Caesar (L1) or XOR-hex (L2, L3), keyed by astronomy + per-image fingerprint |
| L3 red channels | `hashlib.md5(star_name + code)` → deterministic across Python sessions |

The *astronomy* is fixed (everyone observes from Zurich on 2025-06-21), but the *image presentation* and *secret word* differ per user. Two students with the same secret word still get different ciphertexts because the per-image quantity (`decoy_sum`, `decoy_count`, `red_channels`) is mixed into the cipher key.

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

Each level requires **both** computer vision **and** astronomy, combined into a single key. An LLM cannot:
- Read the embedded base64 image without executing `cv2.imdecode`
- Compute Venus's phase or Jupiter's altitude without running `ephem`
- Pattern-match the encoded word to its solution because the cipher key changes per user

A student must actually run `ephem` *and* actually inspect pixel values; reasoning alone won't recover the key. L2 and L3's hex output also removes letter-frequency and anagram cues, so even a partial decode doesn't leak the answer.

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
