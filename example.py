import nbformat as nbf
import random
import os
import ephem
import math
import numpy as np
import cv2
import base64

# ============================================================================
# CHALLENGE METADATA - Required for automatic challenge registration
# ============================================================================

challenge_metadata = {
    "title": "Celestial Chase",
    "description": "Stranded light-years from home, your only way back is written in the stars. Decode the cosmos before time runs out.",
    "imageURL": "/resources/python.jpg",
    "difficulty": "Astronomically Hard",
    "is_active": True,
}

# ============================================================================
# CONFIGURATION: One-word title for file naming
# ============================================================================
one_word_title = "celestialchase"

challenge_hints = {
    1: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl1_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": False,
    },
    2: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl2_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": False,
    },
    3: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl3_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": True,
    },
}

# ============================================================================
# TODO SECTION: Edit the word list below
# ============================================================================
# You can customize this word list to create your own challenge theme.
# The list should contain roughly 20 different code-related words (more is allowed).
# Each word will be randomly selected based on the challenge code/seed.
# Students will need to extract these words from the puzzle text.
#
# ADAPT:
# - words: Change the list items to your desired words
# ============================================================================

words = [
    "python", "coding", "challenge", "notebook", "jupyter",
    "function", "variable", "loop", "list", "string",
    "algorithm", "debug", "compile", "syntax", "module",
    "library", "import", "class", "object", "method"
]

# Fixed observation constants - all students use the same date/location
OBS_DATE = '2025/6/21 12:00:00'  # Summer solstice, UTC
OBS_LAT  = '47.3769'             # Zurich
OBS_LON  = '8.5417'

# ============================================================================
# DO NOT MODIFY: The functions below are required for the challenge system
# ============================================================================

def get_solution(code, lvl):
    """Generate solution for each level based on code seed"""
    random.seed(code + lvl)
    return random.choice(words)

def get_hash(number):
    """Hash function for code validation"""
    return number % 20

# ============================================================================
# if you want, you can implement a custom solution checker function here, rather than just having the exact word match, might want to discuss this with the CASH team first though
#def check_solution(expected_code, submitted_code, level, user_hash):
#    """
#    Custom validation for TSP challenge.
#     Level 1: Float with 5% tolerance
#     Level 2: Float with 0.1% tolerance
#     """
#     try:
#         code_parsed = float(submitted_code)
#         expected = float(expected_code)
#
#         if level == 1:
#             # 5% tolerance
#             return abs(code_parsed - expected) < 0.05 * expected
#         elif level == 2:
#             # 0.1% tolerance
#             return abs(code_parsed - expected) < 0.001 * expected
#         else:
#             return expected_code == submitted_code
#     except:
#         return False

#def get_solution(final_challenge_code, lvl):
#   if you decide to implement a custom checker then this function has to give the solution to a given level
#   SO YOU NEED TO REPLACE THE GET_SOLUTION FUNCTION FROM ABOVE
#    random.seed(code+lvl)
#    return random.choice(words)


def generate_notebook_lvl(final_challenge_code=1, solution=False, nb=None, level=1):
    # ---------------------------------------------------------
    # do not modify this section for generating the notebook file
    filename = f"{one_word_title}_lvl{level}_{final_challenge_code}.ipynb"
    if solution:
        filename = f"{one_word_title}_lvl{level}_solution.ipynb"

    print(f"Generating notebook {filename}...")
    os.makedirs(f"notebooks/{one_word_title}", exist_ok=True)
    filename = f"notebooks/{one_word_title}/" + filename

    with open(filename, "w") as f:
        nbf.write(nb, f)
    print(f"Notebook '{filename}' generated successfully!")

# ============================================================================
# END: DO NOT MODIFY
# ============================================================================


# ============================================================================
# IMAGE + CIPHER HELPERS
# ============================================================================

def img_to_base64(img):
    """Encode a cv2 image to a base64 PNG string for embedding in notebooks."""
    _, buf = cv2.imencode('.png', img)
    return base64.b64encode(buf).decode('utf-8')

def make_perm(n, seed):
    """Generate a reproducible permutation of range(n) from an integer seed."""
    rng = random.Random(seed)
    perm = list(range(n))
    rng.shuffle(perm)
    return perm

def transpose_encode(word, perm):
    """Transposition cipher: rearrange word letters according to perm.
    encoded[perm[i]] = word[i]  =>  decode: decoded[i] = encoded[perm[i]]
    """
    encoded = [''] * len(word)
    for i, c in enumerate(word):
        encoded[perm[i]] = c
    return ''.join(encoded)

def get_observer():
    """Return a configured ephem.Observer for Zurich at OBS_DATE."""
    obs = ephem.Observer()
    obs.lat  = OBS_LAT
    obs.lon  = OBS_LON
    obs.date = OBS_DATE
    return obs

