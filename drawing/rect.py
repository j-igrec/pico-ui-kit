def fill_rect(display, x, y, w, h, color):
    display.fill_rect(x, y, w, h, color)


def hline(display, x, y, w, color):
    display.hline(x, y, w, color)


def vline(display, x, y, h, color):
    display.vline(x, y, h, color)


def rounded_rect(display, x, y, w, h, r, color):
    """Outline-only rounded rectangle with corner radius r."""
    display.hline(x + r,     y,         w - 2*r, color)
    display.hline(x + r,     y + h - 1, w - 2*r, color)
    display.vline(x,         y + r,     h - 2*r, color)
    display.vline(x + w - 1, y + r,     h - 2*r, color)
    for dr in range(r):
        offset = r - 1 - dr
        display.pixel(x + offset,         y + r - 1 - dr,  color)  # TL
        display.pixel(x + w - 1 - offset, y + r - 1 - dr,  color)  # TR
        display.pixel(x + offset,         y + h - r + dr,  color)  # BL
        display.pixel(x + w - 1 - offset, y + h - r + dr,  color)  # BR


def fill_rounded_rect(display, x, y, w, h, r, color):
    """Filled rounded rectangle."""
    display.fill_rect(x + r, y,     w - 2*r, h,     color)
    display.fill_rect(x,     y + r, r,       h-2*r, color)
    display.fill_rect(x+w-r, y + r, r,       h-2*r, color)
    for dr in range(r):
        rw = r - dr
        display.hline(x + r - rw,     y + dr,         w - 2*(r-rw), color)
        display.hline(x + r - rw,     y + h - 1 - dr, w - 2*(r-rw), color)
