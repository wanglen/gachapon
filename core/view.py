import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageColor
from core.config import GameConfig

class GachaponView(ttk.Frame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        master.minsize(400, 300)
        master.resizable(False, False)
        self.style = ttk.Style()
        self.sprite_cache = {}
        
        # Initialize balance label first
        self.balance_label = tk.Label(
            self,
            text="Crystals: 0",
            font=("Arial", 12, "bold"),
            fg="#2ecc71"
        )
        
        self._configure_styles()
        self._create_widgets()
        self.create_sprite_templates()
        self._create_screenshot_button()
        self.setup_ui()

    def _configure_styles(self):
        """Configure UI theme and colors"""
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Result.Text', background='black', foreground='white')
        self.style.configure('Ad.TButton', foreground='#27ae60')
        self.style.configure('MiniGame.TButton', foreground='#e67e22')

    def _create_widgets(self):
        """Initialize UI components"""
        ttk.Label(self, text="Gachapon Simulator", style='Title.TLabel').pack(pady=10)
        
        # Add sound button initialization
        self.sound_btn = tk.Button(
            self,
            text="🔊 Sound On",
            font=("Arial", 10),
            relief="flat"
        )
        self.sound_btn.pack(side=tk.BOTTOM, pady=5)
        
        self.pull_btn = ttk.Button(self, text="Pull (100 crystals)")
        self.pull_btn.pack(pady=5)
        self.result_text = tk.Text(self, height=4, width=40, font=('Arial', 14))
        self.result_text.pack(pady=10)
        self.inventory_btn = ttk.Button(self, text="View Inventory")
        self.inventory_btn.pack(pady=5)
        self.stats_label = ttk.Label(self, text="Pulls: 0 | 5★ Pity: 0/50")
        self.stats_label.pack(pady=5)
        
        # Updated ad button with icon
        self.ad_btn = ttk.Button(
            self, 
            text="📺 Watch Ad (+300 crystals)",  # Added TV emoji
            style='Ad.TButton'
        )
        self.ad_btn.pack(pady=5)
        
        # Updated minigame button with icon
        self.minigame_btn = ttk.Button(
            self,
            text="🎮 Play Minigame",  # Added gamepad emoji
            style='MiniGame.TButton' 
        )
        self.minigame_btn.pack(pady=5)
        
        for tier in GameConfig.RARITY_RATES:
            self.result_text.tag_configure(f"{tier}star", foreground=GameConfig.COLORS[tier][0])

    def create_sprite_templates(self):
        """Generate more detailed character sprites"""
        for tier in GameConfig.COLORS:
            img = Image.new('RGBA', (48, 48), (0,0,0,0))
            d = ImageDraw.Draw(img)
            base_hex, accent_hex = GameConfig.COLORS[tier]
            base_color = ImageColor.getrgb(base_hex)
            accent_color = ImageColor.getrgb(accent_hex)
            
            for i in range(48):
                alpha = int(255 * (0.7 - (i/48)*0.3))
                d.line((i,0,i,47), fill=base_color + (alpha,))
            
            if tier == 3:
                d.regular_polygon((24,24,20), n_sides=6, fill=accent_color)
            elif tier == 4:
                d.polygon([(12,24), (24,12), (36,24), (24,36)], fill=accent_color)
            else:
                d.polygon([(12,28), (24,12), (36,28), (24,24)], fill=accent_color)
                d.polygon([(18,32), (24,24), (30,32)], fill=accent_color)
            
            d.ellipse((2,2,45,45), outline=base_color, width=2)
            for _ in range(random.randint(3, 6)):
                x = random.randint(5, 43)
                y = random.randint(5, 43)
                size = random.choice([1, 2, 3])
                d.ellipse((x,y,x+size,y+size), fill=random.choice(['white', accent_hex, '#ffffffaa']))
            
            d.text((4, 4), str(tier), fill=accent_color)
            
            self.sprite_cache[tier] = ImageTk.PhotoImage(img.resize((32,32)))
            
    def _update_display(self, result, tier, total_pulls, pity_counter):
        self.result_text.delete(1.0, tk.END)
        self.result_text.image_create(tk.END, image=self.sprite_cache[tier])
        self.result_text.insert(tk.END, f"\nYOU GOT:\n{result}\n{tier}★")
        self._update_stats(total_pulls, pity_counter)

    def _update_stats(self, total_pulls, pity_counter):
        stats_text = f"Pulls: {total_pulls} | 5★ Pity: {pity_counter}/50"
        self.stats_label.config(text=stats_text)

    def _create_screenshot_button(self):
        self.screenshot_btn = ttk.Button(
            self, 
            text="📸 Take Screenshot"
            # Command will be set by controller
        )
        self.screenshot_btn.pack(pady=5)

    def setup_ui(self):
        # Properly pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
        
        # Reposition balance label to top-right
        self.balance_label.pack_forget()  # Remove old positioning
        self.balance_label.pack(
            side=tk.TOP, 
            anchor='e',  # East alignment
            padx=10,
            pady=5,
            fill=tk.X
        )
        
        # Keep sound button at bottom
        self.sound_btn.pack(side=tk.BOTTOM, pady=5)
        
        # Ensure proper button order
        self.pull_btn.pack(pady=5)
        self.ad_btn.pack(pady=5)
        self.minigame_btn.pack(pady=5)
        self.inventory_btn.pack(pady=5)
        self.screenshot_btn.pack(pady=5)
        
        # Force UI refresh
        self.update_idletasks()

    def update_balance_display(self):
        """Update crystal balance display"""
        balance = self.controller.model.crystal_balance
        self.balance_label.config(text=f"Crystals: {balance}")

    def show_message(self, title, message):
        """Display a message dialog"""
        messagebox.showinfo(title, message) 