"""
league_hotkey.py

Press Ctrl+Alt+L anywhere on your system to launch League of Legends.
Press Ctrl+Alt+Q anywhere to quit this script.

This listens for its own dedicated hotkey combo system-wide — the same
mechanism apps like Discord (push-to-talk) or OBS (start recording) use.
It does NOT intercept clicks, override other shortcuts, or run hidden;
you'll see this console window the whole time it's active, and the quit
hotkey always works.

Requires: pip install keyboard
On Windows, global hotkeys need this run from an elevated (Administrator)
terminal to register reliably in all apps/games.
"""

import keyboard
import subprocess
import os
import time
import ctypes
from ctypes import wintypes

# ---- config ----
LEAGUE_PATH = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
LEAGUE_ARGS = ["--launch-product=league_of_legends", "--launch-patchline=live"]

LAUNCH_HOTKEY = "ctrl+alt+l"
QUIT_HOTKEY = "ctrl+alt+q"

# window titles to look for once launched, so we can force them forward
WINDOW_TITLE_HINTS = ["league of legends", "riot client"]


# ---- force the League/Riot window to the front, even from a background hotkey ----
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)


def _find_window_by_title(hints):
    hints = [h.lower() for h in hints]
    found = []

    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value.lower()
                if any(h in title for h in hints):
                    found.append(hwnd)
        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return found[0] if found else None


def _force_foreground(hwnd):
    if not hwnd:
        return
    fg_hwnd = user32.GetForegroundWindow()
    current_thread = kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(current_thread, target_thread, True)
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(current_thread, target_thread, False)


def _bring_league_forward(timeout_s=6.0, poll_s=0.5):
    waited = 0.0
    while waited < timeout_s:
        hwnd = _find_window_by_title(WINDOW_TITLE_HINTS)
        if hwnd:
            _force_foreground(hwnd)
            return True
        time.sleep(poll_s)
        waited += poll_s
    return False


def launch_league():
    print("Launching League...")
    try:
        if os.path.exists(LEAGUE_PATH):
            subprocess.Popen([LEAGUE_PATH] + LEAGUE_ARGS)
            if _bring_league_forward():
                print("Brought League/Riot window to the front.")
            else:
                print("Launched, but couldn't find the window to bring forward.")
        else:
            print(f"League client not found at: {LEAGUE_PATH}")
            print("Update LEAGUE_PATH at the top of the script.")
    except Exception as e:
        print(f"Couldn't launch League: {e}")


def main():
    print(f"Ready.")
    print(f"  {LAUNCH_HOTKEY}  -> launch League")
    print(f"  {QUIT_HOTKEY}  -> quit this script")

    keyboard.add_hotkey(LAUNCH_HOTKEY, launch_league)
    keyboard.wait(QUIT_HOTKEY)  # blocks here until the quit hotkey fires

    print("Quit hotkey pressed — exiting.")


if __name__ == "__main__":
    main()