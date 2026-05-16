# pico-ui-kit

A simple UI kit for MicroPython. Build consistent, well-designed interfaces on any colour display — without reinventing colours, spacing, and typography for every project.

The design decisions are already made and baked into the component library. Drop in your display driver, pick a viewport for your screen size, and start building on any MicroPython board.

This started as a personal project and is open sourced for anyone who wants a solid UI foundation for their Pico builds. Contributions are welcome.

---

## Features

- **Display-agnostic** — works with any colour display driver (ST7789, ILI9341, GC9A01, and others) via a simple adapter
- **Light & dark colour mode** — both built together for every theme; switch by writing a config file to flash and resetting — no rebuild needed
- **Viewport system** — tune spacing and type scale to match your screen size (xs → xl)
- **Desktop simulator** — preview and iterate on your screens without touching the hardware
- **Bitmap fonts** — IBM Plex Mono Regular and Bold at 8px and 16px, ready to deploy to the device
- **Component library** — growing set of ready-to-use UI components
- **Any MicroPython board** — not tied to a specific chip or device

---

## Roadmap

- **More colour themes** — additional colour palettes beyond the default
- **More components** — buttons, progress bars, lists, and icons
- **Monochrome & e-paper support** — SSD1306 OLED and e-ink panels

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
├── adapter.py                ← DisplayAdapter — wraps any driver for use with components
├── mode.cfg                  ← optional — write 'light' or 'dark' to select colour mode at boot
├── tokens/
│   ├── src/
│   │   ├── 01-primitive/     ← token source JSON (not committed)
│   │   ├── 02-Semantic/      ← token source JSON (not committed)
│   │   ├── 03-viewports/     ← token source JSON (not committed)
│   │   └── fonts/            ← IBMPlexMono-*.ttf — committed under OFL licence
│   ├── build_tokens.py       ← run to regenerate token modules
│   ├── primitive.py          ← generated — raw color/number values
│   ├── semantic_light.py     ← generated — light theme role aliases over primitives
│   ├── semantic_dark.py      ← generated — dark theme role aliases over primitives
│   ├── semantic.py           ← generated shim — delegates to tokens/theme.py
│   ├── colormode.py          ← boot-time colour mode loader (reads mode.cfg)
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
│   └── badge.py              ← badge()
└── simulator/
    ├── display.py            ← Pygame Display — same interface as DisplayAdapter
    └── run.py                ← entry point: runs built-in demo or a screen file
```

No component is written until a screen requires it.

---

## Token layers

```
Token source JSON  (tokens/src/)
    ↓  python tokens/build_tokens.py [--theme N] [--viewport xs]

primitive.py         raw values — colors as (r,g,b), numbers as int px
    ↓  from tokens.primitive import *          (one palette per theme)

semantic_light.py    light colour-mode aliases — ACTION_PRIMARY_BACKGROUND_BASE = COLOUR_BRAND_...
semantic_dark.py     dark colour-mode aliases  — same names, different primitives

colormode.py         reads mode.cfg at boot → imports semantic_light or semantic_dark

semantic.py          shim — from tokens.colormode import *
    ↓  from tokens.semantic import *

viewport.py          viewport-scaled spacing, type scale, radii — GAP_4, FONT_SIZE_BODY_1X, RADIUS_XS
    ↓  from tokens.viewport import *

drawing/ + components/    always import from semantic or viewport, never primitive directly
```

Never edit `primitive.py`, `semantic_light.py`, `semantic_dark.py`, or `viewport.py` by hand. `colormode.py` is hand-written and not regenerated.

### Build options

Two independent flags control what gets generated. Combine freely:

```bash
python tokens/build_tokens.py                          # theme 1, xs  (all defaults)
python tokens/build_tokens.py --theme 2                # switch colour theme
python tokens/build_tokens.py --viewport sm            # change display size
python tokens/build_tokens.py --theme 2 --viewport sm  # both
```

Both light and dark colour modes are **always generated together** — the build produces `semantic_light.py` and `semantic_dark.py` in one pass. Colour mode selection at runtime is handled by `tokens/colormode.py` — see [Colour mode](#colour-mode-light--dark).

#### Theme (colour palette)

A **theme** is a complete colour palette — the set of primitive values that flows into everything else. Each theme corresponds to one file in `tokens/src/01-primitive/`.

| Theme | File | Notes |
|---|---|---|
| `1` | `Mode 1.json` | Default |
| `2` | `Mode 2.json` | Add to `01-primitive/` to unlock |
| `N` | `Mode N.json` | As many as you need |

Adding a new theme: place a new `Mode N.json` in `tokens/src/01-primitive/`. No changes to `02-Semantic/` are needed — the semantic layer resolves references against whichever theme is active.

> **Theme vs colour mode:** These are two different things. **Theme** = which colour palette (e.g. dark-fantasy vs sci-fi vs nature). **Colour mode** = light or dark surface treatment applied on top of any theme.

#### Viewport

| Viewport | Usage |
|---|---|
| `xs` | Smallest — tightest spacing, smallest type (default; suits 240×135 and similar) |
| `sm` | Small display |
| `md` | Medium display |
| `lg` | Large display |
| `xl` | Extra large display |

```bash
python tokens/build_tokens.py --viewport sm  # regenerate viewport.py for a larger display
```

Switching viewport regenerates `viewport.py` with the correct spacing, type scale, and radii. Colours and semantic tokens are viewport-independent.

### Colour mode (light / dark)

Each theme ships with two semantic files: `semantic_light.py` and `semantic_dark.py`. Both are deployed to the device. `tokens/colormode.py` reads a plain text file called `mode.cfg` from the root of the filesystem at boot and loads the matching one. If `mode.cfg` is absent, light is used.

**Switching colour mode on the Pico:**

```python
# Run this once in the REPL — then reset (Ctrl+D) to apply
with open('mode.cfg', 'w') as f:
    f.write('dark')
