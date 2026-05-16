import fonts.monob16 as _bold16
import fonts.monor8  as _reg8

from components.badge import badge
from drawing.text import word_wrap
from tokens.semantic import (
    STRUCTURE_SURFACES_LEVEL_0,
    TEXT_COLOUR_PRIMARY,
    TEXT_COLOUR_SECONDARY,
    STRUCTURE_BORDERS_LEVEL_3,
    STRUCTURE_BORDERS_LEVEL_4,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_001,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_002,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_003,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_004,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_005,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_006,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_007,
    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_008,
    COMMUNICATION_MARKERS_SEMANTIC_DEFAULT_BACKGROUND_NEUTRAL,
)
from tokens.viewport import GAP_2, GAP_3, GAP_4

# ── School → accent color mapping ────────────────────────────────────────────
# Each school maps to a badge category string and a solid bar color token.

_SCHOOL_ACCENT = {
    'Necromancy':    '001',   # rose
    'Transmutation': '002',   # pink
    'Enchantment':   '003',   # fuchsia
    'Conjuration':   '004',   # purple
    'Divination':    '005',   # indigo
    'Abjuration':    '006',   # sky
    'Illusion':      '007',   # teal
    'Evocation':     '008',   # emerald
}

_SCHOOL_BAR = {
    'Necromancy':    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_001,
    'Transmutation': COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_002,
    'Enchantment':   COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_003,
    'Conjuration':   COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_004,
    'Divination':    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_005,
    'Abjuration':    COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_006,
    'Illusion':      COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_007,
    'Evocation':     COMMUNICATION_MARKERS_ACCENT_DEFAULT_BACKGROUND_008,
}

_BAR_FALLBACK = COMMUNICATION_MARKERS_SEMANTIC_DEFAULT_BACKGROUND_NEUTRAL


def _accent(spell):
    return _SCHOOL_ACCENT.get(spell.get('school', ''), 'neutral')


def _bar_color(spell):
    return _SCHOOL_BAR.get(spell.get('school', ''), _BAR_FALLBACK)


# ── Color aliases ─────────────────────────────────────────────────────────────

_BG        = STRUCTURE_SURFACES_LEVEL_0
_TEXT_PRI  = TEXT_COLOUR_PRIMARY
_TEXT_SEC  = TEXT_COLOUR_SECONDARY
_SEPARATOR = STRUCTURE_BORDERS_LEVEL_3
_ICON_PH   = STRUCTURE_BORDERS_LEVEL_4   # school icon placeholder outline

# ── Layout ───────────────────────────────────────────────────────────────────
# Screen: 240×135. All measurements in pixels.

_PAD    = GAP_4   # 12px edge padding
_GAP2   = GAP_2   # 4px
_GAP3   = GAP_3   # 8px — between icon and text column
_BAR_W  = 40      # accent underline width (Figma-measured)
_BAR_H  = 2       # accent underline height

_BADGE_H  = _reg8.height() + 8   # 8px font + 4px top + 4px bottom = 16px
_ICON_W   = 43                    # icon area width (matches Figma 43px container)
_TEXT_X   = _PAD + _ICON_W + _GAP3  # 63 — text column x-start

# Three rows spaced with justify-between over 111px content area.
# Row heights: row1=16, row2=43 (icon-driven), row3=16. Gaps: (111-75)/2 = 18px.
_ROW1_Y   = _PAD                        # 12
_ROW2_Y   = _PAD + _BADGE_H + 18       # 46
_ROW3_Y   = 135 - _PAD - _BADGE_H      # 107

# Text column content (34px) centered in 43px row2 — 4px top offset.
_NAME_Y   = _ROW2_Y + (43 - 34) // 2   # 50
_BAR_Y    = _NAME_Y + _bold16.height() + _GAP2   # 70
_META_Y   = _BAR_Y + _BAR_H + _GAP2    # 76


def spell_card(display, spell, font_bold=_bold16, font_reg=_reg8):
    """
    Render a spell card onto display.

    spell dict keys:
      name, level, ritual (bool), components (str e.g. "V, S, M"),
      casting_time, use, page, classes (list of str), school (str, optional).
    """
    display.fill(_BG)

    _draw_top_row(display, spell, font_reg)
    _draw_middle_row(display, spell, font_bold, font_reg)
    _draw_bottom_row(display, spell, font_reg)


