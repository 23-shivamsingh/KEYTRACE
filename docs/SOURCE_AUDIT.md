# Audit of the original `ramprasathmk/keylogger` repository

Reviewed November 12, 2026 against the public `main` branch using the GitHub repository contents API. This is a source review; the original global keyboard listener was **not executed**.

| Item | Original behavior / evidence | Impact |
| --- | --- | --- |
| Architecture | `keylogger.py`: Tkinter GUI + `pynput.keyboard.Listener` | Python desktop application, not a website; no favicon or web template exists. |
| Listener lifecycle | `_LISTENER` created once as a global; `stop_keylogger()` calls `.stop()`, `start_keylogger()` calls `.start()` on same object | `pynput` listeners are thread objects and cannot be restarted after stopping; second Start may fail. |
| GUI text | GUI announces saving to `keylogger.txt` | Actual paths in code are `out/key_log.txt` and `out/key_log.json`. |
| Output directory | File writers assume `./out` exists | Starting from a directory without the folder may raise `FileNotFoundError`. |
| File writes | `generate_json_file()` writes the whole accumulated event list on both press and release | Growing sessions cause expensive repeated writes. |
| Event semantics | `on_press` appends `Pressed` then `Held` within one function call | `Held` is not necessarily a genuinely held key; event labels can mislead. |
| Tracked logs | `out/key_log.txt` and `out/key_log.json` are committed despite `out/` in `.gitignore` | Recording files should not live in published source control; `.gitignore` does not untrack existing commits. |
| Dependency | `requirements.txt` contains unpinned `pynput` | Installation may vary by platform/version; global monitoring may need platform permission. |
| Build/testing | No automated test suite or CI in examined tree | Functionality isn't verified by automated checks. |
| Security design | Records each global keyboard event and contains README mention of hidden execution | Inappropriate for a public teaching demo without meaningful participant consent. |

## Scope and safe redesign

The replacement intentionally changes behavior, rather than attempting to make hidden recording more reliable:

- No `pynput`, background/system-wide event listener, surveillance, or credential capture.
- Desktop: input events are counted only in its visible `Text` widget after clicking Start.
- Website: browser keyboard events are counted only in the designated input box after checkbox + Start.
- No typed characters in event history, aggregate JSON, or logs. Stopping wipes the sample input.
- Modern standalone website, custom favicon, desktop app icon, tests, reproducible GitHub Pages deployment.

