from drawing.rect import fill_rounded_rect, rounded_rect
from drawing.text import text_w as _text_w
from drawing.icon import draw_icon as _draw_icon

from tokens.semantic import (
    ACTION_PRIMARY_BACKGROUND_BASE,
    ACTION_PRIMARY_BACKGROUND_FOCUS,
    ACTION_PRIMARY_BACKGROUND_HOVER,
    ACTION_PRIMARY_BACKGROUND_PRESSED,
    ACTION_PRIMARY_BACKGROUND_DISABLED,
    ACTION_PRIMARY_BORDER_BASE,
    ACTION_PRIMARY_BORDER_FOCUS,
    ACTION_PRIMARY_BORDER_HOVER,
    ACTION_PRIMARY_BORDER_PRESSED,
    ACTION_PRIMARY_BORDER_DISABLED,
    ACTION_PRIMARY_FOREGROUND_BASE,
    ACTION_PRIMARY_FOREGROUND_FOCUS,
    ACTION_PRIMARY_FOREGROUND_HOVER,
    ACTION_PRIMARY_FOREGROUND_PRESSED,
    ACTION_PRIMARY_FOREGROUND_DISABLED,
    ACTION_PRIMARY_BORDER_RADIUS,
    ACTION_PRIMARY_BORDER_WIDTH,
    ACTION_SECONDARY_BACKGROUND_BASE,
    ACTION_SECONDARY_BACKGROUND_FOCUS,
    ACTION_SECONDARY_BACKGROUND_HOVER,
    ACTION_SECONDARY_BACKGROUND_PRESSED,
    ACTION_SECONDARY_BACKGROUND_DISABLED,
    ACTION_SECONDARY_BORDER_BASE,
    ACTION_SECONDARY_BORDER_FOCUS,
    ACTION_SECONDARY_BORDER_HOVER,
    ACTION_SECONDARY_BORDER_PRESSED,
    ACTION_SECONDARY_BORDER_DISABLED,
    ACTION_SECONDARY_FOREGROUND_BASE,
    ACTION_SECONDARY_FOREGROUND_FOCUS,
    ACTION_SECONDARY_FOREGROUND_HOVER,
    ACTION_SECONDARY_FOREGROUND_PRESSED,
    ACTION_SECONDARY_FOREGROUND_DISABLED,
    ACTION_SECONDARY_BORDER_RADIUS,
    ACTION_SECONDARY_BORDER_WIDTH,
    COMMUNICATION_HIGHLIGHTS_BORDER_SUBTLE,
)
from tokens.viewport import PADDING_2, GAP_2

_ICON_SIZE = 8
_FOCUS_RING_OFFSET = 3   # ring sits 3px outside the button on every side
_FOCUS_RING_WIDTH = 2    # 2px thick stroke

_BG = {
    ('primary',   'default'):  ACTION_PRIMARY_BACKGROUND_BASE,
    ('primary',   'focus'):    ACTION_PRIMARY_BACKGROUND_FOCUS,
    ('primary',   'hover'):    ACTION_PRIMARY_BACKGROUND_HOVER,
    ('primary',   'pressed'):  ACTION_PRIMARY_BACKGROUND_PRESSED,
    ('primary',   'disabled'): ACTION_PRIMARY_BACKGROUND_DISABLED,
    ('secondary', 'default'):  ACTION_SECONDARY_BACKGROUND_BASE,
    ('secondary', 'focus'):    ACTION_SECONDARY_BACKGROUND_FOCUS,
    ('secondary', 'hover'):    ACTION_SECONDARY_BACKGROUND_HOVER,
    ('secondary', 'pressed'):  ACTION_SECONDARY_BACKGROUND_PRESSED,
    ('secondary', 'disabled'): ACTION_SECONDARY_BACKGROUND_DISABLED,
}

_BORDER = {
    ('primary',   'default'):  ACTION_PRIMARY_BORDER_BASE,
    ('primary',   'focus'):    ACTION_PRIMARY_BORDER_FOCUS,
    ('primary',   'hover'):    ACTION_PRIMARY_BORDER_HOVER,
    ('primary',   'pressed'):  ACTION_PRIMARY_BORDER_PRESSED,
    ('primary',   'disabled'): ACTION_PRIMARY_BORDER_DISABLED,
    ('secondary', 'default'):  ACTION_SECONDARY_BORDER_BASE,
    ('secondary', 'focus'):    ACTION_SECONDARY_BORDER_FOCUS,
    ('secondary', 'hover'):    ACTION_SECONDARY_BORDER_HOVER,
    ('secondary', 'pressed'):  ACTION_SECONDARY_BORDER_PRESSED,
    ('secondary', 'disabled'): ACTION_SECONDARY_BORDER_DISABLED,
}

