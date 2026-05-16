"""
simulator/run.py

Desktop entry point for the pico-ui-kit simulator.

Usage:
    cd /path/to/pico-ui-kit
    python3 simulator/run.py                            # built-in badge demo (240×135)
    python3 simulator/run.py --width 320 --height 240  # different display size
    python3 simulator/run.py my_screen.py              # custom screen file

A screen file must define:
    def draw(display): ...               # initial render (must call display.show())
    def on_input(key, display): ...      # optional — handle button presses
"""

import sys
import os
import argparse
import importlib.util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
from simulator.display import Display

KEY_MAP = {
    pygame.K_a:     "A",
    pygame.K_b:     "B",
    pygame.K_UP:    "UP",
    pygame.K_DOWN:  "DOWN",
    pygame.K_LEFT:  "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_SPACE: "CTR",
    pygame.K_s:     "SHAKE",
}


def run(draw_fn, input_fn=None, width=240, height=135):
    display = Display(width=width, height=height)
    draw_fn(display)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                key = KEY_MAP.get(event.key)
                if key and input_fn:
                    input_fn(key, display)


# ---------------------------------------------------------------------------
# Built-in demo — badge grid showing semantic categories and emphasis levels
# ---------------------------------------------------------------------------

def _demo_draw(display):
    from tokens.semantic import STRUCTURE_SURFACES_LEVEL_0
    from components.badge import badge
    import fonts.monor8 as reg8

    display.fill(STRUCTURE_SURFACES_LEVEL_0)

    categories = ['neutral', 'success', 'warning', 'error', 'information']
    emphases   = ['default', 'subtle', 'ghost']

    y = 12
    for emphasis in emphases:
        x = 12
        for cat in categories:
            w = badge(display, reg8, cat[:4], x, y, category=cat, emphasis=emphasis)
            x += w + 4
        y += reg8.height() + 8 + 8

    display.show()


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pico-ui-kit simulator")
    parser.add_argument("screen", nargs="?", help="Screen file to preview")
    parser.add_argument("--width",  type=int, default=240, help="Display width in pixels (default: 240)")
    parser.add_argument("--height", type=int, default=135, help="Display height in pixels (default: 135)")
    args = parser.parse_args()

    if args.screen:
        path = args.screen
        spec = importlib.util.spec_from_file_location("screen", path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        run(mod.draw, getattr(mod, "on_input", None), width=args.width, height=args.height)
    else:
        run(_demo_draw, width=args.width, height=args.height)
