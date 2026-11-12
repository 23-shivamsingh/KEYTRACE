# KEYTRACE — Keyboard Event Lab

**Explore how keyboard input works. Keep what you type private.**

KEYTRACE is an open-source, privacy-focused cybersecurity learning project with a modern browser dashboard and a Python desktop app. It demonstrates keyboard-event categories, typing activity, and estimated typing speed **inside a visible test field**—without silently monitoring your system.

![KEYTRACE dashboard](docs/dashboard-preview.png)

> **Educational demo:** KEYTRACE is not a system-wide keylogger. It does not capture background keystrokes, passwords from other apps, or hidden user activity.

## Features

- **Modern dashboard:** Responsive dark UI, custom KEYTRACE icon, real-time charts, and activity cards.
- **Controlled input lab:** Start a session explicitly, then type disposable sample text in the designated field.
- **Live statistics:** Key-event counts, estimated words per minute, session duration, and key categories.
- **Event stream:** Shows event *categories*, not the characters typed.
- **Privacy by design:** No login, backend, cloud database, or hidden background capture.
- **Data control:** Stop & wipe / Reset clear the demo input; JSON export contains aggregate statistics only.
- **Desktop companion:** Tkinter application with the same visible, opt-in approach.
- **Automated checks:** Python and JavaScript unit tests run in GitHub Actions.

## Preview

| Desktop dashboard | Mobile layout |
| --- | --- |
| ![Desktop preview](docs/dashboard-preview.png) | ![Mobile preview](docs/mobile-preview.png) |

## Project structure

```text
KEYTRACE/
├── .github/workflows/
│   ├── pages.yml           # Publish the website with GitHub Pages
│   └── test.yml            # Run Python and JavaScript tests
├── docs/                   # Screenshots, source review, validation notes
├── keyboard_lab/           # Desktop session/statistics logic
├── tests/                  # Python unit tests
├── web/
│   ├── assets/             # Custom app icon and favicon
│   ├── index.html          # Dashboard
│   ├── styles.css          # Responsive design
│   ├── app.js              # Dashboard interactions
│   ├── metrics.js          # Statistics helpers
│   └── metrics.test.cjs    # JavaScript unit tests
├── keylogger.py            # Desktop application entry point
├── requirements.txt       # No third-party Python dependencies
├── LICENSE
└── README.md
```

## Run the website locally

**Requirements:** Python 3 (only to run the optional local static server). The website itself uses plain HTML, CSS, and JavaScript; no npm installation is required.

```bash
git clone https://github.com/23-shivamsingh/KEYTRACE.git
cd KEYTRACE
python3 -m http.server 8000
```

Open **http://localhost:8000/web/** in a browser. Alternatively, open `web/index.html` directly.

**Try it:** Check the consent box → select **Start session** → type sample text in the playground → review the statistics → select **Stop & wipe**. Do not enter personal data or passwords.

## Run the desktop application

**Requirements:** Python 3.10+ with Tkinter available.

```bash
python3 keylogger.py
```

The desktop app counts events only within its own visible demo field; it does not request system-wide keyboard monitoring access. On Windows, use `py keylogger.py` if `python3` is unavailable.

## Run tests

Python tests:

```bash
python3 -m unittest discover -s tests -v
```

JavaScript tests (requires Node.js):

```bash
node --test web/metrics.test.cjs
```

Both suites also run automatically through `.github/workflows/test.yml` when you push commits or open pull requests.

## Deploy with GitHub Pages

1. Push the complete project to the `main` branch of your GitHub repository.
2. Open **Settings → Pages → Build and deployment**.
3. Set **Source** to **GitHub Actions**.
4. Check **Actions → Publish KEYTRACE website** for the deployment result.

The included `.github/workflows/pages.yml` publishes the contents of `web/` automatically. After a successful deployment, the website should be available at:

**https://23-shivamsingh.github.io/KEYTRACE/**

The public website is a standalone, in-browser demonstration. It does not connect to the Python desktop application or require an API server.

## Privacy and limitations

- Only events inside the explicitly selected input field are measured.
- Typed characters are not written to exported reports or the event-category feed.
- The input field temporarily shows the sample text while you type; **Stop & wipe** or **Reset** clears it.
- Estimated WPM is an approximation based on key-event counts, not a precise typing assessment.
- The project does not provide remote monitoring, authentication, a database, or a WebSocket API.

## Background, license and attribution

KEYTRACE is a redesigned, consent-based educational project developed from the idea and MIT-licensed starting point of [ramprasathmk/keylogger](https://github.com/ramprasathmk/keylogger). The new version uses a different interface and intentionally does **not** retain the original system-wide keylogging behavior.

The original MIT copyright and permission notice is preserved in [`LICENSE`](LICENSE). The redesigned interface and additional educational functionality are maintained in this repository.

---

**Built for cybersecurity education, experimentation, and privacy-aware software design.**
