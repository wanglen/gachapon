from tkinter import messagebox
from playsound import playsound
from core.model import GachaponModel
from core.view import GachaponView
import tkinter as tk
from pathlib import Path

class GachaponController:
    def __init__(self, root):
        self.root = root
        self.model = GachaponModel()
        self.sound_enabled = True
        self._sound_files = {
            'pull': self._resolve_sound_path('sounds/pull.wav'),
            'rare': self._resolve_sound_path('sounds/rare.wav')
        }
        
        # Load before UI creation
        load_success = self.model.load_game()
        if not load_success:
            messagebox.showinfo("New Game", "Starting new game!")
            self.model.check_daily_login()
            self.model.save_game()
            
        # Create and pack view
        self.view = GachaponView(root, self)
        self.view.pack(fill=tk.BOTH, expand=True)
        
        self._setup_bindings()
        self.update_all_displays()
        
        # Debug: Print current state
        print(f"[DEBUG] Loaded State:", {
            'crystals': self.model.crystal_balance,
            'pulls': self.model.total_pulls,
            'pity': self.model.pity_counter
        })
        
        self._verify_sound_system()
        
        root.protocol("WM_DELETE_WINDOW", self.on_exit)

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
        login_result = self.model.check_daily_login()
        if login_result:
            messagebox.showinfo("Daily Bonus", "🎉 Daily login bonus: +200 crystals!")
            self.update_balance_display()
            self.model.save_game()
        elif login_result is None:  # First time login
            pass  # Already handled in model
        else:
            messagebox.showinfo("Welcome Back", "You already claimed today's bonus!")

    def handle_pull(self):
        try:
            result, tier = self.model.pull()
            self._update_display(result, tier)
            self.update_balance_display()
            self.update_stats_display()
            self.model.save_game()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("System Error", f"Pull failed: {str(e)}")
            self.model.save_game()

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
        """Fixed path handling"""
        sound_key = 'rare' if tier == 5 else 'pull'
        self.play_sound(self._sound_files[sound_key])

    def play_sound(self, filename):
        """More robust sound playback with fallbacks"""
        if not self.sound_enabled or not filename:
            return
            
        try:
            from playsound import playsound
            # Use synchronous playback for better compatibility
            self.root.after(100, lambda: playsound(filename, block=True))
        except Exception as e:
            print(f"Final sound attempt failed: {e}")
            self.sound_enabled = False
            self.view.sound_btn.config(text="🔇 Sound Error")

    def take_screenshot(self):
        from utils.screenshot import take_game_screenshot
        take_game_screenshot(self.root) 

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.view.sound_btn.config(
            text="🔊 Sound On" if self.sound_enabled else "🔇 Sound Off"
        ) 

    def play_minigame(self):
        """Handle minigame interaction - unlimited free crystals"""
        self.model.crystal_balance += 50
        self.update_balance_display()
        self.model.save_game()
        self.view.show_message("Minigame Completed", "You earned 50 crystals!")

    def watch_ad(self):
        """Handle ad watching simulation"""
        self.model.crystal_balance += 300
        self.view.update_balance_display()
        self.model.save_game()  # Add this line to force immediate save
        self.view.show_message("Ad Watched", "+300 crystals!")

    def _grant_ad_reward(self):
        self.model.crystal_balance += 300
        self.view.ad_btn.config(state=tk.NORMAL)
        self.update_balance_display()
        messagebox.showinfo("Ad Complete", "✅ +300 crystals awarded!")

    def update_balance_display(self):
        self.view.update_balance_display()

    def update_stats_display(self):
        """Force update pull counters"""
        stats_text = f"Pulls: {self.model.total_pulls} | 5★ Pity: {self.model.pity_counter}/50"
        self.view.stats_label.config(text=stats_text)
        self.view.stats_label.update_idletasks()  # Force UI refresh

    def on_exit(self):
        """Save on exit with validation"""
        print(f"[DEBUG] Pre-Save State:", {
            'crystals': self.model.crystal_balance,
            'pulls': self.model.total_pulls,
            'pity': self.model.pity_counter
        })
        self.model.save_game()
        self.root.destroy() 

    def _setup_bindings(self):
        """Connect UI elements to controller methods"""
        self.view.pull_btn.config(command=self.handle_pull)
        self.view.inventory_btn.config(command=self.show_inventory)
        self.view.screenshot_btn.config(command=self.take_screenshot)
        self.view.sound_btn.config(command=self.toggle_sound)
        
        # Add ad watch button binding
        if hasattr(self.view, 'ad_btn'):
            self.view.ad_btn.config(command=self.watch_ad)

        # Add minigame binding
        self.view.minigame_btn.config(command=self.play_minigame)

    def show_inventory(self):
        """Display inventory contents"""
        inventory_text = "\n".join([
            f"{item}: {count}" 
            for item, count in self.model.inventory.items()
        ])
        messagebox.showinfo("Inventory", inventory_text or "Empty")

    def take_screenshot(self):
        """Handle screenshot functionality"""
        # Implementation would go here
        self.view.show_message("Screenshot", "Feature coming soon!") 

    def update_all_displays(self):
        self.update_balance_display()
        self.update_stats_display() 

    def _verify_sound_system(self):
        """Check sound system readiness without playing test sound"""
        try:
            # Only validate file existence and imports
            from playsound import playsound  # Verify import works
            test_file = self._resolve_sound_path('sounds/pull.wav')
            
            # Don't actually play the sound, just verify path
            if not Path(test_file).exists():
                raise FileNotFoundError(f"Sound file missing: {test_file}")
                
        except Exception as e:
            messagebox.showwarning(
                "Sound System Error",
                f"Sound system failed to initialize:\n{str(e)}\n"
                "Sound effects will be disabled."
            )
            self.sound_enabled = False

    def _resolve_sound_path(self, relative_path):
        """Convert relative path to absolute path with better diagnostics"""
        try:
            base_dir = Path(__file__).parent.parent
            full_path = base_dir / relative_path
            if not full_path.exists():
                raise FileNotFoundError(f"Sound file missing: {full_path}")
            return str(full_path.resolve())  # Use absolute path
        except Exception as e:
            messagebox.showerror("Path Error", str(e))
            return None 