"""
simulator/run.py

Desktop entry point for the pico-ui-kit simulator.

Usage:
    cd /path/to/pico-ui-kit
    python3 simulator/run.py              # built-in spell card demo
    python3 simulator/run.py my_screen.py # custom screen file

A screen file must define:
    def draw(display): ...               # initial render (must call display.show())
    def on_input(key, display): ...      # optional — handle button presses
"""

import sys
import os
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


def run(draw_fn, input_fn=None):
    display = Display()
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
# Built-in demo
# ---------------------------------------------------------------------------

def _demo_draw(display):
    from components.spell_card import spell_card
    spell_card(display, {
        "name":         "Acid Splash",
        "level":        "Cantrip",
        "ritual":       False,
        "components":   "V, S",
        "casting_time": "Action",
        "use":          "Damage",
        "page":         "239",
        "classes":      ["Sorcerer", "Wizard"],
        "school":       "Evocation",
    })
    display.show()


def _demo_input(key, display):
    if key == "SHAKE":
        _demo_draw(display)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        spec = importlib.util.spec_from_file_location("screen", path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        run(mod.draw, getattr(mod, "on_input", None))
    else:
        run(_demo_draw, _demo_input)
