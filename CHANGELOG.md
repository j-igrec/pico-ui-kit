# Changelog

All notable changes to pico-ui-kit are documented here.

## [0.0.1] - 2026-05-16

### Added
- Scaffolded entire project: components/, drawing/, fonts/, simulator/, tokens/
- badge.py component
- Drawing primitives: line.py, rect.py, text.py
- IBM Plex Mono font files (8/16px, regular/bold)
- Token system with build_tokens.py, primitive.py, semantic.py
- Simulator (display.py, run.py)
- adapter.py (DisplayAdapter abstraction)
- tokens/colormode.py
- Split semantic tokens into semantic_light.py / semantic_dark.py
- CHANGELOG.md, __init__.py with version metadata, release.sh

### Changed
- Refactored semantic.py and build_tokens.py
- Updated simulator
- Major README.md rewrite

### Removed
- components/spell_card.py (moved to consuming project)
- tokens/src/ JSON source files (now gitignored)
- tokens/viewport.py
