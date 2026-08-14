"""
confirm_launch.py

Wraps any app with a confirmation nag before it actually opens.
Point a shortcut at this instead of directly at the app, and it'll ask:

    "Are you sure you want to open <App>
     instead of playing League of Legends?"

Two buttons, both say "Yes" same trick as go_play_league.py.
The LEFT one is the real decline (does nothing, app never opens).
The RIGHT one actually launches the app you originally wanted.

--- How to wire this up to a shortcut (example: Chrome) ---
1. Right-click your Chrome shortcut -> Properties
2. Copy whatever is currently in "Target"
   (e.g. "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
3. Replace "Target" with:
   pythonw "C:\\path\\to\\confirm_launch.py" "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
4. Click OK.

That shortcut now asks first. Every other way of opening Chrome
(other shortcuts, taskbar search, etc.) is completely untouched —
this only affects the one shortcut you deliberately point at it.

Requires: nothing extra, just tkinter (ships with Python on Windows).
"""

import sys
import os
import subprocess
import tkinter as tk


def main():
    if len(sys.argv) < 2:
        print("Usage: confirm_launch.py <path to app> [args...]")
        return

    target_path = sys.argv[1]
    target_args = sys.argv[2:]
    app_name = os.path.splitext(os.path.basename(target_path))[0]

    root = tk.Tk()
    root.title("Wait a second")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    w, h = 380, 170
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    msg = f"Are you sure you want to open {app_name}\ninstead of playing League of Legends?"
    tk.Label(root, text=msg, font=("Segoe UI", 11), justify="center", pady=24).pack()

    btns = tk.Frame(root)
    btns.pack(pady=10)

    def decline():
        # the fake yes — does nothing, the app never opens
        root.destroy()

    def accept():
        # the real yes — opens what you actually wanted
        try:
            if os.path.exists(target_path):
                subprocess.Popen([target_path] + target_args)
            else:
                print(f"Target not found: {target_path}")
        except Exception as e:
            print(f"Couldn't open {target_path}: {e}")
        root.destroy()

    tk.Button(btns, text="Yes", width=10, command=decline).pack(side="left", padx=15)
    tk.Button(btns, text="Yes", width=10, command=accept).pack(side="left", padx=15)

    root.bell()
    root.mainloop()


if __name__ == "__main__":
    main()