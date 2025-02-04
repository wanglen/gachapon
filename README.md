# Gachapon Simulator

A feature-rich Python gacha game with strategic resource management and collectible character progression system.

![Game Screenshot](screenshot.png)

## Features

**Core Gameplay**
- 🎰 Gacha system with 3 rarity tiers (3★, 4★, 5★)
- 🛡️ Pity counter guaranteeing 5★ after 50 pulls
- 📦 Inventory management with tier-based sorting
- 🎨 Procedurally generated character sprites

**Economy Systems**
- 💎 Crystal currency (100/pull) with multiple earning methods:
  - Daily login bonuses (200/day)
  - Achievement rewards (500-1000 crystals)
  - Mini-game challenges (+50/play)
  - Ad watching simulations (+300/view)
- 📈 Real-time balance tracking
- 💰 First pull protection system

**Player Experience**
- 🎮 Intuitive Tkinter GUI with multiple interactive panels
- 🔊 Dynamic sound effects with toggle control
- 📸 Built-in screenshot functionality
- 🏆 Achievement milestone tracking
- 📅 Daily reward system with streak protection

**Technical Features**
- 🧩 MVC architecture separation
- 📊 Real-time pull statistics
- 🖼️ Pillow-powered image generation
- 🎚️ Configurable rates and balances
- ⚙️ Cross-platform compatibility

## Requirements

- Python 3.6+
- Pillow (PIL Fork)
- playsound (for audio playback)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/wanglen/gachapon.git
cd gachapon
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
- AI-assisted development using [DeepSeek](https://www.deepseek.com) and [Cursor](https://www.cursor.com)
- Uses Pillow (PIL Fork) for image processing
- Emoji icons provided by Unicode Consortium

## License

MIT License - see [LICENSE](LICENSE) file for details
