def hline(display, x, y, w, color):
    display.hline(x, y, w, color)


def vline(display, x, y, h, color):
    display.vline(x, y, h, color)


def dot(display, x, y, color):
    """Draw a 2×2 separator dot."""
    display.fill_rect(x, y, 2, 2, color)
