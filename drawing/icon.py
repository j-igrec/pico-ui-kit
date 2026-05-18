def draw_icon(display, icon, x, y, fg, bg=None):
    """Draw a 1-bit icon module at (x, y).

    icon must expose width(), height(), and data() — bytes packed MSB-first,
    row-major, the same shape as fonts/ modules from font_to_py.

    fg: colour for "on" pixels (any token tuple).
    bg: colour for "off" pixels; None to render transparently (off pixels are skipped).
    """
    w = icon.width()
    h = icon.height()
    raw = icon.data()
    row_bytes = (w + 7) // 8
    raw_len = len(raw)
    for row in range(h):
        row_off = row * row_bytes
        for col in range(w):
            b = row_off + (col >> 3)
            if b < raw_len and raw[b] & (1 << (7 - (col & 7))):
                display.pixel(x + col, y + row, fg)
            elif bg is not None:
                display.pixel(x + col, y + row, bg)
