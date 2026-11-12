"""A foreground-only demonstration of keyboard event statistics.

No raw keystrokes, keyboard characters, or typing contents are stored by this module.
Only caller-supplied events are counted; there is no system-wide keyboard listener.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import monotonic
from typing import Callable

CATEGORIES = ("letters", "numbers", "editing", "navigation", "other")
_EDITING_KEYS = {"BackSpace", "Delete", "Return", "KP_Enter", "Tab", "space"}
_NAVIGATION_KEYS = {
    "Left", "Right", "Up", "Down", "Home", "End", "Prior", "Next",
    "Page_Up", "Page_Down", "Escape",
}


def classify_key(keysym: str, char: str = "") -> str:
    """Categorize an input field event without returning its typed character."""
    if keysym in _EDITING_KEYS:
        return "editing"
    if keysym in _NAVIGATION_KEYS:
        return "navigation"
    if len(char) == 1 and char.isalpha():
        return "letters"
    if len(char) == 1 and char.isdecimal():
        return "numbers"
    return "other"


@dataclass
class KeyboardSession:
    clock: Callable[[], float] = monotonic
    started: bool = False
    started_at: float | None = None
    finished_elapsed: float = 0.0
    key_count: int = 0
    categories: Counter[str] = field(default_factory=Counter)
    events: list[dict] = field(default_factory=list)
    recent_seconds: list[float] = field(default_factory=list)

    def start(self) -> bool:
        """Start a fresh explicitly initiated demo session."""
        if self.started:
            return False
        self.started = True
        self.started_at = self.clock()
        self.finished_elapsed = 0.0
        self.key_count = 0
        self.categories.clear()
        self.events.clear()
        self.recent_seconds.clear()
        return True

    def stop(self) -> bool:
        if not self.started:
            return False
        self.finished_elapsed = self.elapsed_seconds
        self.started = False
        return True

    @property
    def elapsed_seconds(self) -> float:
        if self.started and self.started_at is not None:
            return max(0.0, self.clock() - self.started_at)
        return self.finished_elapsed

    @property
    def wpm(self) -> int:
        """Estimate 5-character-word WPM (not typing accuracy)."""
        minutes = self.elapsed_seconds / 60
        return round((self.key_count / 5) / minutes) if minutes > 0 else 0

    def record_key(self, keysym: str, char: str = "") -> dict | None:
        """Count one key press inside the app's demo field, never its content."""
        if not self.started:
            return None
        category = classify_key(keysym, char)
        self.key_count += 1
        self.categories[category] += 1
        elapsed = round(self.elapsed_seconds, 2)
        event = {"category": category, "elapsed_seconds": elapsed}
        self.events.append(event)
        self.recent_seconds.append(elapsed)
        self.events = self.events[-80:]
        self.recent_seconds = self.recent_seconds[-1000:]
        return event

    def report(self) -> dict:
        return {
            "project": "KEYTRACE | Keyboard Event Lab",
            "privacy": "Aggregated counts only; no keystroke characters or typed text.",
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": round(self.elapsed_seconds, 2),
            "key_presses": self.key_count,
            "estimated_wpm": self.wpm,
            "categories": {k: self.categories.get(k, 0) for k in CATEGORIES},
        }
