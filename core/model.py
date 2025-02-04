import random
from collections import defaultdict
from core.config import GameConfig
import datetime
from datetime import date
import json
from pathlib import Path

class GachaponModel:
    SAVE_FILE = Path("gachapon_save.json")
    
    def __init__(self):
        self.inventory = defaultdict(int)
        self.pity_counter = 0
        self.total_pulls = 0
        self.crystal_balance = 0  # Start with 0 crystals
        self._init_crystals = False  # Track if initial crystals were set
        self.achievements = {
            'first_pull': False,
            'five_star_pull': False,
            'collection_10': False
        }
        self.last_login_date = None
        
    def can_pull(self):
        return self.crystal_balance >= 100
        
    def pull(self):
        """Core gacha pull logic with currency check"""
        if not self.can_pull():
            raise ValueError("Not enough crystals")
            
        self.crystal_balance -= 100
        chosen_tier = self._select_rarity()
        self._update_pity_counter(chosen_tier)
        
        character, icon = random.choice(GameConfig.CHARACTERS[chosen_tier])
        full_name = f"{chosen_tier}★ {icon} {character}"
        self.inventory[full_name] += 1
        self.total_pulls += 1
        
        self.check_achievements(full_name)
        
        return full_name, chosen_tier

    def _select_rarity(self):
        """Select rarity tier with pity system"""
        if self.pity_counter >= GameConfig.PITY_THRESHOLD:
            return 5
            
        tiers, weights = zip(*GameConfig.RARITY_RATES.items())
        return random.choices(tiers, weights=weights, k=1)[0]

    def _update_pity_counter(self, chosen_tier):
        """Manage pity counter state"""
        if chosen_tier == 5:
            self.pity_counter = 0
        else:
            self.pity_counter += 1 

    def check_achievements(self, pull_result):
        if not self.achievements['first_pull']:
            self.crystal_balance += 500
            self.achievements['first_pull'] = True
            
        if '★5' in pull_result and not self.achievements['five_star_pull']:
            self.crystal_balance += 1000
            self.achievements['five_star_pull'] = True 

    def check_daily_login(self):
        """Check and grant daily login bonus if new day"""
        today = datetime.date.today()
        
        # Existing player with save data
        if self.SAVE_FILE.exists():
            if not self.last_login_date:  # Legacy save handling
                return False
            
            # Normal daily check
            if today > self.last_login_date:
                days_missing = (today - self.last_login_date).days
                if days_missing == 1:  # Consecutive day
                    self.crystal_balance += 200
                    self.last_login_date = today
                    return True
                else:  # Broken streak
                    self.last_login_date = today
                    return False
            return False
        
        # New player initialization (only runs once)
        else:  
            self.crystal_balance = 1000  # Base crystals
            self.crystal_balance += 200  # First day bonus
            self.last_login_date = today
            return True

    def save_game(self):
        """Save current game state to JSON file"""
        save_data = {
            'inventory': dict(self.inventory),
            'pity_counter': int(self.pity_counter),
            'total_pulls': int(self.total_pulls),
            'crystal_balance': int(self.crystal_balance),
            'achievements': self.achievements,
            'last_login_date': (
                self.last_login_date.isoformat() 
                if self.last_login_date 
                else None
            )
        }
        
        # Validate numerical values
        assert isinstance(save_data['pity_counter'], int), "Invalid pity counter"
        assert isinstance(save_data['total_pulls'], int), "Invalid pull count"
        assert isinstance(save_data['crystal_balance'], int), "Invalid crystal balance"
        
        with open(self.SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=2)

    def load_game(self):
        """Load game state from JSON file if exists"""
        if self.SAVE_FILE.exists():
            try:
                with open(self.SAVE_FILE, 'r') as f:
                    save_data = json.load(f)
                    
                # Validate critical fields
                self.crystal_balance = save_data.get('crystal_balance', 0)
                self.last_login_date = (
                    datetime.date.fromisoformat(save_data['last_login_date']) 
                    if save_data.get('last_login_date') 
                    else None
                )
                # Ensure other fields exist
                self.inventory = defaultdict(int, save_data.get('inventory', {}))
                self.pity_counter = save_data.get('pity_counter', 0)
                self.total_pulls = save_data.get('total_pulls', 0)
                self.achievements = {**self._default_achievements(), **save_data.get('achievements', {})}
                
                return True
            except Exception as e:
                print(f"Save corruption: {e}")
                return False
        return False

    def _default_achievements(self):
        """Return fresh achievements state"""
        return {
            'first_pull': False,
            'five_star_pull': False,
            'collection_10': False,
            'ad_watched': False
        } 