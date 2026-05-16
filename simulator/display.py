import pygame

WIDTH  = 240
HEIGHT = 135
SCALE  = 3


class Display:
    """
    Desktop simulator for the ST7789 240×135 LCD.

    Presents the same drawing API as the real hardware driver so components
    run unchanged. Colors are (r, g, b) tuples — matching the token format.

    Draw calls write to an internal 240×135 surface. Call show() to push the
    frame to the Pygame window (mirrors the real driver's flush-on-show model).
    """

    def __init__(self):
        pygame.init()
        self._surface = pygame.Surface((WIDTH, HEIGHT))
        self._window  = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
        pygame.display.set_caption(f"pico-ui-kit  [{WIDTH}×{HEIGHT}]")
        self._surface.fill((0, 0, 0))

    # -------------------------------------------------------------------------
    # Drawing API — matches ST7789 driver interface
    # -------------------------------------------------------------------------

    def fill(self, color):
        self._surface.fill(color[:3])

    def fill_rect(self, x, y, w, h, color):
        pygame.draw.rect(self._surface, color[:3], (x, y, w, h))

    def hline(self, x, y, w, color):
        pygame.draw.line(self._surface, color[:3], (x, y), (x + w - 1, y))

    def vline(self, x, y, h, color):
        pygame.draw.line(self._surface, color[:3], (x, y), (x, y + h - 1))

    def pixel(self, x, y, color):
        self._surface.set_at((x, y), color[:3])

    def write(self, font, text, x, y, fg, bg=None):
        """Render text using a font_to_py bitmap font module.
        bg=None renders transparently — 0-bits in the glyph are not drawn.
        """
        cx = x
        for ch in text:
            try:
                glyph, h, w = font.get_ch(ch)
            except Exception:
                continue
            row_bytes = (w + 7) // 8
            for row in range(h):
                for col in range(w):
                    b   = row * row_bytes + col // 8
                    bit = 7 - (col % 8)
                    if b < len(glyph) and glyph[b] & (1 << bit):
                        self._surface.set_at((cx + col, y + row), fg[:3])
                    elif bg is not None:
                        self._surface.set_at((cx + col, y + row), bg[:3])
            cx += w

    def show(self):
        """Flush the internal surface to the Pygame window at 3× scale."""
        scaled = pygame.transform.scale(self._surface, (WIDTH * SCALE, HEIGHT * SCALE))
        self._window.blit(scaled, (0, 0))
        pygame.display.flip()