def az_alt_to_xy(az_deg, alt_deg, w, h):
    """
    Map azimuth (0-360) and altitude (-90 to 90) to image pixel coordinates.
    az  -> x: 0 deg = left, 360 deg = right
    alt -> y: 90 deg = top, -90 deg = bottom (flipped for image coords)
    """
    x = int((az_deg % 360) / 360 * w) % w
    y = int((90 - alt_deg) / 180 * h) % h
    return x, y

def make_starfield(w, h, n_stars=300, seed=42):
    """Dark starfield with random white/grey dots of varying brightness."""
    rng = np.random.RandomState(seed)
    img = np.zeros((h, w, 3), dtype=np.uint8)
    xs = rng.randint(0, w, n_stars)
    ys = rng.randint(0, h, n_stars)
    brightness = rng.randint(80, 255, n_stars)
    for x, y, b in zip(xs, ys, brightness):
        img[y, x] = [b, b, b]
    return img

def make_nebula(w, h, seed=42):
    """Colorful nebula background with random stars on top."""
    rng = np.random.RandomState(seed)
    base = rng.randint(0, 60, (h, w, 3)).astype(np.uint8)
    for _ in range(6):
        cx, cy = rng.randint(0, w), rng.randint(0, h)
        r      = rng.randint(60, 150)
        color  = rng.randint(20, 120, 3).tolist()
        cv2.circle(base, (cx, cy), r, color, -1)
    base = cv2.GaussianBlur(base, (61, 61), 0)
    xs = rng.randint(0, w, 400)
    ys = rng.randint(0, h, 400)
    brightness = rng.randint(120, 255, 400)
    for x, y, b in zip(xs, ys, brightness):
        base[y, x] = [b, b, b]
    return base


# ============================================================================
# TODO SECTION: Notebook Level Challenges
# ============================================================================
# Edit the challenge text to create the levels for your own challenge
#
# Each level outputs a valid Jupyter notebook. You can include text, images,
# code cells, and subtasks.
#
# IMPORTANT: the correct code word is determined by calling "get_solution(code)"
#
# ADAPT the following functions:
# - generate_notebook_lvl1(): Customize level 1
# - generate_notebook_lvl2(): Customize level 2
# - generate_notebook_lvl3(): Customize level 3
# ============================================================================


