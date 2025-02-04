from tkinter import messagebox
from playsound import playsound
from core.model import GachaponModel
from core.view import GachaponView
import tkinter as tk

class GachaponController:
    def __init__(self, root):
        self.root = root  # Keep reference to root window
        self.model = GachaponModel()
        self.view = GachaponView(root, controller=self)
        self.view.pack(expand=True, fill='both')
        self.view.pull_btn.config(command=self.handle_pull)
        self.view.inventory_btn.config(command=self.handle_inventory)
        self.view.screenshot_btn.config(command=self.take_screenshot)
        self.view.sound_btn.config(command=self.toggle_sound)
        self.sound_enabled = True
        
        # Add new systems
        self._setup_crystal_systems()
        self._check_daily_login()

    def _setup_crystal_systems(self):
        """Initialize all crystal acquisition UI elements"""
        # Mini-game button
        self.view.minigame_btn = tk.Button(
            self.root, 
            text="🕹 Play Mini-Game (+50 crystals)", 
            command=self.play_minigame
        )
        self.view.minigame_btn.pack(side=tk.BOTTOM, pady=3)
        
        # Ad button
        self.view.ad_btn = tk.Button(
            self.root,
            text="📺 Watch Ad (+300 crystals)",
            command=self.watch_ad
        )
        self.view.ad_btn.pack(side=tk.BOTTOM, pady=3)
        
        # Achievement label
        self.achievement_label = tk.Label(
            self.root, 
            text="Achievements: 0",
            font=("Arial", 10)
        )
        self.achievement_label.pack(side=tk.TOP, anchor='ne')

    def _check_daily_login(self):
        """Check for daily login bonus on startup"""
        if self.model.check_daily_login():
            messagebox.showinfo("Daily Bonus", "🎉 Daily login bonus: +200 crystals!")
            self.update_balance_display()

    def handle_pull(self):
        if not self.model.can_pull():
            messagebox.showerror("Cannot Pull", "You need 100 crystals to pull!")
            return
        
        try:
            result, tier = self.model.pull()
            self._update_display(result, tier)
            self.update_balance_display()
            
            new_achievements = self.model.check_achievements(result)
            if new_achievements:
                achievement_text = "🎉 New Achievements!\n" + "\n".join(new_achievements)
                messagebox.showinfo("Achievements Unlocked", achievement_text)
                self.update_balance_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def handle_inventory(self):
        inventory_text = "=== INVENTORY ===\n" + "\n".join(
            f"{char}: {count}x" for char, count in 
            sorted(self.model.inventory.items(), key=lambda x: -int(x[0][0]))
        )
        messagebox.showinfo("Inventory", inventory_text)

    def _update_display(self, result, tier):
        total_pulls = self.model.total_pulls
        pity_counter = self.model.pity_counter
        self.view._update_display(result, tier, total_pulls, pity_counter)
        self._play_sound_effects(tier)

    def _play_sound_effects(self, tier):
        if tier == 5:
            self.play_sound('sounds/rare.wav')
        self.play_sound('sounds/pull.wav')

    def play_sound(self, filename):
        if self.sound_enabled:
            try:
                playsound(filename)
            except Exception as e:
                print(f"Error playing sound: {e}")

    def take_screenshot(self):
        from utils.screenshot import take_game_screenshot
        take_game_screenshot(self.root) 

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.view.sound_btn.config(
            text="🔊 Sound On" if self.sound_enabled else "🔇 Sound Off"
        ) 

    def play_minigame(self):
        """Simple clicker mini-game"""
        self.model.crystal_balance += 50
        self.update_balance_display()
        messagebox.showinfo("Mini-Game", "🎯 Target Hit! +50 crystals!")

    def watch_ad(self):
        """Simulated ad watching with 3 second delay"""
        self.view.ad_btn.config(state=tk.DISABLED)
        self.root.after(3000, self._grant_ad_reward)
        messagebox.showinfo("Ad", "📺 Watching ad... (3 seconds)")

    def _grant_ad_reward(self):
        self.model.crystal_balance += 300
        self.view.ad_btn.config(state=tk.NORMAL)
        self.update_balance_display()
        messagebox.showinfo("Ad Complete", "✅ +300 crystals awarded!")

    def update_balance_display(self):
        self.view.update_balance_display() 