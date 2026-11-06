import unittest

from src.models.TimerTemplate import TimerStep, TimerTemplate
from src.services.TimerService import TimerService


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


class TimerServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FakeClock()
        self.timer = TimerService(clock=self.clock)

    def test_stopwatch_counts_and_resets(self) -> None:
        self.timer.start_stopwatch()
        self.clock.now = 3.8

        self.assertEqual(self.timer.display().seconds, 3)
        self.assertTrue(self.timer.display().running)

        self.timer.stop()
        self.assertEqual(self.timer.display().seconds, 0)
        self.assertIsNone(self.timer.display().mode)

    def test_template_runs_stages_for_each_configured_cycle(self) -> None:
        template = TimerTemplate(
            name="Pomodoro",
            steps=(TimerStep("Foco", 1), TimerStep("Pausa", 2)),
            cycles=2,
        )
        self.timer.start_template(template)

        self.clock.now = 60
        display = self.timer.display()
        self.assertEqual(
            (display.step_name, display.cycle, display.seconds),
            ("Pausa", 1, 120),
        )

        self.clock.now = 180
        display = self.timer.display()
        self.assertEqual(
            (display.step_name, display.cycle, display.seconds),
            ("Foco", 2, 60),
        )

        self.clock.now = 300
        display = self.timer.display()
        self.assertEqual(
            (display.step_name, display.cycle, display.seconds),
            ("Pausa", 2, 60),
        )

        self.clock.now = 360
        self.assertTrue(self.timer.update())
        self.assertFalse(self.timer.display().running)
        self.assertEqual(self.timer.display().seconds, 0)
        self.assertFalse(self.timer.update())


if __name__ == "__main__":
    unittest.main()
