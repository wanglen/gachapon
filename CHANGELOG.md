# Changelog

## [1.2.1] - 2025-02-03
### Fixed
- Crystal persistence between sessions
- UI layout initialization errors
- Missing button bindings for ads/minigame
- Attribute errors in view component
- Save file corruption edge cases
- Model-view synchronization delays

### Added
- Emoji icons for ad/minigame buttons
- Debug logging for state validation
- Immediate save after critical actions
- Save file integrity checks
- Top-right crystal counter position
- Force UI refresh after loading

### Changed
- Improved error handling flow
- Unified UI update triggers
- Enhanced save validation rules
- Minigame reward to 50 crystals (unlimited)
- Ad reward persistence mechanism

## [1.2.0] - 2025-02-03
### Added
- Crystal currency system (100 per pull)
- Daily login bonus (200 crystals/day)
- Achievements system with crystal rewards
- Mini-game for earning extra crystals
- Ad watching system (300 crystals/ad)
- Balance display in main UI
- Sound toggle functionality

### Changed
- Pull system requires crystals
- Inventory sorting now considers tier first
- Improved error handling for insufficient crystals
- Enhanced achievement tracking display
- Ad button disables during viewing

### Fixed
- Crystal balance display updates
- Achievement triggering logic
- Sound toggle persistence
- Model-view synchronization issues

## [1.1.0] - 2025-02-03
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

## [1.0.0] - 2025-02-03
### Initial Release
- Basic console-based gachapon game
- Three rarity tiers with probability system
- Simple inventory tracking
- No graphical interface 