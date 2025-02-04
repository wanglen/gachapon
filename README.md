# Gachapon Simulator

A Python-based gachapon game with a graphical interface featuring collectible characters with different rarity tiers.

![Game Screenshot](screenshot.png) *[Optional: Add screenshot later]*

## Features

- 🎮 Graphical user interface (GUI) using Tkinter
- 💎 Crystal currency system (100 per pull)
- 🌟 Three rarity tiers (3★, 4★, 5★) with different probabilities
- 🛡️ Pity system guaranteeing 5★ after 50 unsuccessful pulls
- 📦 Inventory tracking system with tier-sorted display
- 🎨 Custom generated sprites with tier-specific designs
- 🔊 Sound feedback with toggle control
- 📊 Real-time pull statistics and crystal balance
- 🎯 Mini-game for earning extra crystals
- 📺 Ad simulation system (300 crystals per view)
- 🏆 Achievement system with crystal rewards
- 📅 Daily login bonuses (200 crystals/day)

## Requirements

- Python 3.6+
- Pillow (PIL Fork)
- playsound (for audio playback)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gachapon-simulator.git
cd gachapon-simulator
```

2. Install dependencies:

```bash
pip install Pillow playsound PyObjC
```

# How to Play

1. Run the game:
```bash
python gachapon.py
```

2. Interface controls:
- **Pull Button**: Spend 100 crystals for a random character
- **Inventory Button**: View collected characters sorted by tier
- **Mini-Game Button**: Earn 50 crystals per click
- **Ad Button**: Watch simulated ads for 300 crystals
- **Sound Toggle**: Enable/disable sound effects

3. Game mechanics:
- Base rates: 3★ (70%), 4★ (25%), 5★ (5%)
- Pity system: Guaranteed 5★ after 50 unsuccessful pulls
- Daily login bonus: 200 crystals awarded on first launch each day
- Achievements: Earn bonus crystals for milestones
- Character sprites: Randomly generated with tier-specific effects

## Credits

- Developed by Ghost
- Built with Python's Tkinter GUI toolkit
- Uses Pillow (PIL Fork) for image processing
- Emoji icons provided by Unicode Consortium

## License

MIT License - see [LICENSE](LICENSE) file for details
