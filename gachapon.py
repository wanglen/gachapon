import random
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageDraw, ImageTk, ImageColor

# Gachapon configuration
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

class GachaponGame:
    def __init__(self):
        self.inventory = defaultdict(int)
        self.pity_counter = 0
        
    def pull(self):
        """Perform a single gachapon pull"""
        # Weighted random selection for rarity
        tiers, weights = zip(*RARITY_RATES.items())
        chosen_tier = random.choices(tiers, weights=weights, k=1)[0]
        
        # Pity system - increase 5★ chance after 50 pulls without one
        self.pity_counter += 1
        if self.pity_counter >= 50:
            chosen_tier = 5
            self.pity_counter = 0
        
        # Select character and icon from chosen tier
        character, icon = random.choice(CHARACTERS[chosen_tier])
        full_name = f"{chosen_tier}★ {icon} {character}"
        self.inventory[full_name] += 1
        
        # Reset pity counter if 5★ pulled
        if chosen_tier == 5:
            self.pity_counter = 0
            
        return full_name

    def show_inventory(self):
        """Display collected characters"""
        print("\n=== INVENTORY ===")
        for char, count in sorted(self.inventory.items(), 
                                key=lambda x: -int(x[0][0])):
            print(f"{char}: {count}x")
        print()

class GachaponGUI:
    def __init__(self, master):
        self.game = GachaponGame()
        self.master = master
        master.title("Gachapon Simulator")
        master.geometry("600x400")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Create UI elements
        self.create_widgets()
        
        self.sprite_cache = {}
        self.create_sprite_templates()
        
    def create_widgets(self):
        # Header
        self.header = ttk.Label(self.master, text="Gachapon Simulator", style='Title.TLabel')
        self.header.pack(pady=10)
        
        # Pull Button
        self.pull_btn = ttk.Button(self.master, text="Pull (100 crystals)", command=self.do_pull)
        self.pull_btn.pack(pady=5)
        
        # Result Display
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.pack(pady=10)
        
        self.result_text = tk.Text(self.result_frame, height=4, width=40, 
                                 font=('Arial', 14), bg='black', fg='white')
        self.result_text.pack()
        
        # Inventory Button
        self.inventory_btn = ttk.Button(self.master, text="View Inventory", 
                                      command=self.show_inventory)
        self.inventory_btn.pack(pady=5)
        
        # Stats Label
        self.stats_label = ttk.Label(self.master, text="Pulls: 0 | 5★ Pity: 0/50")
        self.stats_label.pack(pady=5)
        
        # Configure text colors
        self.result_text.tag_configure('3star', foreground='#00a8ff')
        self.result_text.tag_configure('4star', foreground='#9b59b6')
        self.result_text.tag_configure('5star', foreground='#f1c40f')

    def create_sprite_templates(self):
        """Generate more detailed character sprites"""
        colors = {
            3: ('#00a8ff', '#005f89'),  # Base color, accent color
            4: ('#9b59b6', '#5e2a7a'), 
            5: ('#f1c40f', '#c29f0b')
        }
        
        for tier in [3, 4, 5]:
            # Create base image
            img = Image.new('RGBA', (48, 48), (0,0,0,0))
            d = ImageDraw.Draw(img)
            base_hex, accent_hex = colors[tier]
            
            # Convert hex colors to RGB tuples
            base_color = ImageColor.getrgb(base_hex)
            accent_color = ImageColor.getrgb(accent_hex)
            
            # Background gradient
            for i in range(48):
                alpha = int(255 * (0.7 - (i/48)*0.3))
                d.line((i,0,i,47), fill=base_color + (alpha,))
            
            # Main shape
            if tier == 3:
                # Shield shape
                d.regular_polygon((24,24,20), n_sides=6, fill=accent_color)
            elif tier == 4:
                # Diamond shape
                d.polygon([(12,24), (24,12), (36,24), (24,36)], fill=accent_color)
            else:  # 5★
                # Crown shape
                d.polygon([(12,28), (24,12), (36,28), (24,24)], fill=accent_color)
                d.polygon([(18,32), (24,24), (30,32)], fill=accent_color)
            
            # Decorative border
            d.ellipse((2,2,45,45), outline=base_color, width=2)
            
            # Sparkle effect
            for _ in range(3):
                x = random.randint(5, 43)
                y = random.randint(5, 43)
                d.ellipse((x,y,x+2,y+2), fill='white')
            
            self.sprite_cache[tier] = ImageTk.PhotoImage(img.resize((32,32)))
            
    def do_pull(self):
        result = self.game.pull()
        tier = int(result[0])
        stars = "☆" * tier
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.image_create(tk.END, image=self.sprite_cache[tier])
        self.result_text.insert(tk.END, f"\nYOU GOT:\n{result}\n{stars}★", f"{tier}star")
        self.update_stats()
        
        if tier == 5:
            self.master.bell()
            self.result_text.config(bg='#2c3e50')
            self.master.after(1000, lambda: self.result_text.config(bg='black'))
        
    def show_inventory(self):
        inventory_text = "=== INVENTORY ===\n"
        for char, count in sorted(self.game.inventory.items(), 
                                key=lambda x: -int(x[0][0])):
            inventory_text += f"{char}: {count}x\n"
            
        messagebox.showinfo("Inventory", inventory_text)
        
    def update_stats(self):
        total_pulls = sum(self.game.inventory.values())
        stats_text = f"Pulls: {total_pulls} | 5★ Pity: {self.game.pity_counter}/50"
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GachaponGUI(root)
    root.mainloop()