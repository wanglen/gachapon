import json
from pathlib import Path
from typing import Dict, List, Tuple

class GameConfig:
    _CONFIG_FILE = Path(__file__).parent.parent / "config.json"
    
    # Type hints for better IDE support
    CHARACTERS: Dict[int, List[Tuple[str, str]]] = {}
    RARITY_RATES: Dict[int, int] = {}
    COLORS: Dict[int, List[str]] = {}
    PITY_THRESHOLD: int = 50

    @classmethod
    def load_config(cls):
        """Load and validate configuration from JSON file"""
        try:
            with open(cls._CONFIG_FILE, 'r') as f:
                config = json.load(f)
            
            # Validate required fields
            for field in ['CHARACTERS', 'RARITY_RATES', 'COLORS', 'PITY_THRESHOLD']:
                if field not in config:
                    raise ValueError(f"Missing required field: {field}")
            
            # Convert string keys to integers and validate values
            cls.CHARACTERS = {int(k): v for k, v in config['CHARACTERS'].items()}
            cls.RARITY_RATES = {int(k): v for k, v in config['RARITY_RATES'].items()}
            cls.COLORS = {int(k): v for k, v in config['COLORS'].items()}
            cls.PITY_THRESHOLD = int(config['PITY_THRESHOLD'])
            
            # Validate rates sum to 100%
            if sum(cls.RARITY_RATES.values()) != 100:
                raise ValueError("Rarity rates must sum to 100%")
            
            # Validate character counts per tier
            for tier, characters in cls.CHARACTERS.items():
                if len(characters) < 5:
                    raise ValueError(f"Tier {tier} must have at least 5 characters")
                
            # Validate color formats
            for tier, colors in cls.COLORS.items():
                if len(colors) != 2 or any(not c.startswith('#') for c in colors):
                    raise ValueError(f"Invalid color format for tier {tier}")
                
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found: {cls._CONFIG_FILE}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON in config file: {cls._CONFIG_FILE}")

# Load config when module is imported
GameConfig.load_config() 