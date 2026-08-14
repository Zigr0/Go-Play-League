# Go-play-league

Three small Windows tools that nag you to play League of Legends,
each a little more elaborate than the last.

The running gag: every popup gives you two buttons, both labeled
**"Yes"** but only one of them actually does anything. Consider
it a coin flip with worse odds.

All three are plain Python, no build step. `league_hotkey.py` needs
one extra package (`keyboard`); the other two use only the standard
library.

---

## LeagueReminder.py

Pops up every 10 minutes with **"go play league."** Automatically
skips itself if League is already running, so it won't nag you
mid-game.

```
python go_play_league.py
```

Notes:
- The "already running" check only looks for `LeagueClientUx.exe`
  and `League of Legends.exe` — not the background Riot service,
  since that one often stays resident even when you're not playing.
  If it counted the background service, the reminder would think
  League is "running" 24/7 and never fire.
- Edit `INTERVAL_MS` at the top to change the timing (it's in
  milliseconds — 600000 = 10 minutes).
- Edit `LEAGUE_PATH` if your Riot Client isn't installed at the
  default location.

---

## league_hotkey.py

Press **`Ctrl+Alt+L`** anywhere on your system to launch League.
Press **`Ctrl+Alt+Q`** anywhere to quit the script.

```
pip install keyboard
python league_hotkey.py
```

Notes:
- This listens for its own dedicated hotkey combo system-wide — the
  same mechanism apps like Discord (push-to-talk) or OBS (start
  recording) use. It does not intercept clicks, override other
  shortcuts, or hide itself.
- On Windows, global hotkeys sometimes need this run from an
  elevated (Administrator) terminal to register reliably while
  games/other apps have focus.
- If Riot Client is already running in the background, Windows can
  block its window from coming to the front even though the launch
  technically succeeds. This script works around that by finding
  the League/Riot window after launching and forcing it forward
  (standard `user32.dll` window APIs via `ctypes` — no extra
  dependency needed for that part).

---

## LeagueNagware.py

Wraps **one app of your choosing** with a confirmation gate:

> *"Are you sure you want to open [App] instead of playing League of
> Legends?"*

This is opt-in per app, not automatic or system-wide — you point one
shortcut at it, and only that shortcut gets the nag. Every other way
of opening that app (other shortcuts, taskbar search, etc.) is
untouched.

**Setup (repeat for each app you want to gate):**

1. Right-click the shortcut you want to wrap → **Properties**
2. Copy whatever is currently in **Target**
3. Replace **Target** with:
   ```
   pythonw "C:\path\to\confirm_launch.py" "<the path you just copied>"
   ```
4. Click OK.

Example, wrapping Brave:
```
pythonw "C:\path\to\confirm_launch.py" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
```

> If `pythonw` isn't recognized on your system, use `python` instead
> — it'll flash a console window briefly before the popup appears,
> which is harmless.

---

## Requirements

- Windows
- Python 3
- `pip install keyboard` (only needed for `league_hotkey.py`)

## Why these aren't "automatic" / system-wide

On purpose. Making any of these apply to *every* app without you
deliberately opting each one in would mean hooking into how Windows
launches programs generally — the same category of technique real
hijack-style malware uses, regardless of the joke framing. These
tools only ever do something because you explicitly pointed a
shortcut, hotkey, or timer at them yourself.

## License

MIT
