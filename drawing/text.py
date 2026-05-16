def write(display, font, text, x, y, fg, bg=None):
    display.write(font, text, x, y, fg, bg)


def text_w(font, text):
    return font.max_width() * len(text)


def text_h(font):
    return font.height()


def word_wrap(text, chars_per_line, max_lines=2):
    """Split text into at most max_lines lines, breaking on word boundaries."""
    words = text.split()
    lines = []
    current = ''
    for word in words:
        candidate = (current + ' ' + word).strip()
        if len(candidate) <= chars_per_line:
            current = candidate
        else:
            if current:
                lines.append(current)
            if len(lines) >= max_lines:
                break
            current = word
    if current and len(lines) < max_lines:
        lines.append(current)
    return lines
