def fill_rect(display, x, y, w, h, color):
    display.fill_rect(x, y, w, h, color)


def hline(display, x, y, w, color):
    display.hline(x, y, w, color)


def vline(display, x, y, h, color):
    display.vline(x, y, h, color)


def _corner_offsets(r):
    """Quarter-circle row offsets for radius r using doubled-int math (no sqrt).

    Returns a list where index `dr` (counted from the outermost row of the corner
    region) holds the inset from the bounding-box edge for that row.
    """
    offsets = []
    r2_sq = (2 * r) * (2 * r)
    for dr in range(r):
        dy_d = 2 * (r - dr) - 1
        dy_d_sq = dy_d * dy_d
        dx_d = 0
        while dx_d + 1 <= 2 * r:
            if (dx_d + 1) * (dx_d + 1) + dy_d_sq > r2_sq:
                break
            dx_d += 1
        offsets.append(r - ((dx_d + 1) // 2))
    return offsets


def rounded_rect(display, x, y, w, h, r, color):
    """Outline-only rounded rectangle with corner radius r."""
    if r <= 0:
        display.hline(x,         y,         w, color)
        display.hline(x,         y + h - 1, w, color)
        display.vline(x,         y,         h, color)
        display.vline(x + w - 1, y,         h, color)
        return

    r = min(r, min(w, h) // 2)
    offsets = _corner_offsets(r)
    top_offset = offsets[0]

    # Straight edges between corners — start/end where the corner curve begins.
    display.hline(x + top_offset,         y,         w - 2 * top_offset, color)
    display.hline(x + top_offset,         y + h - 1, w - 2 * top_offset, color)
    display.vline(x,                      y + r,     h - 2 * r,          color)
    display.vline(x + w - 1,              y + r,     h - 2 * r,          color)

    # Corner pixels — plot one pixel per row, bridge any vertical step.
    prev_offset = top_offset
    for dr, offset in enumerate(offsets):
        display.pixel(x + offset,             y + dr,           color)
        display.pixel(x + w - 1 - offset,     y + dr,           color)
        display.pixel(x + offset,             y + h - 1 - dr,   color)
        display.pixel(x + w - 1 - offset,     y + h - 1 - dr,   color)
        if dr > 0 and prev_offset > offset + 1:
            for col in range(offset + 1, prev_offset):
                display.pixel(x + col,             y + dr,           color)
                display.pixel(x + w - 1 - col,     y + dr,           color)
                display.pixel(x + col,             y + h - 1 - dr,   color)
                display.pixel(x + w - 1 - col,     y + h - 1 - dr,   color)
        prev_offset = offset


def fill_rounded_rect(display, x, y, w, h, r, color):
    """Filled rectangle with rounded corners (quarter-circle approximation)."""
    if r <= 0:
        display.fill_rect(x, y, w, h, color)
        return

    r = min(r, min(w, h) // 2)
    offsets = _corner_offsets(r)

    # Middle band — full width, only the non-corner rows.
    if h > 2 * r:
        display.fill_rect(x, y + r, w, h - 2 * r, color)

    # Top and bottom corner rows — narrower at the outer edge, widening toward the body.
    for dr, offset in enumerate(offsets):
        row_w = w - 2 * offset
        if row_w > 0:
            display.hline(x + offset, y + dr,         row_w, color)
            display.hline(x + offset, y + h - 1 - dr, row_w, color)
