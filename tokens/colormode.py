# tokens/colormode.py
# Boot-time colour mode selection — do not edit by hand, but this is NOT auto-generated.
#
# Reads mode.cfg from the working directory at import time:
#   - On the Pico: place mode.cfg at the root of the filesystem
#   - In the simulator: place mode.cfg in the pico-ui-kit project root
#
# To switch colour mode:
#   1. Write 'light' or 'dark' to mode.cfg on the device
#   2. Reset the device (Ctrl+D in the REPL, or power cycle)
#
# If mode.cfg is absent or unreadable, 'light' is used.

try:
    with open('mode.cfg') as _f:
        _colormode = _f.read().strip()
except OSError:
    _colormode = 'light'

if _colormode == 'dark':
    from tokens.semantic_dark import *
else:
    from tokens.semantic_light import *
