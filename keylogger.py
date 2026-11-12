"""KEYTRACE desktop lab (local, opt-in, in-window keyboard demonstration).

This intentionally replaces the old global key listener with a visible typing pad.
Run: python keylogger.py
"""

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from keyboard_lab import KeyboardSession

BG = "#090e18"
SIDEBAR = "#0d1420"
SURFACE = "#121e2c"
ELEVATED = "#182638"
BORDER = "#293747"
TEXT = "#f4f8f9"
MUTED = "#91a2af"
LIME = "#c5fa78"
CYAN = "#7cb9f3"
FONT = "Helvetica Neue"


class KeytraceApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("KEYTRACE  |  Keyboard Event Lab")
        self.root.geometry("1100x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)
        self.session = KeyboardSession()
        self.current_page = "lab"
        icon = Path(__file__).parent / "web" / "assets" / "icon.png"
        if icon.exists():
            try:
                self.icon = tk.PhotoImage(file=str(icon))
                self.root.iconphoto(True, self.icon)
            except tk.TclError:
                pass
        self._build()
        self._refresh()

    def _label(self, parent, text, size=12, color=TEXT, weight="normal", **kwargs):
        return tk.Label(
            parent, text=text, font=(FONT, size, weight), fg=color,
            bg=parent.cget("bg"), anchor="w", **kwargs,
        )

    def _button(self, parent, label, command, primary=False, width=14):
        return tk.Button(
            parent, text=label, command=command, width=width,
            font=(FONT, 11, "bold"), relief="flat", cursor="hand2", bd=0,
            bg=LIME if primary else ELEVATED, fg=BG if primary else TEXT,
            activebackground="#b7e76b" if primary else BORDER,
            activeforeground=BG if primary else TEXT, pady=11,
        )

    def _build(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)
        nav = tk.Frame(outer, bg=SIDEBAR, width=230, padx=22, pady=26)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)

        brand = tk.Frame(nav, bg=SIDEBAR)
        brand.pack(fill="x", pady=(0, 52))
        mark = tk.Label(brand, text="⌘", bg=LIME, fg=BG, font=(FONT, 20, "bold"), width=2)
        mark.pack(side="left", padx=(0, 12))
        tk.Label(brand, text="KEYTRACE", bg=SIDEBAR, fg=TEXT, font=(FONT, 16, "bold")).pack(side="left")
        self._label(nav, "WORKSPACE", 10, MUTED, "bold").pack(anchor="w", pady=(0, 13))
        self.lab_nav = self._button(nav, "  ⌨  Keyboard lab", lambda: self.show_page("lab"), width=20)
        self.lab_nav.pack(fill="x", pady=(0, 9))
        self.about_nav = self._button(nav, "  ◈  About & privacy", lambda: self.show_page("about"), width=20)
        self.about_nav.pack(fill="x")
        self._label(nav, "LOCAL-FIRST EDITION", 10, CYAN, "bold").pack(side="bottom", anchor="w", pady=(0, 8))
        self._label(nav, "Nothing sent to a server.", 10, MUTED).pack(side="bottom", anchor="w")

        self.content = tk.Frame(outer, bg=BG, padx=36, pady=31)
        self.content.pack(side="left", fill="both", expand=True)
        header = tk.Frame(self.content, bg=BG)
        header.pack(fill="x", pady=(0, 22))
        self._label(header, "LOCAL / INTERACTIVE LAB", 10, CYAN, "bold").pack(side="left")
        self.status = tk.Label(header, text="●  IDLE", fg=MUTED, bg=ELEVATED,
                               font=(FONT, 10, "bold"), padx=12, pady=7)
        self.status.pack(side="right")
        self.body = tk.Frame(self.content, bg=BG)
        self.body.pack(fill="both", expand=True)
        self.show_page("lab")

    def show_page(self, page):
        self.current_page = page
        for child in self.body.winfo_children():
            child.destroy()
        if page == "about":
            self._build_about()
        else:
            self._build_lab()
        self.lab_nav.config(bg=ELEVATED if page == "lab" else SIDEBAR)
        self.about_nav.config(bg=ELEVATED if page == "about" else SIDEBAR)

    def _metric(self, parent, title, initial):
        card = tk.Frame(parent, bg=SURFACE, padx=17, pady=15, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self._label(card, title.upper(), 10, MUTED, "bold").pack(anchor="w")
        value = self._label(card, initial, 26, TEXT, "bold")
        value.pack(anchor="w", pady=(8, 0))
        return value

    def _build_lab(self):
        self._label(self.body, "Explore keyboard input.", 28, TEXT, "bold").pack(anchor="w")
        self._label(self.body, "A private, opt-in experiment inside this window only.",
                    12, MUTED).pack(anchor="w", pady=(9, 26))
        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x", pady=(0, 23))
        self.events_metric = self._metric(cards, "Key presses", "0")
        self.wpm_metric = self._metric(cards, "Estimated WPM", "0")
        self.time_metric = self._metric(cards, "Elapsed", "00:00")

        panel = tk.Frame(self.body, bg=SURFACE, padx=24, pady=22,
                         highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="both", expand=True)
        top = tk.Frame(panel, bg=SURFACE)
        top.pack(fill="x", pady=(0, 16))
        self._label(top, "Live typing sandbox", 16, TEXT, "bold").pack(side="left")
        self._label(top, "ONLY INPUT IN THIS BOX IS COUNTED", 9, LIME, "bold").pack(side="right")
        self._label(panel, "Press Start, then type disposable sample text below.",
                    11, MUTED).pack(anchor="w", pady=(0, 10))

        self.pad = tk.Text(panel, height=6, wrap="word", bg=ELEVATED, fg=TEXT,
                           insertbackground=LIME, selectbackground="#41586c",
                           relief="flat", bd=0, font=("Menlo", 12), padx=14, pady=12,
                           highlightthickness=1, highlightbackground=BORDER,
                           highlightcolor=LIME)
        self.pad.pack(fill="both", expand=True)
        self.pad.bind("<KeyPress>", self.on_key)
        self.pad.config(state="disabled")
        self._label(panel, "Do not enter passwords, credentials, or personal information.",
                    10, MUTED).pack(anchor="w", pady=(10, 0))
        controls = tk.Frame(panel, bg=SURFACE)
        controls.pack(fill="x", pady=(21, 0))
        self.start_btn = self._button(controls, "Start demo", self.start, primary=True)
        self.start_btn.pack(side="left", padx=(0, 10))
        self.stop_btn = self._button(controls, "Stop & wipe", self.stop)
        self.stop_btn.pack(side="left", padx=(0, 10))
        self.export_btn = self._button(controls, "Export stats", self.export, width=13)
        self.export_btn.pack(side="left")
        self.reset_btn = self._button(controls, "Reset", self.reset, width=8)
        self.reset_btn.pack(side="right")
        self._set_button_states()

        counts = tk.Frame(self.body, bg=BG)
        counts.pack(fill="x", pady=(21, 0))
        self.category_label = self._label(counts, "Categories: no activity yet.", 11, MUTED)
        self.category_label.pack(anchor="w")

    def _build_about(self):
        self._label(self.body, "Privacy by design.", 28, TEXT, "bold").pack(anchor="w")
        self._label(self.body, "A safer way to learn how keyboard events work.",
                    13, MUTED).pack(anchor="w", pady=(9, 30))
        cards = [
            ("01  Explicit start", "Keyboard metrics are collected only after you click Start demo."),
            ("02  Window-scoped", "Only text typed in the visible sandbox is counted; not other apps."),
            ("03  No raw keystrokes", "Only summary counts and key categories are held in memory."),
            ("04  Clear on stop", "Stopping discards the sample text. Export includes only statistics."),
            ("05  Offline by default", "The desktop app has no background listener or network requests."),
        ]
        for title, description in cards:
            frame = tk.Frame(self.body, bg=SURFACE, padx=19, pady=14,
                             highlightbackground=BORDER, highlightthickness=1)
            frame.pack(fill="x", pady=(0, 12))
            self._label(frame, title, 13, LIME, "bold").pack(anchor="w")
            self._label(frame, description, 11, MUTED).pack(anchor="w", pady=(6, 0))

    def _set_button_states(self):
        if self.current_page != "lab":
            return
        active = self.session.started
        self.start_btn.config(state="disabled" if active else "normal")
        self.stop_btn.config(state="normal" if active else "disabled")
        self.export_btn.config(state="normal" if self.session.key_count > 0 else "disabled")
        self.pad.config(state="normal" if active else "disabled")

    def on_key(self, event):
        if not self.session.started:
            return "break"
        self.session.record_key(event.keysym, event.char)
        self._update_stats()
        return None

    def start(self):
        if self.session.start():
            self.pad.config(state="normal")
            self.pad.delete("1.0", "end")
            self.pad.focus_set()
            self._set_button_states()
            self._update_stats()

    def stop(self):
        if self.session.stop():
            self.pad.delete("1.0", "end")
            self._set_button_states()
            self._update_stats()

    def reset(self):
        if self.session.started:
            self.stop()
        self.session = KeyboardSession()
        if self.current_page == "lab":
            self.pad.config(state="normal")
            self.pad.delete("1.0", "end")
            self._set_button_states()
        self._update_stats()

    def export(self):
        if self.session.key_count == 0:
            messagebox.showinfo("No stats yet", "Run a test before exporting statistics.")
            return
        path = filedialog.asksaveasfilename(
            title="Save anonymous keyboard statistics", defaultextension=".json",
            initialfile="keytrace-statistics.json",
            filetypes=[("JSON", "*.json")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.session.report(), f, indent=2)
            except OSError as exc:
                messagebox.showerror("Export failed", str(exc))

    def _update_stats(self):
        self.status.config(text="●  LIVE IN SANDBOX" if self.session.started else "●  IDLE",
                           fg=LIME if self.session.started else MUTED)
        if self.current_page != "lab":
            return
        secs = int(self.session.elapsed_seconds)
        self.events_metric.config(text=str(self.session.key_count))
        self.wpm_metric.config(text=str(self.session.wpm))
        self.time_metric.config(text=f"{secs // 60:02d}:{secs % 60:02d}")
        cats = self.session.categories
        if self.session.key_count == 0:
            self.category_label.config(text="Categories: no activity yet.")
        else:
            content = "     ·     ".join(
                f"{label}: {cats.get(label, 0)}" for label in
                ("letters", "numbers", "editing", "navigation", "other")
            )
            self.category_label.config(text=content)
        self._set_button_states()

    def _refresh(self):
        self._update_stats()
        self.root.after(350, self._refresh)


def main():
    root = tk.Tk()
    KeytraceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
