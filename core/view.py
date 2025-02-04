import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk, ImageColor
from core.config import GameConfig

class GachaponView(ttk.Frame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller  # Store controller reference
        self.master = master
        master.minsize(400, 300)  # Minimum window size
        master.resizable(False, False)  # Disable resizing
        self.style = ttk.Style()
        self.sprite_cache = {}
        self.balance_label = None  # Add this line if not present
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

    def _create_widgets(self):
        """Initialize UI components"""
        ttk.Label(self, text="Gachapon Simulator", style='Title.TLabel').pack(pady=10)
        self.pull_btn = ttk.Button(self, text="Pull (100 crystals)")
        self.pull_btn.pack(pady=5)
        self.result_text = tk.Text(self, height=4, width=40, font=('Arial', 14))
        self.result_text.pack(pady=10)
        self.inventory_btn = ttk.Button(self, text="View Inventory")
        self.inventory_btn.pack(pady=5)
        self.stats_label = ttk.Label(self, text="Pulls: 0 | 5★ Pity: 0/50")
        self.stats_label.pack(pady=5)
        
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
        # Add sound toggle button
        self.sound_btn = tk.Button(
            self.master, 
            text="🔊 Sound On",
            font=("Arial", 10),
            relief="flat"
        )
        self.sound_btn.pack(side=tk.BOTTOM, pady=5)

        # Add/update balance display
        self.balance_label = tk.Label(
            self.master, 
            text="Crystals: 1000",
            font=("Arial", 12, "bold"),
            fg="#2ecc71"
        )
        self.balance_label.pack(side=tk.TOP, pady=5)

        # ... rest of existing UI code ... 

    def update_balance_display(self):
        """Update crystal balance display"""
        balance = self.controller.model.crystal_balance
        self.balance_label.config(text=f"Crystals: {balance}") 