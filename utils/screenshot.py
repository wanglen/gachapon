from PIL import ImageGrab
import tkinter as tk
import os
import sys

def take_game_screenshot(root_window, filename="screenshot.png"):
    """
    Capture and save a screenshot of the game window
    Args:
        root_window (tk.Tk): Main game window instance
        filename (str): Output file name (default: screenshot.png)
    Returns:
        str: Full path to saved screenshot
    """
    try:
        # Get window coordinates
        x0 = root_window.winfo_rootx()
        y0 = root_window.winfo_rooty()
        x1 = x0 + root_window.winfo_width()
        y1 = y0 + root_window.winfo_height()
        
        # Capture window region
        screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1))
        
        # Save to file
        filepath = os.path.abspath(filename)
        screenshot.save(filepath)
        
        print(f"Game screenshot saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error capturing game window: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # For testing purposes
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")
    root.update()  # Ensure window is rendered
    take_game_screenshot(root)
    root.destroy() 