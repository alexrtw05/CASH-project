# Celestial Chase

> *Stranded light-years from home, your only way back is written in the stars. Decode the cosmos before time runs out.*

A three-level astronomy coding challenge built for the CASH scavenger hunt system. Students use the `ephem` Python library to decode secret words hidden using real celestial mechanics.

---

## Overview

Each student receives a unique challenge code (0-19) which determines:
- Their secret word (randomly seeded)
- Their observation date (weekly offsets from a base date)
- Their encoded signal (Caesar cipher keyed to real astronomical data)

Students never see their challenge code. Everything they need is embedded in their notebook.

---

## Levels

### LVL 1 - Lunar Calibration
**Theme:** You've just woken from cryo-sleep. A signal pulses in rhythm with the Moon.

**Task:** Compute the Moon's illumination percentage (`moon.phase`) on the date given in the notebook. Use `int(moon.phase) % 26` as a Caesar shift to decode the word.

**Skills:** basic `ephem` usage, Caesar cipher, string manipulation

---

### LVL 2 - The Petrova Signal
**Theme:** The Astrophage is spreading. Your crewmates left a message encoded in Jupiter's position.

**Task:** Set up an `ephem.Observer` at Zurich, compute Jupiter's altitude in degrees, use `int(altitude) % 26` as the Caesar shift.

**Skills:** `ephem.Observer`, planet computation, unit conversion (radians to degrees)

---

### LVL 3 - Hail Mary
**Theme:** Alone, 40 light-years from Earth. The final transmission is fragmented across the solar system.

**Task:** Compute altitude shifts for four bodies - Sun, Moon, Jupiter, Saturn - in order. Each letter of the encoded word is shifted by a different body (`letter i` uses `shifts[i % 4]`).

**Skills:** multi-body computation, per-letter cipher, building a full decode pipeline

---

## Setup

### Requirements
```bash
pip install ephem nbformat
```

### Generate notebooks
```bash
python celestialchase.py
```

This generates:
- `notebooks/celestialchase/celestialchase_lvl1_0.ipynb` ... `_19.ipynb`
- `notebooks/celestialchase/celestialchase_lvl2_0.ipynb` ... `_19.ipynb`
- `notebooks/celestialchase/celestialchase_lvl3_0.ipynb` ... `_19.ipynb`
- One solution notebook per level (`_solution.ipynb`)

---

## How challenge codes work

| What varies | How |
|---|---|
| Secret word | `random.seed(code + level)` -> `random.choice(words)` |
| Observation date | `base_date + code * 7 days` (weekly steps through lunar cycle) |
| Encoded signal | Caesar cipher keyed to real moon phase / planet altitude on that date |

Students receive a notebook with their date and encoded word already embedded. They compute the astronomy, derive the shift, and decode the word. No challenge code is ever shown to them.

---

## File structure

```
celestialchase.py          - challenge generator (this file)
notebooks/
  celestialchase/
    celestialchase_lvl1_0.ipynb
    ...
    celestialchase_lvl3_19.ipynb
    celestialchase_lvl1_solution.ipynb
    celestialchase_lvl2_solution.ipynb
    celestialchase_lvl3_solution.ipynb
```

---

## Customization

| What | Where |
|---|---|
| Word list | `words = [...]` near top of file |
| Observation location | `OBS_LAT`, `OBS_LON` |
| Base date | `base_date = ephem.Date('2025/1/1 12:00:00')` in lvl1 |
| Date step size | `final_challenge_code * 7` (days per code) |
| Planets used | `bodies = ['Sun', 'Moon', 'Jupiter', 'Saturn']` in lvl3 |
