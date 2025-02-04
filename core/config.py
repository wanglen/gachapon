class GameConfig:
    CHARACTERS = {
        3: [
            ("Warrior", "🗡️"), 
            ("Mage", "🔮"),
            ("Archer", "🏹"),
            ("Thief", "🗡️"),
            ("Cleric", "⛪")
        ],
        4: [
            ("Dragon Knight", "🐲"),
            ("Archmage", "📚"),
            ("Sniper", "🎯"),
            ("Assassin", "🥷"),
            ("High Priest", "🙏")
        ],
        5: [
            ("Phoenix Lord", "🔥"),
            ("Arcane Sovereign", "🌀"),
            ("Celestial Archer", "🌌"),
            ("Shadow Monarch", "👑"),
            ("Divine Oracle", "🔮")
        ]
    }

    RARITY_RATES = {
        3: 70,  # 70% chance
        4: 25,  # 25% chance
        5: 5    # 5% chance
    }

    COLORS = {
        3: ('#00a8ff', '#005f89'),
        4: ('#9b59b6', '#5e2a7a'),
        5: ('#f1c40f', '#c29f0b')
    }

    PITY_THRESHOLD = 50 