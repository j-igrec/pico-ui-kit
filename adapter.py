class DisplayAdapter:
    """
    Wraps any MicroPython display driver so it works with pico-ui-kit components.

    Most drivers already support fill, fill_rect, hline, vline, and pixel.
    The write() method (bitmap font rendering) is the one most drivers lack —
    this adapter provides a pixel-by-pixel fallback when the driver doesn't
    have it. If the driver does have write(), it is used directly.

    Usage:
        from adapter import DisplayAdapter
        import st7789  # or ssd1306, ili9341, etc.

        raw = st7789.ST7789(spi, dc=dc, cs=cs, rst=rst)
        display = DisplayAdapter(raw, width=240, height=135)

        from components.badge import badge
        import fonts.monor8 as font
        badge(display, font, "OK", 10, 10)
    """

    def __init__(self, driver, width, height):
        self._d = driver
        self.width = width
        self.height = height

    def fill(self, color):
        self._d.fill(color)

    def fill_rect(self, x, y, w, h, color):
        self._d.fill_rect(x, y, w, h, color)

    def hline(self, x, y, w, color):
        self._d.hline(x, y, w, color)

    def vline(self, x, y, h, color):
        self._d.vline(x, y, h, color)

    def pixel(self, x, y, color):
        self._d.pixel(x, y, color)

    def write(self, font, text, x, y, fg, bg=None):
        if hasattr(self._d, 'write'):
            self._d.write(font, text, x, y, fg, bg)
            return
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
                        self._d.pixel(cx + col, y + row, fg)
                    elif bg is not None:
                        self._d.pixel(cx + col, y + row, bg)
            cx += w

    def show(self):
        if hasattr(self._d, 'show'):
            self._d.show()
