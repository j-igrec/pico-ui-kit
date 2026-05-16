# pico-ui-kit

A MicroPython UI component library for Raspberry Pi Pico projects with the 1.14" IPS LCD (240×135, ST7789VW). Shared across all Pico projects.

Mirrors the structure and token naming of the main [design-system](../design-system) — primitive tokens → semantic tokens → viewport tokens → components — but rendered via direct pixel drawing calls instead of CSS.

---

## Setup

**Requirements (desktop only — nothing is installed on the Pico):**

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.9+ | Run simulator and build scripts |
| pygame | 2.x | Simulator window rendering |
| font-to-py | 0.44+ | Convert TTF fonts to MicroPython bitmap modules |

```bash
pip3 install pygame font-to-py
```

**Font source files** live in `tokens/src/fonts/` (IBM Plex Mono TTF — open source, available from [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Mono)). These are never deployed to the Pico.

**Generating bitmap fonts** — run once after adding or changing a font source:

```bash
cd pico-ui-kit
FTP=$(python3 -c "import font_to_py, os; print(os.path.dirname(font_to_py.__file__)+'/../../../bin/font_to_py')")
# Or find it with: find ~/Library/Python -name font_to_py 2>/dev/null
$FTP tokens/src/fonts/IBMPlexMono-Regular.ttf  8  fonts/monor8.py
$FTP tokens/src/fonts/IBMPlexMono-Bold.ttf     8  fonts/monob8.py
$FTP tokens/src/fonts/IBMPlexMono-Regular.ttf  16 fonts/monor16.py
$FTP tokens/src/fonts/IBMPlexMono-Bold.ttf     16 fonts/monob16.py
```

Generated font files in `fonts/` are committed to the repo and deployed to the Pico. The TTF source files in `tokens/src/fonts/` are committed under the [OFL licence](tokens/src/fonts/OFL.txt) — font regeneration is only needed if you add a new font or size.

---

## Structure

```
pico-ui-kit/
├── tokens/
│   ├── src/                  ← Figma JSON exports + TTF font sources (not committed)
│   │   ├── 01-primitive/
│   │   ├── 02-Semantic/
│   │   ├── 03-viewports/
│   │   └── fonts/            ← IBMPlexMono-*.ttf (download from Google Fonts)
│   ├── build_tokens.py       ← run after re-exporting from Figma
│   ├── primitive.py          ← generated — raw color/number values
│   ├── semantic.py           ← generated — named role aliases over primitives
│   └── viewport.py           ← generated — spacing, type scale, radii for active viewport
├── fonts/                    ← generated bitmap font modules (deployed to Pico)
│   ├── monor8.py             ← IBM Plex Mono Regular 8px
│   ├── monob8.py             ← IBM Plex Mono Bold 8px
│   ├── monor16.py            ← IBM Plex Mono Regular 16px
│   └── monob16.py            ← IBM Plex Mono Bold 16px
├── drawing/
│   ├── text.py               ← write(), text_w(), text_h()
│   ├── rect.py               ← fill_rect(), hline(), vline()
│   └── line.py               ← hline(), vline(), dot()
├── components/
│   ├── badge.py              ← badge()
│   └── spell_card.py         ← spell_card()
└── simulator/
    ├── display.py            ← Pygame Display — same API as real ST7789 driver
    └── run.py                ← entry point: runs built-in demo or a screen file
```

No component is written until a screen requires it.

---

## Token layers

```
Figma variables
    ↓  export JSON to tokens/src/
    ↓  python tokens/build_tokens.py [--mode N] [--theme light|dark] [--viewport xs]

primitive.py    raw values — colors as (r,g,b), numbers as int px
    ↓  from tokens.primitive import *

semantic.py     named role aliases — ACTION_PRIMARY_BACKGROUND_BASE = COLOUR_BRAND_...
    ↓  from tokens.semantic import *

viewport.py     viewport-scaled spacing, type scale, radii — GAP_4, FONT_SIZE_BODY_1X, RADIUS_XS
    ↓  from tokens.viewport import *

drawing/ + components/    always import from semantic or viewport, never primitive directly
```

Figma is the single source of truth. Never edit `primitive.py`, `semantic.py`, or `viewport.py` by hand.

### Build options

Three independent flags control what gets generated. Combine any of them freely:

```bash
python tokens/build_tokens.py                                    # mode 1, light, xs  (all defaults)
python tokens/build_tokens.py --mode 2                           # switch colour palette
python tokens/build_tokens.py --theme dark                       # light or dark
python tokens/build_tokens.py --viewport sm                      # change display size
python tokens/build_tokens.py --mode 2 --theme dark --viewport sm  # all three
```

#### Mode (colour palette)

A **mode** selects which primitive colour palette to build from — it is the closest equivalent to a "brand" in a web design system. Each mode corresponds to one file in `tokens/src/01-primitive/`.

| Mode | File | Notes |
|---|---|---|
| `1` | `Mode 1.json` | Default |
| `2` | `Mode 2.json` | Add to `01-primitive/` to unlock |
| `N` | `Mode N.json` | As many as you need |

