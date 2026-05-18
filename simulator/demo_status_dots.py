"""Visual smoke test for the Silkscreen font + status_dot + icon-enabled badges.

Run:
    python3 simulator/run.py simulator/demo_status_dots.py
"""

from tokens.semantic import STRUCTURE_SURFACES_LEVEL_0
from components.badge import badge
from components.status_dot import status_dot
import fonts.monor8 as reg8

import icons.check as ic_check
import icons.bell as ic_bell
import icons.triangle_alert as ic_warn
import icons.circle_alert as ic_err


_ACCENT_COLOURS = ['001', '002', '003', '004', '005', '006', '007', '008', '009']
_SEMANTIC_COLOURS = ['neutral', 'success', 'warning', 'error', 'information', 'attention']


def draw(display):
    display.fill(STRUCTURE_SURFACES_LEVEL_0)

    # ── Status dots: accent 001..009 + focus ──
    y = 6
    x = 8
    for col in _ACCENT_COLOURS:
        status_dot(display, x, y, colour=col, type='accent')
        x += 10
    status_dot(display, x, y, colour='focus', type='accent')

    # ── Status dots: semantic ──
    y += 12
    x = 8
    for col in _SEMANTIC_COLOURS:
        status_dot(display, x, y, colour=col, type='semantic')
        x += 10

    # ── Badges with real icons: default emphasis ──
    y += 14
    x = 8
    rows = [
        ('neutral',     'Info', ic_bell),
        ('success',     'Done', ic_check),
        ('warning',     'Warn', ic_warn),
        ('error',       'Stop', ic_err),
    ]
    for col, label, ic in rows:
        w = badge(display, reg8, label, x, y,
                  colour=col, emphasis='default', type='semantic', icon=ic)
        x += w + 4

    # ── Badges with icons: subtle emphasis ──
    y += 18
    x = 8
    for col, label, ic in rows:
        w = badge(display, reg8, label, x, y,
                  colour=col, emphasis='subtle', type='semantic', icon=ic)
        x += w + 4

    # ── Badges with icons: ghost emphasis ──
    y += 18
    x = 8
    for col, label, ic in rows:
        w = badge(display, reg8, label, x, y,
                  colour=col, emphasis='ghost', type='semantic', icon=ic)
        x += w + 4

    display.show()