def generate_notebook_lvl1(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text and instructions for level 1
    # do not modify the solution extraction logic below

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 1)
    # --------------------------------

    """
    Level 1: The Teal Beacon
    - 400x400 starfield image with Venus marked as a cyan pixel at its az/alt position
    - key = int(venus_az_deg) * int(venus_alt_deg) + int(venus_phase)
    - Word encoded with transposition cipher keyed by this value
    - Students: find cyan pixel with cv2, compute Venus phase with ephem, build key, decode
    - Cannot brute force: need exact pixel coords AND venus.phase combined
    """

    nb = nbf.v4.new_notebook()

    # Header
    nb.cells.append(nbf.v4.new_markdown_cell("## CASH Notebook"))
    nb.cells.append(nbf.v4.new_markdown_cell("## Celestial Chase - LVL 1: The Teal Beacon"))
    nb.cells.append(nbf.v4.new_markdown_cell(
        "### 🛰️ Need help? Open the mission briefing:\n"
        "[**OPEN LVL 1 HINT PAGE**](https://alexrtw05.github.io/CASH-project/lvl1.html)\n\n"
        "_Open in your browser for cipher tools, hints, and the full mission narrative._"
    ))

    # --- Astronomy computation ---
    obs = get_observer()
    venus = ephem.Venus()
    venus.compute(obs)
    az_deg  = int(math.degrees(float(venus.az)))
    alt_deg = int(math.degrees(float(venus.alt)))
    phase   = int(venus.phase)

    # Compute pixel position - encoding happens after image is built
    W, H = 400, 400
    vx, vy = az_alt_to_xy(az_deg, alt_deg, W, H)

    # --- Image generation - unique per user ---
    rng = np.random.RandomState(final_challenge_code * 17 + 3)

    # Unique background: vary star count, brightness, subtle tint per user
    n_bg_stars = rng.randint(200, 500)
    tint       = rng.randint(0, 25, 3).tolist()
    img        = np.zeros((H, W, 3), dtype=np.uint8)
    xs         = rng.randint(0, W, n_bg_stars)
    ys         = rng.randint(0, H, n_bg_stars)
    bvals      = rng.randint(60, 230, n_bg_stars)
    for x, y, b in zip(xs, ys, bvals):
        img[y, x] = [max(0, min(255, b + tint[i])) for i in range(3)]

    # Decoy near-cyan pixels to prevent trivial single-pixel search
    # Real Venus: R=0 exactly. Decoys: R in 1-30 (visually similar, not exact)
    n_decoys = rng.randint(4, 9)
    for _ in range(n_decoys):
        dpx = rng.randint(5, W-5)
        dpy = rng.randint(5, H-5)
        fake_r = int(rng.randint(1, 30))
        img[dpy, dpx] = [255, 255, fake_r]

    # Real Venus: bright cyan cross, R=0 exactly
    vx, vy = az_alt_to_xy(az_deg, alt_deg, W, H)
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(0,0)]:
        nx, ny = vx+dx, vy+dy
        if 0 <= nx < W and 0 <= ny < H:
            img[ny, nx] = [255, 255, 0]  # BGR cyan - R must be exactly 0

    # Compute decoy_sum: sum of red-channel values of the decoy near-cyan pixels.
    # Decoys: B=255, G=255, R in [1,30]; real Venus has R=0 so it's excluded by R > 0.
    # The < 50 upper bound gives students a tiny safety margin.
    decoy_mask = (img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] > 0) & (img[:,:,2] < 50)
    decoy_sum  = int(img[decoy_mask, 2].sum())

    # Per-letter Caesar cipher. Each letter at position i is shifted by
    #   shift_i = (pixel_x + pixel_y + venus.phase + decoy_sum + i*7) % 26
    # decoy_sum is per-image (different for every student), so two students with
    # the same secret word still produce different ciphertexts. The position-dependent
    # i*7 term means brute-forcing all 26 shifts on the whole word doesn't work.
    shift_base = (vx + vy + phase + decoy_sum) % 26
    encoded_chars = []
    for i, ch in enumerate(final_solution_word):
        shift = (shift_base + i * 7) % 26
        encoded_chars.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
    encoded_word = ''.join(encoded_chars)

    img_b64 = img_to_base64(img)

    # --- Notebook cells ---
    intro_text = """You've just woken up from cryo-sleep. No memory. No crew. Just you, a dying sun, and a faint signal pulsing from the sky.

One star glows different from the rest. Not white. Not grey. **Teal.**

Find it. Its position holds part of the key. But position alone is not enough - you must also know how much of its face is lit by the sun, and listen for the dimmer ghosts of cyan scattered through the night.

The signal arrives shifted - each letter pushed a different distance along the alphabet. Recover the shifts and the message clears.

---

**The encoded signal:** `{encoded}`

**Your task:**
1. Display the image and find the **real cyan pixel** - the only pixel where `B == 255` and `G == 255` and `R == 0` (decoys have `R > 0`).
2. Read its `(x, y)` coordinates.
3. Find all **decoy near-cyan pixels** (`B == 255` and `G == 255` and `0 < R < 50`) and sum their red-channel values: `decoy_sum = sum(img[mask, 2])`. This number is unique to your image.
4. Use `ephem` to compute **Venus's phase** (`int(venus.phase)`) on `{date}` UTC from Zurich (lat=`{lat}`, lon=`{lon}`).
5. Build the base shift: `shift_base = (x + y + int(venus.phase) + decoy_sum) % 26`.
6. For each letter `i` of the encoded word (0-indexed), the shift used was `(shift_base + i * 7) % 26`. Reverse it:
   - `decoded[i] = chr((ord(encoded[i]) - ord('a') - shift) % 26 + ord('a'))`
""".format(encoded=encoded_word, date=OBS_DATE, lat=OBS_LAT, lon=OBS_LON)

    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))

    # Image loader cell - base64 embedded so students need no external files
    image_cell = f"""import base64, cv2, numpy as np
from IPython.display import display, Image as IPImage

# Starfield image embedded directly in this notebook
img_b64 = "{img_b64}"

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

cv2.imwrite('starfield.png', img)
display(IPImage('starfield.png'))
print("Image shape:", img.shape)
"""
    nb.cells.append(nbf.v4.new_code_cell(image_cell))

    # Student solution cell
    student_code = f"""import ephem

encoded  = "{encoded_word}"
obs_date = "{OBS_DATE}"
obs_lat  = "{OBS_LAT}"
obs_lon  = "{OBS_LON}"

# TODO Step 1: Find the real cyan pixel (B=255, G=255, R=0) in img.
# Hint: build a mask, then use np.where.
pixel_x, pixel_y = 0, 0  # replace with actual coordinates

# TODO Step 2: Sum the red-channel values of all decoy near-cyan pixels.
# Decoys have B=255, G=255, and 0 < R < 50.
# Hint: build a mask, then img[mask, 2].sum()
decoy_sum = 0  # replace

# TODO Step 3: Compute Venus's phase with ephem.
obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date
venus = ephem.Venus()
venus.compute(obs)
phase = 0  # replace: int(venus.phase)

# TODO Step 4: Build the base shift.
shift_base = 0  # replace: (pixel_x + pixel_y + phase + decoy_sum) % 26

# TODO Step 5: Reverse the per-letter Caesar shift.
# For each letter at position i:
#   shift = (shift_base + i * 7) % 26
#   plain = chr((ord(encoded[i]) - ord('a') - shift) % 26 + ord('a'))
answer = ""
# fill in the loop here

print(answer)
"""
    nb.cells.append(nbf.v4.new_code_cell(student_code))

    # Solution code
    solution_code = f"""import ephem, cv2, numpy as np, base64

encoded  = "{encoded_word}"
img_b64  = "{img_b64}"
obs_date = "{OBS_DATE}"
obs_lat  = "{OBS_LAT}"
obs_lon  = "{OBS_LON}"

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

# Real cyan pixel: B=255, G=255, R=0
real_mask = (img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] == 0)
ys, xs    = np.where(real_mask)
pixel_x   = int(np.median(xs))
pixel_y   = int(np.median(ys))

# Decoy near-cyan pixels: B=255, G=255, 0 < R < 50
decoy_mask = (img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] > 0) & (img[:,:,2] < 50)
decoy_sum  = int(img[decoy_mask, 2].sum())

obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date
venus = ephem.Venus()
venus.compute(obs)
phase = int(venus.phase)

shift_base = (pixel_x + pixel_y + phase + decoy_sum) % 26

answer = ""
for i, ch in enumerate(encoded):
    shift  = (shift_base + i * 7) % 26
    answer += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))

print(answer)  # {final_solution_word}
"""

    # TODO:
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell
    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below

    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file
    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=1)
    # -----------------------------------------------------------------