_FG = {
    ('primary',   'default'):  ACTION_PRIMARY_FOREGROUND_BASE,
    ('primary',   'focus'):    ACTION_PRIMARY_FOREGROUND_FOCUS,
    ('primary',   'hover'):    ACTION_PRIMARY_FOREGROUND_HOVER,
    ('primary',   'pressed'):  ACTION_PRIMARY_FOREGROUND_PRESSED,
    ('primary',   'disabled'): ACTION_PRIMARY_FOREGROUND_DISABLED,
    ('secondary', 'default'):  ACTION_SECONDARY_FOREGROUND_BASE,
    ('secondary', 'focus'):    ACTION_SECONDARY_FOREGROUND_FOCUS,
    ('secondary', 'hover'):    ACTION_SECONDARY_FOREGROUND_HOVER,
    ('secondary', 'pressed'):  ACTION_SECONDARY_FOREGROUND_PRESSED,
    ('secondary', 'disabled'): ACTION_SECONDARY_FOREGROUND_DISABLED,
}

_RADIUS = {
    'primary':   ACTION_PRIMARY_BORDER_RADIUS,
    'secondary': ACTION_SECONDARY_BORDER_RADIUS,
}

_BORDER_W = {
    'primary':   ACTION_PRIMARY_BORDER_WIDTH,
    'secondary': ACTION_SECONDARY_BORDER_WIDTH,
}


def _is_transparent(c):
    return len(c) == 4 and c[3] == 0


def _is_module(x):
    """True iff x is an icon module (has width/height) rather than None/True/False."""
    return x is not None and x is not True and x is not False


def button(display, font, label, x, y,
           type='primary', state='default',
           icon_only=False, lead_icon=None, trail_icon=None):
    """
    Draw a button and return its width (excluding the focus ring).

    type:       'primary' | 'secondary'
    state:      'default' | 'focus' | 'hover' | 'pressed' | 'disabled'
    icon_only:  True for a fixed 18x18 square button. label & trail_icon are ignored;
                lead_icon (if a module) is rendered centred.
    lead_icon:  None | True (reserve slot) | icon module (draw it). For icon_only mode,
                this is THE icon.
    trail_icon: None | True | icon module. Ignored when icon_only=True.

    Returns the button's inner width in px. The focus ring (when state='focus') extends
    3px outside this width on each side — caller should leave 3px clear around the
    button bounds if buttons may be focused adjacent to other content.
    """
    bg     = _BG[(type, state)]
    border = _BORDER[(type, state)]
    fg     = _FG[(type, state)]
    radius = _RADIUS[type]
    bw     = _BORDER_W[type]

    has_lead  = lead_icon is not None and lead_icon is not False
    has_trail = trail_icon is not None and trail_icon is not False

    # ---- Geometry ----
    if icon_only:
        content_w = _ICON_SIZE
        content_h = _ICON_SIZE
    else:
        font_lh = font.height() + (font.height() % 2)  # round odd bitmap up to even line-height
        text_width = _text_w(font, label)
        content_w = text_width
        if has_lead:
            content_w += _ICON_SIZE + GAP_2
        if has_trail:
            content_w += GAP_2 + _ICON_SIZE
        content_h = max(font_lh, _ICON_SIZE if (has_lead or has_trail) else 0)

    w = content_w + PADDING_2 * 2 + bw * 2
    h = content_h + PADDING_2 * 2 + bw * 2

    # ---- Background fill ----
    if not _is_transparent(bg):
        fill_rounded_rect(display, x, y, w, h, radius, bg)

    # ---- Border outline ----
    if not _is_transparent(border):
        rounded_rect(display, x, y, w, h, radius, border)

    # ---- Content ----
    cx = x + bw + PADDING_2
    cy = y + bw + PADDING_2

    if icon_only:
        if _is_module(lead_icon):
            ix = cx + (_ICON_SIZE - lead_icon.width()) // 2
            iy = cy + (_ICON_SIZE - lead_icon.height()) // 2
            _draw_icon(display, lead_icon, ix, iy, fg)
    else:
        cursor = cx

        if has_lead:
            if _is_module(lead_icon):
                iy = cy + (content_h - lead_icon.height()) // 2
                ix = cursor + (_ICON_SIZE - lead_icon.width()) // 2
                _draw_icon(display, lead_icon, ix, iy, fg)
            cursor += _ICON_SIZE + GAP_2

        text_y = cy + (content_h - font.height()) // 2
        display.write(font, label, cursor, text_y, fg, None if _is_transparent(bg) else bg)
        cursor += _text_w(font, label)

        if has_trail:
            cursor += GAP_2
            if _is_module(trail_icon):
                iy = cy + (content_h - trail_icon.height()) // 2
                ix = cursor + (_ICON_SIZE - trail_icon.width()) // 2
                _draw_icon(display, trail_icon, ix, iy, fg)

    # ---- Focus ring (drawn last so it overlays neighbours' pixels) ----
    if state == 'focus':
        rx = x - _FOCUS_RING_OFFSET
        ry = y - _FOCUS_RING_OFFSET
        rw = w + 2 * _FOCUS_RING_OFFSET
        rh = h + 2 * _FOCUS_RING_OFFSET
        ring_radius = radius
        ring = COMMUNICATION_HIGHLIGHTS_BORDER_SUBTLE
        # 2px stroke = two concentric outlines, 1px apart
        rounded_rect(display, rx, ry, rw, rh, ring_radius, ring)
        if ring_radius > 0:
            rounded_rect(display, rx + 1, ry + 1, rw - 2, rh - 2, ring_radius - 1, ring)
        else:
            rounded_rect(display, rx + 1, ry + 1, rw - 2, rh - 2, 0, ring)

    return w
