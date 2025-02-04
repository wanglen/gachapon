# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-01-03
### Added
- Graphical user interface using Tkinter
- Sound effects for pulls and rare acquisitions
- Inventory tracking system with tier-sorted display
- Pity counter system (guaranteed 5★ after 50 pulls)
- Cross-platform compatibility
- README documentation
- CHANGELOG file

### Changed
- Refactored codebase to MVC architecture
- Improved code organization with separate modules:
  - `model.py` - Game logic and state
  - `view.py` - UI components
  - `controller.py` - Event handling
  - `config.py` - Game constants
- Enhanced sprite generation with tier-specific designs
- Window positioning to center on screen
- Error handling for sound playback

### Fixed
- Pull button interaction issues
- Sound effect triggering
- Model-View communication errors
- Inventory display sorting
- Window resizing and positioning

## [1.0.0] - 2025-01-03
### Initial Release
- Basic console-based gachapon game
- Three rarity tiers with probability system
- Simple inventory tracking
- No graphical interface 