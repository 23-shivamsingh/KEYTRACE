import unittest

from keyboard_lab.session import KeyboardSession, classify_key


class Clock:
    now = 100.0

    def __call__(self):
        return self.now


class SessionTests(unittest.TestCase):
    def test_classification_does_not_return_character(self):
        self.assertEqual(classify_key("a", "a"), "letters")
        self.assertEqual(classify_key("1", "1"), "numbers")
        self.assertEqual(classify_key("BackSpace", "\b"), "editing")
        self.assertEqual(classify_key("Left"), "navigation")
        self.assertEqual(classify_key("Control_L"), "other")

    def test_explicit_start_and_stop(self):
        clock = Clock()
        session = KeyboardSession(clock=clock)
        self.assertIsNone(session.record_key("a", "a"))
        self.assertTrue(session.start())
        self.assertFalse(session.start())
        session.record_key("a", "a")
        clock.now += 12
        session.record_key("Return", "\r")
        self.assertEqual(session.key_count, 2)
        self.assertTrue(session.stop())
        self.assertFalse(session.stop())
        self.assertEqual(session.elapsed_seconds, 12)
        self.assertEqual(session.categories["letters"], 1)
        self.assertEqual(session.categories["editing"], 1)

    def test_no_raw_text_saved_in_reports_or_events(self):
        clock = Clock()
        session = KeyboardSession(clock=clock)
        session.start()
        private_text = "DoNotStoreMe"
        for letter in private_text:
            session.record_key(letter, letter)
        import json
        serialized = json.dumps({"report": session.report(), "events": session.events})
        self.assertNotIn(private_text, serialized)
        self.assertNotIn("DoNotStoreMe", serialized)
        self.assertNotIn("D", serialized.split('"events"')[1])
        self.assertEqual(session.key_count, len(private_text))

    def test_restart_uses_fresh_state(self):
        session = KeyboardSession()
        session.start()
        session.record_key("1", "1")
        session.stop()
        session.start()
        self.assertEqual(session.key_count, 0)
        self.assertEqual(session.report()["categories"]["numbers"], 0)

    def test_estimated_wpm(self):
        clock = Clock()
        session = KeyboardSession(clock=clock)
        session.start()
        for _ in range(50):
            session.record_key("a", "a")
        clock.now += 60
        self.assertEqual(session.wpm, 10)


if __name__ == "__main__":
    unittest.main()
