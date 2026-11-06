import json
import tempfile
import unittest
from pathlib import Path

from src.services.SettingsStore import AppSettings, SettingsStore
from src.models.TimerTemplate import TimerStep, TimerTemplate


class SettingsStoreTests(unittest.TestCase):
    def test_loads_legacy_settings_and_saves_composed_templates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(
                json.dumps(
                    {
                        "theme": "light",
                        "templates": [{"name": "Foco", "minutes": 25}],
                    }
                ),
                encoding="utf-8",
            )
            store = SettingsStore(path)

            loaded = store.load()
            self.assertEqual(loaded.templates[0].steps[0].minutes, 25)

            composed = TimerTemplate(
                "Pomodoro",
                (TimerStep("Foco", 25), TimerStep("Pausa", 5)),
                4,
            )
            store.save(AppSettings("dark", (composed,)))
            saved = store.load()

            self.assertEqual(saved.theme, "dark")
            self.assertEqual(saved.templates, (composed,))


if __name__ == "__main__":
    unittest.main()
