import random
from collections import defaultdict
from core.config import GameConfig
import datetime
from datetime import date

class GachaponModel:
    def __init__(self):
        self.inventory = defaultdict(int)
        self.pity_counter = 0
        self.total_pulls = 0
        self.crystal_balance = 1000  # Starting crystals
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
        if self.last_login_date != today:
            self.crystal_balance += 200
            self.last_login_date = today
            return True
        return False 