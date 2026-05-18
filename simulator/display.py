import pygame

_DEFAULT_SCALE = 1


class Display:
    """
    Desktop simulator for any pixel display.

    Presents the same drawing API as a DisplayAdapter so components run
    unchanged on desktop and on device. Colors are (r, g, b) tuples.

    Draw calls write to an internal surface at the given resolution.
    Call show() to push the frame to the Pygame window.
    """

    def __init__(self, width=240, height=135, scale=_DEFAULT_SCALE):
        self.width  = width
        self.height = height
        self._scale = scale
        pygame.init()
        self._surface = pygame.Surface((width, height))
        self._window  = pygame.display.set_mode((width * scale, height * scale))
        pygame.display.set_caption(f"pico-ui-kit  [{width}×{height}]")
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
        """Flush the internal surface to the Pygame window at scale."""
        scaled = pygame.transform.scale(
            self._surface,
            (self.width * self._scale, self.height * self._scale),
        )
        self._window.blit(scaled, (0, 0))
        pygame.display.flip()
