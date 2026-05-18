"""Visual smoke test for the button component — all states & both types.

Run:
    python3 simulator/run.py simulator/demo_buttons.py
"""

from tokens.semantic import STRUCTURE_SURFACES_LEVEL_0
from components.button import button
import fonts.monor8 as reg8

import icons.plus as ic_plus
import icons.chevron_right as ic_chevron


def draw(display):
    display.fill(STRUCTURE_SURFACES_LEVEL_0)

    states = ['default', 'focus', 'hover', 'pressed', 'disabled']

    # ── Row 1: Primary buttons, all 5 states, label only ──
    y = 6
    x = 6
    for s in states:
        w = button(display, reg8, 'Btn', x, y, type='primary', state=s)
        x += w + 6   # 6px gap leaves room for focus ring

    # ── Row 2: Secondary buttons ──
    y += 26
    x = 6
    for s in states:
        w = button(display, reg8, 'Btn', x, y, type='secondary', state=s)
        x += w + 6

    # ── Row 3: Icon-only buttons (primary then secondary) ──
    y += 26
    x = 6
    for t in ['primary', 'secondary']:
        for s in states:
            w = button(display, reg8, '', x, y,
                       type=t, state=s, icon_only=True, lead_icon=ic_plus)
            x += w + 6

    # ── Row 4: Buttons with lead/trail icons ──
    y += 26
    x = 6
    w = button(display, reg8, 'Add', x, y, type='primary', state='default', lead_icon=ic_plus)
    x += w + 6
    w = button(display, reg8, 'Next', x, y, type='primary', state='default', trail_icon=ic_chevron)
    x += w + 6
    w = button(display, reg8, 'Save', x, y, type='secondary', state='default',
               lead_icon=ic_plus, trail_icon=ic_chevron)
    x += w + 6

    display.show()