def _draw_top_row(display, spell, font):
    x = _PAD
    acc = _accent(spell)

    # Level badge — school accent, subtle
    level = str(spell.get("level", ""))
    x += badge(display, font, level, x, _ROW1_Y, category=acc, emphasis='subtle')

    # Ritual badge — school accent, ghost; only shown when ritual=True
    if spell.get("ritual"):
        x += _GAP3
        badge(display, font, "R", x, _ROW1_Y, category=acc, emphasis='subtle')

    # Component badges — always neutral, right-aligned
    components = []
    if spell.get('v'): components.append('V')
    if spell.get('s'): components.append('S')
    if spell.get('m'): components.append('M')
    _draw_badges_right(display, font, components, _ROW1_Y, 'neutral')


def _draw_middle_row(display, spell, font_bold, font_reg):
    _draw_school_icon(display, spell.get("school", ""))

    # Spell name — wrap to 2 lines if needed
    chars_per_line = (240 - _TEXT_X - _PAD) // font_bold.max_width()
    lines = word_wrap(spell["name"], chars_per_line)
    for i, line in enumerate(lines):
        display.write(font_bold, line, _TEXT_X, _NAME_Y + i * font_bold.height(), _TEXT_PRI, _BG)

    # Accent bar and meta row shift down by one line height if name wrapped
    name_h  = font_bold.height() * len(lines)
    bar_y   = _NAME_Y + name_h + _GAP2
    meta_y  = bar_y + _BAR_H + _GAP2

    # Accent bar — school color
    display.fill_rect(_TEXT_X, bar_y, _BAR_W, _BAR_H, _bar_color(spell))

    # Meta row: casting_time · use
    x = _TEXT_X
    ct = spell.get("casting_time", "")
    display.write(font_reg, ct, x, meta_y, _TEXT_SEC, None)
    x += font_reg.max_width() * len(ct) + _GAP2
    dot_y = meta_y + (font_reg.height() - 2) // 2
    display.fill_rect(x, dot_y, 2, 2, _SEPARATOR)
    x += 2 + _GAP2
    display.write(font_reg, spell.get("use", ""), x, meta_y, _TEXT_SEC, None)


def _draw_bottom_row(display, spell, font):
    # Class badges — uncomment to re-enable
    # x = _PAD
    # for i, cls in enumerate(spell.get("classes", [])):
    #     if i > 0:
    #         x += _GAP2
    #         dot_y = _ROW3_Y + (_BADGE_H - 2) // 2
    #         display.fill_rect(x, dot_y, 2, 2, _SEPARATOR)
    #         x += 2 + _GAP2
    #     x += badge(display, font, cls, x, _ROW3_Y)

    # Page badge — ghost, right-aligned
    page_str = "p." + str(spell.get("page", ""))
    page_w = max(20, font.max_width() * len(page_str) + 8)
    badge(display, font, page_str, 240 - _PAD - page_w, _ROW3_Y)


def _draw_badges_right(display, font, labels, y, category='neutral'):
    """Draw ghost badges right-aligned with dot separators."""
    if not labels:
        return
    badge_widths = [max(20, font.max_width() * len(l) + 8) for l in labels]
    sep_w = _GAP2 + 2 + _GAP2   # gap + 2px dot + gap = 10px
    total = sum(badge_widths) + (len(labels) - 1) * sep_w
    x = 240 - _PAD - total
    for i, (label, w) in enumerate(zip(labels, badge_widths)):
        if i > 0:
            x += _GAP2
            dot_y = y + (_BADGE_H - 2) // 2
            display.fill_rect(x, dot_y, 2, 2, _SEPARATOR)
            x += 2 + _GAP2
        badge(display, font, label, x, y, category=category, emphasis='ghost')
        x += w


def _draw_school_icon(display, school):
    color = _SCHOOL_BAR.get(school, _BAR_FALLBACK)

    try:
        from school_icons import ICONS
        entry = ICONS.get(school)
    except ImportError:
        entry = None

    if entry:
        w, h, bitmap = entry
        ix = _PAD + (43 - w) // 2
        iy = _ROW2_Y + (43 - h) // 2
        row_bytes = (w + 7) // 8
        for row in range(h):
            for col in range(w):
                idx = row * row_bytes + col // 8
                if bitmap[idx] & (1 << (7 - col % 8)):
                    display.pixel(ix + col, iy + row, color)
    else:
        # Fallback outline placeholder
        ix = _PAD + (43 - 32) // 2
        iy = _ROW2_Y + (43 - 22) // 2
        display.hline(ix, iy,      32, _ICON_PH)
        display.hline(ix, iy + 21, 32, _ICON_PH)
        for dy in range(22):
            display.pixel(ix,      iy + dy, _ICON_PH)
            display.pixel(ix + 31, iy + dy, _ICON_PH)
