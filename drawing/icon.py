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
    for row in range(h):
        for col in range(w):
            b = row * row_bytes + col // 8
            bit = 7 - (col % 8)
            if b < len(raw) and raw[b] & (1 << bit):
                display.pixel(x + col, y + row, fg)
            elif bg is not None:
                display.pixel(x + col, y + row, bg)


def icon_w(icon):
    return icon.width()


def icon_h(icon):
    return icon.height()
