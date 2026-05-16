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

Generated font files in `fonts/` are committed to the repo and deployed to the Pico. The TTF source files in `tokens/src/fonts/` are not committed (add to `.gitignore`).

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
    ↓  python tokens/build_tokens.py [--viewport xs]

primitive.py    raw values — colors as (r,g,b), numbers as int px
    ↓  from tokens.primitive import *

semantic.py     named role aliases — ACTION_PRIMARY_BACKGROUND_BASE = COLOUR_BRAND_...
    ↓  from tokens.semantic import *

viewport.py     viewport-scaled spacing, type scale, radii — GAP_4, FONT_SIZE_BODY_1X, RADIUS_XS
    ↓  from tokens.viewport import *

drawing/ + components/    always import from semantic or viewport, never primitive directly
```

Figma is the single source of truth. Never edit `primitive.py`, `semantic.py`, or `viewport.py` by hand.

### Viewports

| Viewport | Usage |
|---|---|
| `xs` | Raspberry Pi Pico 240×135 (default) |
| `sm` | Small dashboard display |
| `md` | Medium dashboard display |
| `lg` | Large display |
| `xl` | Extra large display |

```bash
python tokens/build_tokens.py               # xs (default)
python tokens/build_tokens.py --viewport sm # switch to sm
```

Switching viewport regenerates `viewport.py` with the correct spacing, type scale, and radii. Colors and semantic tokens are viewport-independent and never change.

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
cd /Users/jaysonigrec/vault/pico-ui-kit
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

## Consumer projects

| Project | Repo |
|---|---|
| SpellSpinner | `vault/pico-spellspinner` |