```

```python
# Switch back to light
with open('mode.cfg', 'w') as f:
    f.write('light')
```

Or delete `mode.cfg` entirely to revert to the default (light).

**In your own app code**, wire this into a toggle button:

```python
def toggle_colormode():
    try:
        with open('mode.cfg') as f:
            current = f.read().strip()
    except OSError:
        current = 'light'
    next_mode = 'dark' if current == 'light' else 'light'
    with open('mode.cfg', 'w') as f:
        f.write(next_mode)
    import machine
    machine.reset()  # reset applies the new colour mode
```

**In the simulator**, place a `mode.cfg` file in the `pico-ui-kit/` project root:

```bash
echo 'dark' > mode.cfg          # use dark colour mode in simulator
rm mode.cfg                      # revert to light (default)
```

> `mode.cfg` is gitignored — it is per-device and should not be committed.

**RAM cost:** only one semantic module is loaded at a time. `semantic_light.py` and `semantic_dark.py` sit on flash; the inactive one uses no RAM.

### Token names in components

| Want | Import from |
|---|---|
| A color by role | `tokens.semantic` — e.g. `ACTION_PRIMARY_BACKGROUND_BASE` |
| Spacing / type scale / radii | `tokens.viewport` — e.g. `GAP_4`, `FONT_SIZE_BODY_1X`, `RADIUS_XS` |
| Raw value (rare) | `tokens.primitive` — e.g. `COLOUR_NEUTRAL_950` |

---

## Desktop Simulator

A Pygame-based simulator lets you preview screens on your desktop at 3× scale without touching the Pico. Components render identically — the only difference is the `Display` object they receive.

```
simulator/
├── display.py    # Pygame Display — same interface as DisplayAdapter
└── run.py        # entry point: point at any screen file to preview it
```

### How it works

Components never import the hardware driver directly. They receive a display object as an argument. On-device that object is a `DisplayAdapter` wrapping your real driver. In the simulator it is a Pygame surface with the same method signatures.

```
Real device:  main.py  → DisplayAdapter(driver, w, h)  → SPI → LCD
Desktop:      run.py   → Display(width, height)         → Pygame window
```

### Running a preview

```bash
# 1. Install pygame (desktop only — one time)
pip install pygame

# 2. Run the built-in badge demo (240×135 default)
cd path/to/pico-ui-kit
python3 simulator/run.py

# 3. Preview at a different display size
python3 simulator/run.py --width 320 --height 240

# 4. Run a specific screen file
python3 simulator/run.py path/to/my_screen.py
python3 simulator/run.py path/to/my_screen.py --width 320 --height 240
```

> **macOS note:** run from your terminal directly — Pygame windows launched from background processes may not appear.

The window opens at 3× the display resolution. Keyboard keys map to the physical buttons:

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

## Display interface

All components receive a display object as their first argument. On device this is a `DisplayAdapter` wrapping your hardware driver. In the simulator it is `simulator.Display`. Both expose the same interface:

| Method | Description |
|---|---|
| `fill(color)` | Fill the entire screen |
| `fill_rect(x, y, w, h, color)` | Draw a filled rectangle |
| `hline(x, y, w, color)` | Draw a horizontal line |
| `vline(x, y, h, color)` | Draw a vertical line |
| `pixel(x, y, color)` | Set a single pixel |
| `write(font, text, x, y, fg, bg)` | Render a bitmap font string |
| `show()` | Flush frame to screen (if driver requires it) |
| `width` | Display width in pixels |
| `height` | Display height in pixels |

`DisplayAdapter` provides a pixel-by-pixel `write()` fallback for drivers that do not have one, so any driver supporting the first five methods is compatible.

### Wiring up on hardware

```python
from adapter import DisplayAdapter
import st7789  # replace with your display driver

# Set up your driver as usual
raw = st7789.ST7789(spi, dc=Pin(8), cs=Pin(9), rst=Pin(10), width=240, height=135)

# Wrap it
display = DisplayAdapter(raw, width=240, height=135)

# Use any component
from components.badge import badge
import fonts.monor8 as font

badge(display, font, "OK", 10, 10)
display.show()
```

The `width` and `height` you pass to `DisplayAdapter` should match the viewport you built your tokens for — they are available as `display.width` and `display.height` in your screen code.

---

## Using this library

pico-ui-kit is a plain Python library — there is no package manager step. The components, fonts, token modules, and `adapter.py` are source files you deploy alongside your own code.

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

Download the repo and copy the following to your Pico (via Thonny, mpremote, or rshell):

```
adapter.py
drawing/
components/
fonts/
tokens/primitive.py
tokens/semantic_light.py
tokens/semantic_dark.py
tokens/semantic.py
tokens/colormode.py
tokens/viewport.py
tokens/__init__.py
```

The `simulator/`, `tokens/src/`, and `tokens/build_tokens.py` are desktop-only and do not belong on the device.

### Token customisation

The committed token files reflect Mode 1 / XS — suitable for a 240×135 Pico display out of the box. Both light and dark themes are always included.

For other customisation (viewport or colour theme), the token source files and build script are included in the repository — see [Build options](#build-options).

To switch between light and dark on a deployed device, see [Colour mode](#colour-mode-light--dark) — no rebuild needed.

---

## Projects using pico-ui-kit

| Project | Repo |
|---|---|
| SpellSpinner | [pico-spellspinner](https://github.com/YOUR_USERNAME/pico-spellspinner) |
