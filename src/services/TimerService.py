import math
import time
from dataclasses import dataclass
from typing import Callable

from src.models.TimerTemplate import TimerTemplate


@dataclass(frozen=True)
class TimerDisplay:
    seconds: int
    running: bool
    mode: str | None
    step_name: str | None = None
    cycle: int | None = None
    total_cycles: int | None = None


class TimerService:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._mode: str | None = None
        self._running = False
        self._elapsed_before_start = 0.0
        self._started_at: float | None = None
        self._template: TimerTemplate | None = None

    @property
    def running(self) -> bool:
        return self._running

    def start_stopwatch(self) -> None:
        self._mode = "stopwatch"
        self._template = None
        self._elapsed_before_start = 0.0
        self._start()

    def start_template(self, template: TimerTemplate) -> None:
        self._mode = "sequence"
        self._template = template
        self._elapsed_before_start = 0.0
        self._start()

    def stop(self) -> None:
        self._mode = None
        self._template = None
        self._running = False
        self._elapsed_before_start = 0.0
        self._started_at = None

    def _start(self) -> None:
        self._started_at = self._clock()
        self._running = True

    def _elapsed_seconds(self) -> float:
        elapsed = self._elapsed_before_start
        if self._running and self._started_at is not None:
            elapsed += self._clock() - self._started_at
        return elapsed

    def update(self) -> bool:
        if (
            self._running
            and self._template is not None
            and self._elapsed_seconds() >= self._total_duration()
        ):
            self._elapsed_before_start = float(self._total_duration())
            self._started_at = None
            self._running = False
            return True
        return False

    def display(self) -> TimerDisplay:
        elapsed = self._elapsed_seconds()
        if self._template is None:
            return TimerDisplay(
                seconds=int(elapsed), running=self._running, mode=self._mode
            )

        stage_durations = [
            step.duration_seconds
            for _ in range(self._template.cycles)
            for step in self._template.steps
        ]
        stage_index, stage_elapsed = self._current_stage(elapsed, stage_durations)
        step = self._template.steps[stage_index % len(self._template.steps)]
        remaining = max(0, math.ceil(stage_durations[stage_index] - stage_elapsed))
        return TimerDisplay(
            seconds=remaining,
            running=self._running,
            mode=self._mode,
            step_name=step.name,
            cycle=stage_index // len(self._template.steps) + 1,
            total_cycles=self._template.cycles,
        )

    def _total_duration(self) -> int:
        if self._template is None:
            return 0
        return sum(step.duration_seconds for step in self._template.steps) * (
            self._template.cycles
        )

    @staticmethod
    def _current_stage(
        elapsed: float, stage_durations: list[int]
    ) -> tuple[int, float]:
        remaining_elapsed = elapsed
        for index, duration in enumerate(stage_durations):
            if remaining_elapsed < duration:
                return index, remaining_elapsed
            remaining_elapsed -= duration
        return len(stage_durations) - 1, float(stage_durations[-1])
