import unittest

from src.models.TimerTemplate import TimerTemplate


class TimerTemplateTests(unittest.TestCase):
    def test_loads_legacy_single_duration_template(self) -> None:
        template = TimerTemplate.from_dict({"name": "Foco", "minutes": 25})

        self.assertEqual(template.name, "Foco")
        self.assertEqual(template.cycles, 1)
        self.assertEqual(template.steps[0].name, "Temporizador")
        self.assertEqual(template.steps[0].minutes, 25)

    def test_rejects_non_positive_duration_and_cycles(self) -> None:
        with self.assertRaises(ValueError):
            TimerTemplate.from_dict(
                {
                    "name": "Inválido",
                    "cycles": 0,
                    "steps": [{"name": "Foco", "minutes": 25}],
                }
            )
        with self.assertRaises(ValueError):
            TimerTemplate.from_dict(
                {
                    "name": "Inválido",
                    "cycles": 1,
                    "steps": [{"name": "Foco", "minutes": True}],
                }
            )


if __name__ == "__main__":
    unittest.main()
