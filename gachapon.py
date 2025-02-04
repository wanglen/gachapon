import tkinter as tk
from core.controller import GachaponController

if __name__ == "__main__":
    root = tk.Tk()
    app = GachaponController(root)
    
    # Center window on screen
    root.update_idletasks()  # Get accurate window size
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()