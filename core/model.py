import random
from collections import defaultdict
from core.config import GameConfig

class GachaponModel:
    def __init__(self):
        self.inventory = defaultdict(int)
        self.pity_counter = 0
        self.total_pulls = 0
        
    def pull(self):
        """Core gacha pull logic"""
        chosen_tier = self._select_rarity()
        self._update_pity_counter(chosen_tier)
        
        character, icon = random.choice(GameConfig.CHARACTERS[chosen_tier])
        full_name = f"{chosen_tier}★ {icon} {character}"
        self.inventory[full_name] += 1
        self.total_pulls += 1
        
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