from tkinter import messagebox
from playsound import playsound
from core.model import GachaponModel
from core.view import GachaponView

class GachaponController:
    def __init__(self, root):
        self.root = root  # Keep reference to root window
        self.model = GachaponModel()
        self.view = GachaponView(root, controller=self)
        self.view.pack(expand=True, fill='both')
        self.view.pull_btn.config(command=self.handle_pull)
        self.view.inventory_btn.config(command=self.handle_inventory)
        self.view.screenshot_btn.config(command=self.take_screenshot)
        self.sound_enabled = True

    def handle_pull(self):
        result, tier = self.model.pull()
        self._update_display(result, tier)

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