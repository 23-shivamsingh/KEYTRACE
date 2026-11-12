# Validation performed (12 November 2026)

## Source review

Original upstream code was fetched and inspected through the GitHub connector, including `keylogger.py`, `README.md`, `requirements.txt`, `.gitignore`, `Code.md`, `scripts/`, `docs/`, and `out/` folder names. The original system-wide keyboard listener was **not executed**, so upstream runtime status remains unconfirmed. See `SOURCE_AUDIT.md`.

## Redesigned KEYTRACE tests

- `python -m unittest discover -s tests -v`: **5 tests passed**.
- `node --test web/metrics.test.cjs`: **3 tests passed**.
- Python compile and JavaScript syntax checks: **passed**.
- Tkinter under virtual display (`xvfb-run`): built window, Start demo, key classification, Stop/wipe, restart, page switching, Reset: **passed**.
- Chromium Playwright with HTML/CSS/JS injected into `about:blank` (environment policy blocked local HTTP and file URL navigation): opt-in required before Start, 6 keyboard events categorized, Stop erased sample text, restart, Reset, zero page errors: **passed**.
- Mobile Chromium viewport 390×844: **no horizontal overflow**.
- Headless browser preview images captured in `docs/`.

## Limitations

- Desktop GUI smoke test was performed on Linux under a virtual display. No native macOS or Windows graphical run was performed.
- Browser verification used the exact project HTML/CSS/JS injected as page content; normal GitHub Pages deployment was not exercised.
- This replacement does not attempt to validate or preserve system-wide keystroke capture; keyboard events are intentionally limited to a visible demo field.
