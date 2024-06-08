## Keylogger with Screenshots

This Python script logs keystrokes and takes screenshots whenever an 'Enter' key is pressed. It also captures form information and saves it to a log file (`log.txt`). The script is designed to run in the background, hidden from the user.

### Dependencies
- Python 3.x
- pynput
- ctypes
- pygetwindow
- Pillow (PIL)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/keylogger.git
   cd keylogger
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the script using Python:
   ```bash
   python keylogger.py
   ```

2. The script will start capturing keystrokes and taking screenshots when 'Enter' is pressed.

3. To stop the script, press 'Ctrl + S' together.

### Note
- Screenshots are saved in the `screenshots` directory.
- Keystroke logs are saved in `log.txt`.

### Disclaimer
This script is for educational purposes only. Be responsible and use it ethically.