def generate_notebook_lvl2(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text and instructions for level 2
    # do not modify the solution extraction logic below

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 2)
    # --------------------------------

    """
    Level 2: Ghost Stars
    - 600x600 nebula image
    - 4 planets (Mars, Jupiter, Saturn, Mercury) placed as near-white 3x3 pixels at their sky positions
    - Each pixel blue channel = int(planet.earth_distance * 1000) % 256
    - seed = sum(blue_channel[i] + int(alt_deg[i]) for each planet)
    - Word encoded with transposition cipher keyed by this seed
    - Students: find 4 special pixels with cv2, read blue channels, compute altitudes with ephem, combine, decode
    - Cannot brute force: needs exact blue channels from image AND exact altitudes from ephem combined
    """

    nb = nbf.v4.new_notebook()

    # Header
    nb.cells.append(nbf.v4.new_markdown_cell("## CASH Notebook"))
    nb.cells.append(nbf.v4.new_markdown_cell("## Celestial Chase - LVL 2: Ghost Stars"))
    nb.cells.append(nbf.v4.new_markdown_cell(
        "### 🛰️ Need help? Open the mission briefing:\n"
        "[**OPEN LVL 2 HINT PAGE**](https://alexrtw05.github.io/CASH-project/lvl2.html)\n\n"
        "_Open in your browser for BGR explainers, cluster tools, and the key calculator._"
    ))

    # --- Astronomy computation ---
    obs = get_observer()
    planet_names = ['Mars', 'Jupiter', 'Saturn', 'Mercury']
    body_map = {
        'Mars':    ephem.Mars,
        'Jupiter': ephem.Jupiter,
        'Saturn':  ephem.Saturn,
        'Mercury': ephem.Mercury,
    }

    planet_data = {}  # name -> (az_deg, alt_deg, blue_channel)
    for name in planet_names:
        body = body_map[name]()
        body.compute(obs)
        az_deg  = int(math.degrees(float(body.az)))
        alt_deg = int(math.degrees(float(body.alt)))
        blue    = int(body.earth_distance * 1000) % 256
        planet_data[name] = (az_deg, alt_deg, blue)

    # Encoding happens AFTER image generation so we can mix in a per-image quantity

    # --- Image generation - unique per user ---
    W, H = 600, 600
    rng = np.random.RandomState(final_challenge_code * 31 + 7)

    # Unique nebula per user: vary blob count, positions, colors, sizes
    base = rng.randint(0, 50, (H, W, 3)).astype(np.uint8)
    n_blobs = int(rng.randint(5, 10))
    for _ in range(n_blobs):
        cx    = int(rng.randint(0, W))
        cy    = int(rng.randint(0, H))
        r     = int(rng.randint(40, 180))
        color = rng.randint(10, 110, 3).tolist()
        cv2.circle(base, (cx, cy), r, color, -1)
    img = cv2.GaussianBlur(base, (61, 61), 0)

    # Unique background stars per user
    n_bg = int(rng.randint(300, 600))
    bxs  = rng.randint(0, W, n_bg)
    bys  = rng.randint(0, H, n_bg)
    bvs  = rng.randint(100, 255, n_bg)
    for x, y, b in zip(bxs, bys, bvs):
        img[y, x] = [b, b, b]

    # Decoy near-white 3x3 patches: G=255, R=255, B=255 (pure white)
    # Real planets have B != 255, so students filter: G==255 and R==255 and B!=255
    n_decoys = int(rng.randint(6, 14))
    for _ in range(n_decoys):
        dpx = int(rng.randint(5, W-5))
        dpy = int(rng.randint(5, H-5))
        for ddx in range(-1, 2):
            for ddy in range(-1, 2):
                nx, ny = dpx+ddx, dpy+ddy
                if 0 <= nx < W and 0 <= ny < H:
                    img[ny, nx] = [255, 255, 255]  # pure white decoy

    # Real planet markers: G=255, R=255, B=blue_channel (always < 255)
    for name, (az_deg, alt_deg, blue) in planet_data.items():
        blue = blue % 255  # ensure never 255 so decoys are distinguishable
        px, py = az_alt_to_xy(az_deg, alt_deg, W, H)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = px+dx, py+dy
                if 0 <= nx < W and 0 <= ny < H:
                    img[ny, nx] = [blue, 255, 255]  # BGR: B=blue (not 255)

    # Count pure-white decoy clusters in the actual image. Pure white is B=G=R=255;
    # real planet markers have B != 255 so they are excluded.
    # Counting clusters (not pixels) gives a small integer (6-13 ish) that's distinct per user
    # but easy to compute - the student just labels connected components on the pure-white mask.
    from scipy import ndimage as _nd
    pure_white_mask = (img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] == 255)
    _, decoy_count  = _nd.label(pure_white_mask)

    # Astronomy contribution: sum of (blue + altitude) over all 4 planets
    planet_sum = sum(blue + alt for (_, alt, blue) in planet_data.values())

    # XOR stream cipher with key derived from (planet_sum, decoy_count).
    # planet_sum requires ALL FOUR planets matched correctly; decoy_count requires
    # actually counting clusters in this student's nebula. Combined, two students with
    # the same secret word still produce different ciphertexts.
    base_key = (planet_sum + decoy_count) & 0xFF
    encoded_chars = []
    for i, ch in enumerate(final_solution_word):
        key_byte    = (base_key + i * 23) & 0xFF
        cipher_byte = ord(ch) ^ key_byte
        encoded_chars.append(f"{cipher_byte:02x}")
    encoded_word = ''.join(encoded_chars)

    img_b64 = img_to_base64(img)

    # --- Notebook cells ---
    intro_text = """The Astrophage trail leads deeper into the system. Four planets. Four signals. None of them quite white.

Your instruments detect four near-white pixels scattered across the nebula. They look like noise - but they are not. Each one was placed by a planet at the exact moment of observation. Their blue channel encodes the distance. Their position in the sky encodes the altitude.

But the nebula also hides pure-white interference - decoy clusters left by cosmic radiation. Their count is a fingerprint of your particular slice of space.

The signal is XOR-scrambled into raw bytes. Combine the planets and the noise to recover the mask.

---

**The encoded signal (hex):** `{encoded}`

**Your task:**
1. Display the nebula. Find the **four real planet markers** - 3x3 patches where `G == 255` and `R == 255` and `B != 255` (pure-white decoys have B=255 too).
2. Find the **pure-white decoy clusters** - 3x3 patches where `B == G == R == 255`. Count how many distinct clusters there are (use `scipy.ndimage.label` or implement your own flood fill). Call this `decoy_count`.
3. For each real planet marker centre, read its **blue channel**: `img[y, x, 0]` (OpenCV uses BGR).
4. Use `ephem` to compute each planet's **altitude in degrees** on `{date}` UTC from Zurich. Planets in order: `{planets}`.
5. Match each cluster to its planet using the position formula:
   ```
   x = int((az_deg % 360) / 360 * 600)
   y = int((90 - alt_deg) / 180 * 600)
   ```
6. Build `planet_sum = sum(blue_channel + altitude_deg for each planet)`.
7. Build the base key: `base_key = (planet_sum + decoy_count) & 0xFF`.
8. Walk the hex string two characters at a time. For byte `i`:
   - `key_byte = (base_key + i * 23) & 0xFF`
   - `plain_byte = int(hex_byte, 16) ^ key_byte`
   - Append `chr(plain_byte)` to your answer.
""".format(encoded=encoded_word, date=OBS_DATE, planets=planet_names)

    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))

    # Image loader cell
    image_cell = f"""import base64, cv2, numpy as np
from IPython.display import display, Image as IPImage

img_b64 = "{img_b64}"

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

cv2.imwrite('nebula.png', img)
display(IPImage('nebula.png'))
print("Image shape:", img.shape)
"""
    nb.cells.append(nbf.v4.new_code_cell(image_cell))

    # Student solution cell
    student_code = f"""import ephem, math, numpy as np

encoded      = "{encoded_word}"  # hex string, 2 chars per byte
obs_date     = "{OBS_DATE}"
obs_lat      = "{OBS_LAT}"
obs_lon      = "{OBS_LON}"
planet_names = {planet_names}
W, H         = 600, 600

# TODO Step 1: Find pure-white decoy clusters (B==255, G==255, R==255).
# Count how many distinct clusters there are - this is decoy_count.
# Hint: from scipy import ndimage; _, decoy_count = ndimage.label(mask)
decoy_count = 0  # replace

# TODO Step 2: Find the four real planet markers (G==255, R==255, B!=255).
# Group into 4 clusters and take the center of each.
# Read each centre's blue channel: blue = img[cy, cx, 0]

# TODO Step 3: Compute each planet's az and alt with ephem
obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date

body_map = {{
    'Mars':    ephem.Mars,
    'Jupiter': ephem.Jupiter,
    'Saturn':  ephem.Saturn,
    'Mercury': ephem.Mercury,
}}

# Match each planet to its cluster using:
#   x = int((az_deg % 360) / 360 * W)
#   y = int((90 - alt_deg) / 180 * H)

# TODO Step 4: Build planet_sum
# planet_sum = sum(blue_channel[i] + int(alt_deg[i]) for each planet in planet_names order)
planet_sum = 0  # replace

# TODO Step 5: Build the base key (kept in one byte)
base_key = (planet_sum + decoy_count) & 0xFF

# TODO Step 6: XOR-decode the hex string
# For each byte at position i:
#   cipher_byte = int(encoded[i:i+2], 16)
#   key_byte    = (base_key + (i // 2) * 23) & 0xFF
#   append chr(cipher_byte ^ key_byte) to answer
answer = ""
# fill in the loop here

print(answer)
"""
    nb.cells.append(nbf.v4.new_code_cell(student_code))

    # Solution code
    solution_code = f"""import ephem, math, cv2, numpy as np, base64
from scipy import ndimage

encoded      = "{encoded_word}"
img_b64      = "{img_b64}"
obs_date     = "{OBS_DATE}"
obs_lat      = "{OBS_LAT}"
obs_lon      = "{OBS_LON}"
planet_names = {planet_names}
W, H         = 600, 600

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

# Pure-white decoy clusters
pure_white = (img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] == 255)
_, decoy_count = ndimage.label(pure_white)

# Real planet markers: G==255, R==255, B!=255
real_mask = (img[:,:,1] == 255) & (img[:,:,2] == 255) & (img[:,:,0] != 255)
labeled, n_clusters = ndimage.label(real_mask)

clusters = []
for i in range(1, n_clusters + 1):
    ys, xs = np.where(labeled == i)
    cy, cx = int(np.median(ys)), int(np.median(xs))
    blue   = int(img[cy, cx, 0])
    clusters.append((cx, cy, blue))

obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date

body_map = {{
    'Mars':    ephem.Mars,
    'Jupiter': ephem.Jupiter,
    'Saturn':  ephem.Saturn,
    'Mercury': ephem.Mercury,
}}

planet_sum = 0
for name in planet_names:
    body = body_map[name]()
    body.compute(obs)
    az_deg  = int(math.degrees(float(body.az)))
    alt_deg = int(math.degrees(float(body.alt)))
    ex = int((az_deg % 360) / 360 * W) % W
    ey = int((90 - alt_deg) / 180 * H) % H
    closest = min(clusters, key=lambda c: abs(c[0]-ex) + abs(c[1]-ey))
    planet_sum += closest[2] + alt_deg

base_key = (planet_sum + decoy_count) & 0xFF

answer = ""
for i in range(0, len(encoded), 2):
    cipher_byte = int(encoded[i:i+2], 16)
    key_byte    = (base_key + (i // 2) * 23) & 0xFF
    answer     += chr(cipher_byte ^ key_byte)

print(answer)  # {final_solution_word}
"""

    # TODO:
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell
    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below

    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file
    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=2)
    # -----------------------------------------------------------------


