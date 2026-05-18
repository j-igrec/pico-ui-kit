# Changelog

All notable changes to pico-ui-kit are documented here.

## [0.0.2] - 2026-05-18

### Breaking changes
- **Badge API rewrite.** Props renamed to match Figma 1:1:
  - `category` removed — split into `colour` (`'001'..'009'` | semantic name) and `type` (`'accent'`|`'semantic'`)
  - Positional `text` renamed to `badge_label`
  - Default emphasis changed from `'ghost'` to `'default'`
  - New `status_dot=True` and `icon=True` props (accept `None` / `True` / `False` or an icon module)
- **Font family swapped:** IBM Plex Mono → Silkscreen. Module names (`monor8`, `monob8`, `monor16`, `monob16`) and import paths unchanged, but glyph shapes, widths, and bitmap heights are all different (9px / 15px instead of 8 / 16 due to Silkscreen's native metrics).
- **Token namespace updates** (regenerated from new Figma export):
  - `Line-height/Body/1x`: 8 → 10 (matches Silkscreen bitmap)
  - `Line-height/Body/2x`: 16 (unchanged value, now sourced from a primitive matching the Silkscreen 16px bitmap)
  - Transparent border tokens removed from `Communication/Markers/*` — every variant that previously declared a transparent border now declares none
  - StatusDot's `Subtle` emphasis dropped — only `Default` exists

### Added
- **`components/status_dot.py`** — new 4×4 status dot component. Variants: `type` × `colour` (10 accent + 6 semantic).
- **`components/button.py`** — new Button component. Variants: `type` (`primary` | `secondary`) × `state` (`default` | `focus` | `hover` | `pressed` | `disabled`) × `icon_only` × `lead_icon` × `trail_icon`. Includes layout-neutral 2px focus ring rendered 3px outside the button bbox.
- **Icon pipeline:**
  - `icons/` directory with 118 generated 1-bit bitmap modules (116 Lucide + 2 custom A/B button glyphs).
  - `icons/build_icons.py` script that converts PNGs in `icons/src/` (gitignored) into MicroPython modules. Strips Figma's `, Size=8px` export suffix and the variant-prefix `Icon=`.
  - `drawing/icon.py` with `draw_icon(display, icon, x, y, fg, bg=None)` — same render model as text (1-bit silhouette + token colour at draw time).
- **`Action/Primary/*` and `Action/Secondary/*` token namespaces** for button colours (5 states × bg / border / fg, plus width + radius).
- **`Communication/Highlights/Border/Subtle`** token for the button focus ring.
- **`Radius/sm` (= 4)** for badge corner radius. **`Radius/null` (= 0)** for status dot.
- **Simulator demos:** `simulator/demo_status_dots.py`, `simulator/demo_buttons.py`.

### Changed
- **Badge geometry now matches Figma exactly:**
  - Pill-ish shape via `RADIUS_SM = 4` clamped to `h // 2`.
  - Even-height rule: badge height = 14 (was 13). Achieved by rounding the font bitmap up to an even line-height (`font.height() + font.height() % 2`).
  - Asymmetric padding (`PADDING_1 = 2` vertical, `PADDING_2 = 4` horizontal) replacing the old uniform `PADDING_2` on all sides.
  - Hugs the label tightly: `drawing/text.text_w()` now sums actual glyph widths instead of `font.max_width() * len(text)`.
- **`drawing/text.text_w()`** is now variable-pitch aware (sums real glyph widths). Previously over-estimated by 1–2px per character.
- **`drawing/rect.fill_rounded_rect` and `rounded_rect`** rewritten to use a doubled-integer quarter-circle approximation (no `sqrt`, MicroPython-friendly).

### Fixed
- **`fill_rounded_rect` was drawing corners pointing inward** instead of outward — the corner-row widths were inverted relative to the body fill. Affected badges and any future rounded-corner component.
- **`status_dot` no longer crashes** with `KeyError` when `type` and `colour` mismatch (e.g. `colour='success', type='accent'`). The colour family is auto-derived; `type` is retained for Figma 1:1 parity but is no longer load-bearing.
- **Badge no longer crashes** when delegating to the inline status dot with mismatched colour + type.
- **`button` no longer computes `text_w(label)` twice per render** — cached.
- **`icons/build_icons.py` no longer breaks** when `icons/copy.py` shadows Python's stdlib `copy` module that Pillow imports internally. Build script strips `icons/` from `sys.path` before importing anything.

### Removed
- `icon_w()` and `icon_h()` from `drawing/icon.py` — unused wrappers around `icon.width()` / `icon.height()`.
- `_FOCUS_RING_WIDTH` constant in `components/button.py` — unused.
- StatusDot `subtle` emphasis — no longer in Figma (was always visually broken at 4×4).

### Internal
- `draw_icon` inner pixel loop micro-optimised: `col >> 3` / `col & 7` instead of `// 8` / `% 8`; `len(raw)` and `row * row_bytes` hoisted out of the inner loop.
- Cached `font.height()` and `status_dot_size()` in badge / button hot paths (were called 2–4× per render).

## [0.0.1] - 2026-05-16

### Added
- Scaffolded entire project: components/, drawing/, fonts/, simulator/, tokens/
- badge.py component
- Drawing primitives: line.py, rect.py, text.py
- IBM Plex Mono font files (8/16px, regular/bold)
- Token system with build_tokens.py, primitive.py, semantic.py
- Simulator (display.py, run.py)
- adapter.py (DisplayAdapter abstraction)
- tokens/colormode.py
- Split semantic tokens into semantic_light.py / semantic_dark.py
- CHANGELOG.md, __init__.py with version metadata, release.sh

### Changed
- Refactored semantic.py and build_tokens.py
- Updated simulator
- Major README.md rewrite

### Removed
- components/spell_card.py (moved to consuming project)
- tokens/src/ JSON source files (now gitignored)
- tokens/viewport.py