Adding a new mode: export a new `Mode N.json` from Figma Variables and place it in `tokens/src/01-primitive/`. No changes to `02-Semantic/` are needed — the semantic layer resolves references against whichever mode is active.

> **Mode vs theme:** These are two different things. **Mode** = which colour palette (e.g. dark-fantasy vs sci-fi vs nature). **Theme** = light or dark surface treatment applied on top of any mode.

#### Theme (light / dark)

```bash
python tokens/build_tokens.py --theme dark   # regenerate semantic.py for dark surfaces
```

`02-Semantic/Light.json` and `Dark.json` are shared across all modes — they define colour roles (e.g. `ACTION_PRIMARY_BACKGROUND_BASE`) that point to whatever primitives the active mode provides.

#### Viewport

| Viewport | Usage |
|---|---|
| `xs` | Raspberry Pi Pico 240×135 (default) |
| `sm` | Small dashboard display |
| `md` | Medium dashboard display |
| `lg` | Large display |
| `xl` | Extra large display |

```bash
python tokens/build_tokens.py --viewport sm  # regenerate viewport.py for a larger display
```

Switching viewport regenerates `viewport.py` with the correct spacing, type scale, and radii. Colours and semantic tokens are viewport-independent.

### Token names in components

| Want | Import from |
|---|---|
| A color by role | `tokens.semantic` — e.g. `ACTION_PRIMARY_BACKGROUND_BASE` |
| Spacing / type scale / radii | `tokens.viewport` — e.g. `GAP_4`, `FONT_SIZE_BODY_1X`, `RADIUS_XS` |
| Raw value (rare) | `tokens.primitive` — e.g. `COLOUR_NEUTRAL_950` |

---

## Desktop Simulator

A Pygame-based simulator lets you preview screens on your desktop at 3× scale (720×405 px) without touching the Pico. Components render identically — the only difference is the `Display` object they receive.

```
simulator/
├── display.py    # Pygame Display stub — same API as the real ST7789 driver
└── run.py        # entry point: point at any screen file to preview it
```

### How it works

Components never import the hardware driver directly. They receive a `Display` object as an argument. On-device that object is the real ST7789 driver. In the simulator it is a Pygame surface with the same method signatures.

```
Real device:  main.py  → Display(st7789)      → SPI → LCD
Desktop:      run.py   → Display(simulator)   → Pygame window
```

### Running a preview

```bash
# 1. Install pygame (desktop only — one time)
pip install pygame

# 2. Run the built-in spell card demo
cd path/to/pico-ui-kit
python3 simulator/run.py

# 3. Run a specific screen file
python3 simulator/run.py path/to/my_screen.py
```

> **macOS note:** run from your terminal directly — Pygame windows launched from background processes may not appear.

The window opens at 720×405 (3× the Pico display). Keyboard keys map to the physical buttons:

| Key | Pico button |
|---|---|
| `A` | A |
| `B` | B |
| Arrow keys | Joystick |
| `Space` | Centre / CTR |
| `S` | Shake (trigger IMU event) |
| `Esc` | Quit |

### Dependency

The simulator requires `pygame` on the desktop only. It is never deployed to the Pico.

---

## Using this library

pico-ui-kit is a plain Python library — there is no package manager step. The components, fonts, and token modules are source files you deploy alongside your own code.

### Option A — Git submodule (recommended)

Add pico-ui-kit as a submodule inside your project repo:

```bash
git submodule add https://github.com/YOUR_USERNAME/pico-ui-kit
```

Then in your screen files, adjust `sys.path` so imports resolve:

```python
import sys
sys.path.insert(0, "/path/to/pico-ui-kit")   # desktop
# On Pico hardware: copy the pico-ui-kit folder to the device root
```

Update to the latest version at any time:

```bash
git submodule update --remote pico-ui-kit
```

### Option B — MicroPython Package Manager (mip)

From the Pico REPL or in a boot script, install directly from GitHub:

```python
import mip
mip.install("github:YOUR_USERNAME/pico-ui-kit")
```

This copies only the deployed files (drawing, components, fonts, tokens) — not the simulator or build scripts. Re-run to update.

### Option C — Manual copy

Download the repo and copy the following folders to your Pico (via Thonny, mpremote, or rshell):

```
drawing/
components/
fonts/
tokens/primitive.py
tokens/semantic.py
tokens/viewport.py
tokens/__init__.py
```

The `simulator/`, `tokens/src/`, and `tokens/build_tokens.py` are desktop-only and do not belong on the device.

### Token customisation

The committed `tokens/primitive.py`, `tokens/semantic.py`, and `tokens/viewport.py` reflect Mode 1 / Light / XS — suitable for a 240×135 Pico display out of the box.

To customise (e.g. switch mode, use dark theme, target a larger display):

1. Clone the repo locally
2. Export your token JSON files from Figma into `tokens/src/`
3. Run the build script with your chosen options (see [Build options](#build-options))
4. Deploy the regenerated `.py` files to your Pico

---

## Projects using pico-ui-kit

| Project | Repo |
|---|---|
| SpellSpinner | [pico-spellspinner](https://github.com/YOUR_USERNAME/pico-spellspinner) |