def generate_notebook_lvl3(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text and instructions for level 3
    # do not modify the solution extraction logic below

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 3)
    # --------------------------------

    """
    Level 3: The Star Chart
    - 800x800 chart with 15 real bright stars at actual sky positions (labelled)
    - Stars sorted by altitude descending; top N (N=len(word)) carry the message
    - Each top-N star has a red-channel value embedded in the image (28-227)
    - Per-byte XOR keystream: key_byte[i] = (red_channel_i + altitude_i) & 0xFF
      where i indexes the i-th star in altitude rank
    - Output is hex (2 chars per plaintext byte) - unguessable
    - Cannot brute force: 15! orderings, AND each byte's key combines pixel + astronomy
    """

    nb = nbf.v4.new_notebook()

    # Header
    nb.cells.append(nbf.v4.new_markdown_cell("## CASH Notebook"))
    nb.cells.append(nbf.v4.new_markdown_cell("## Celestial Chase - LVL 3: The Star Chart"))
    nb.cells.append(nbf.v4.new_markdown_cell(
        "### 🛰️ Need help? Open the mission briefing:\n"
        "[**OPEN LVL 3 HINT PAGE**](https://alexrtw05.github.io/CASH-project/lvl3.html)\n\n"
        "_Open in your browser for the star altitude sorter, XOR decoder, and full pipeline guide._"
    ))

    # --- Astronomy computation ---
    obs = get_observer()

    STAR_NAMES = [
        'Sirius', 'Canopus', 'Arcturus', 'Vega', 'Capella',
        'Rigel', 'Procyon', 'Betelgeuse', 'Altair', 'Aldebaran',
        'Antares', 'Spica', 'Pollux', 'Fomalhaut', 'Deneb',
    ]

    star_data = []  # (name, az_deg, alt_deg)
    for name in STAR_NAMES:
        star = ephem.star(name)
        star.compute(obs)
        az_deg  = int(math.degrees(float(star.az)))
        alt_deg = int(math.degrees(float(star.alt)))
        star_data.append((name, az_deg, alt_deg))

    n = len(final_solution_word)

    # Sort all stars by altitude descending, take top N
    sorted_stars = sorted(star_data, key=lambda s: s[2], reverse=True)
    top_stars    = sorted_stars[:n]

    # Per-star red channel value, deterministic across sessions (uses hashlib, NOT hash()).
    # Range 28-227 by construction; decoys use R in 1-27 so students filter R >= 28.
    import hashlib as _hashlib
    def _star_red(name, code):
        h = _hashlib.md5(f"{name}|{code}".encode()).digest()
        return (h[0] | (h[1] << 8)) % 200 + 28  # always 28-227

    red_channels = [_star_red(name, final_challenge_code) for name, _, _ in top_stars]

    # XOR-hex encoding. Each plaintext byte is XOR'd with a key byte derived from
    # the i-th ranked star's (red_channel + altitude). This couples image and astronomy
    # PER BYTE - any single ranking error or missed pixel corrupts that byte.
    encoded_chars = []
    for i, ch in enumerate(final_solution_word):
        _, _, alt_i = top_stars[i]
        key_byte    = (red_channels[i] + alt_i) & 0xFF
        cipher_byte = ord(ch) ^ key_byte
        encoded_chars.append(f"{cipher_byte:02x}")
    encoded_word = ''.join(encoded_chars)

    # --- Image generation - unique per user ---
    W, H = 800, 800
    rng = np.random.RandomState(final_challenge_code * 53 + 11)

    # Unique dark background with nebula hints per user
    base = rng.randint(0, 20, (H, W, 3)).astype(np.uint8)
    n_blobs = int(rng.randint(3, 7))
    for _ in range(n_blobs):
        cx    = int(rng.randint(0, W))
        cy    = int(rng.randint(0, H))
        r     = int(rng.randint(80, 250))
        color = [int(rng.randint(0, 15)), int(rng.randint(0, 15)), int(rng.randint(5, 25))]
        cv2.circle(base, (cx, cy), r, color, -1)
    img = cv2.GaussianBlur(base, (81, 81), 0)

    # Unique background noise stars per user
    n_bg = int(rng.randint(400, 700))
    bxs  = rng.randint(0, W, n_bg)
    bys  = rng.randint(0, H, n_bg)
    bvs  = rng.randint(80, 220, n_bg)
    for x, y, b in zip(bxs, bys, bvs):
        img[y, x] = [b, b, b]

    # Draw all 15 named stars as white circles
    for name, az_deg, alt_deg in star_data:
        px, py = az_alt_to_xy(az_deg, alt_deg, W, H)
        cv2.circle(img, (px, py), 3, (200, 200, 200), -1)

    # Decoy red pixels: B=0, G=0, R in 1-27 (dim red, looks similar but value is low)
    # Real message stars: R in 28-227 (always >= 28 by construction)
    n_decoys = int(rng.randint(8, 18))
    for _ in range(n_decoys):
        dpx = int(rng.randint(5, W-5))
        dpy = int(rng.randint(5, H-5))
        fake_r = int(rng.randint(1, 27))
        cv2.circle(img, (dpx, dpy), 4, (0, 0, fake_r), -1)

    # Real message stars: R in 28-227 (students filter R >= 28).
    # Use the SAME hashlib-derived value as the encoding step (deterministic across sessions).
    for i, (name, az_deg, alt_deg) in enumerate(top_stars):
        rc = _star_red(name, final_challenge_code)
        px, py = az_alt_to_xy(az_deg, alt_deg, W, H)
        cv2.circle(img, (px, py), 4, (0, 0, rc), -1)

    # Label all 15 named stars (same positions for all users - astronomy is fixed)
    for name, az_deg, alt_deg in star_data:
        px, py = az_alt_to_xy(az_deg, alt_deg, W, H)
        cv2.putText(img, name, (px+5, py-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (160, 160, 160), 1, cv2.LINE_AA)

    img_b64 = img_to_base64(img)

    # --- Notebook cells ---
    intro_text = """You are alone. 40 light-years from Earth. The Hail Mary is your last hope.

Mission control's final message was not sent in words. It was written in the stars themselves.

They ranked every visible star by how high it stood in the sky. The brightest in altitude came first. They marked {n} of them red - one per letter. The redness sets the mask. The altitude sets the mask. The order is fixed by the rank.

The signal arrives as raw hex. Find the red stars. Measure their glow. Combine with their height. XOR away the mask. The word will appear.

---

**The encoded signal (hex):** `{encoded}`

**Your task:**
1. Display the star chart. The **real message stars** are red pixels with `B == 0` and `G == 0` and `R >= 28`. Decoy red pixels have `R < 28`.
2. Use `ephem` to compute the **altitude** of all 15 stars on `{date}` UTC from Zurich:
   ```python
   stars = {stars}
   ```
3. Sort all 15 stars by altitude **descending**. Take the top **{n}** - these are the message stars, in altitude-rank order.
4. For each of the top {n} stars, find its pixel in the chart using the position formula and read the **red channel**: `img[y, x, 2]`.
5. The encoded message is hex - 2 chars per byte, {n} bytes total. For byte at position `i` (0-indexed):
   - `key_byte    = (red_channel_i + altitude_deg_i) & 0xFF`
   - `cipher_byte = int(encoded[2i:2i+2], 16)`
   - Append `chr(cipher_byte ^ key_byte)` to the answer.

**Position formula:**
```python
x = int((az_deg % 360) / 360 * 800) % 800
y = int((90 - alt_deg) / 180 * 800) % 800
```
""".format(encoded=encoded_word, date=OBS_DATE, n=n, stars=STAR_NAMES)

    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))

    # Image loader cell
    image_cell = f"""import base64, cv2, numpy as np
from IPython.display import display, Image as IPImage

img_b64 = "{img_b64}"

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

cv2.imwrite('starchart.png', img)
display(IPImage('starchart.png'))
print("Image shape:", img.shape)
"""
    nb.cells.append(nbf.v4.new_code_cell(image_cell))

    # Student solution cell
    student_code = f"""import ephem, math, numpy as np

encoded    = "{encoded_word}"  # hex string, 2 chars per byte
obs_date   = "{OBS_DATE}"
obs_lat    = "{OBS_LAT}"
obs_lon    = "{OBS_LON}"
n          = {n}
W, H       = 800, 800
star_names = {STAR_NAMES}

# TODO Step 1: Compute az and alt for each of the 15 stars
obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date

star_data = []
for name in star_names:
    star = ephem.star(name)
    star.compute(obs)
    az_deg  = int(math.degrees(float(star.az)))
    alt_deg = int(math.degrees(float(star.alt)))
    star_data.append((name, az_deg, alt_deg))

# TODO Step 2: Sort by altitude descending, take the top n
sorted_stars = sorted(star_data, key=lambda s: s[2], reverse=True)
top_stars    = sorted_stars[:n]

# TODO Step 3: For each top star compute pixel position and read the red channel from img.
# x = int((az_deg % 360) / 360 * W) % W
# y = int((90 - alt_deg) / 180 * H) % H
# red = img[y, x, 2]
red_channels = [0] * n  # replace each entry with the actual red value

# TODO Step 4: XOR-decode. For byte at position i:
#   key_byte    = (red_channels[i] + altitude_of_star_i) & 0xFF
#   cipher_byte = int(encoded[2*i:2*i+2], 16)
#   answer     += chr(cipher_byte ^ key_byte)
answer = ""
# fill in the loop here

print(answer)
"""
    nb.cells.append(nbf.v4.new_code_cell(student_code))

    # Solution code
    solution_code = f"""import ephem, math, cv2, numpy as np, base64

encoded    = "{encoded_word}"
img_b64    = "{img_b64}"
obs_date   = "{OBS_DATE}"
obs_lat    = "{OBS_LAT}"
obs_lon    = "{OBS_LON}"
n          = {n}
W, H       = 800, 800
star_names = {STAR_NAMES}

img_bytes = base64.b64decode(img_b64)
img_arr   = np.frombuffer(img_bytes, dtype=np.uint8)
img       = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

obs = ephem.Observer()
obs.lat  = obs_lat
obs.lon  = obs_lon
obs.date = obs_date

star_data = []
for name in star_names:
    star = ephem.star(name)
    star.compute(obs)
    az_deg  = int(math.degrees(float(star.az)))
    alt_deg = int(math.degrees(float(star.alt)))
    star_data.append((name, az_deg, alt_deg))

sorted_stars = sorted(star_data, key=lambda s: s[2], reverse=True)
top_stars    = sorted_stars[:n]

red_channels = []
for name, az_deg, alt_deg in top_stars:
    px = int((az_deg % 360) / 360 * W) % W
    py = int((90 - alt_deg) / 180 * H) % H
    red_channels.append(int(img[py, px, 2]))

answer = ""
for i in range(n):
    _, _, alt_i = top_stars[i]
    key_byte    = (red_channels[i] + alt_i) & 0xFF
    cipher_byte = int(encoded[2*i:2*i+2], 16)
    answer     += chr(cipher_byte ^ key_byte)

print(answer)  # {final_solution_word}
"""

    # TODO:
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell
    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below

    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file
    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=3)
    # -----------------------------------------------------------------


# ============================================================================
# DO NOT MODIFY: Notebook generation and main execution
# ============================================================================

def gen_notebook(code=1, solution=False):
    """Generate all levels for a given code"""
    generate_notebook_lvl1(code, solution)
    generate_notebook_lvl2(code, solution)
    generate_notebook_lvl3(code, solution)


# Execute when run as a script
if __name__ == '__main__':
    # Generate solution notebooks
    gen_notebook(code=1, solution=True)

    # Generate challenge notebooks for different codes
    for i in range(20):
        gen_notebook(code=i, solution=False)

    print("All notebooks generated successfully!")
    print(f"You can find them in the notebooks/{one_word_title}/ directory.")

# ============================================================================
# END: DO NOT MODIFY
# ============================================================================