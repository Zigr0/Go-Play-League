"""
go_play_league.py

Every 600 seconds, pops up a reminder that says "go play league" —
unless League is already running, in which case it skips the popup.

Both buttons say "Yes" — but the LEFT one is secretly a decline
(it just closes the popup). Only the RIGHT one actually launches League.

Requires: nothing extra, uses only the Python standard library (tkinter).
Tested with Python 3.x on Windows.
"""

import tkinter as tk
import subprocess
import os

# ---- config ----
INTERVAL_MS = 600_000  # 600 seconds, in milliseconds

# Update this path if your Riot Client lives somewhere else.
LEAGUE_PATH = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
LEAGUE_ARGS = ["--launch-product=league_of_legends", "--launch-patchline=live"]

# process names to check for, covers the client and the actual game
LEAGUE_PROCESS_NAMES = [
    "LeagueClient.exe",
    "LeagueClientUx.exe",
    "League of Legends.exe",
    "RiotClientServices.exe",
]


def is_league_running():
    try:
        output = subprocess.check_output(
            "tasklist", shell=True, text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    except Exception:
        return False  # if we can't check, fall back to showing the reminder
    output_lower = output.lower()
    return any(name.lower() in output_lower for name in LEAGUE_PROCESS_NAMES)


def launch_league():
    try:
        if os.path.exists(LEAGUE_PATH):
            subprocess.Popen([LEAGUE_PATH] + LEAGUE_ARGS)
        else:
            print("League client not found at:", LEAGUE_PATH)
            print("Update LEAGUE_PATH at the top of the script.")
    except Exception as e:
        print(f"Couldn't launch League: {e}")


def show_reminder(root):
    win = tk.Toplevel(root)
    win.title("Reminder")
    win.attributes("-topmost", True)
    win.resizable(False, False)

    w, h = 320, 140
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    tk.Label(win, text="go play league", font=("Segoe UI", 14, "bold")).pack(pady=(24, 10))

    btns = tk.Frame(win)
    btns.pack()

    def decline():
        win.destroy()

    def accept():
        launch_league()
        win.destroy()

    tk.Button(btns, text="Yes", width=10, command=decline).pack(side="left", padx=15)
    tk.Button(btns, text="Yes", width=10, command=accept).pack(side="left", padx=15)

    win.bell()
    win.focus_force()


def schedule_next(root):
    if not is_league_running():
        show_reminder(root)
    root.after(INTERVAL_MS, schedule_next, root)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    schedule_next(root)
    root.mainloop()