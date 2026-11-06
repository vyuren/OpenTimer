from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TimerStep:
    name: str
    minutes: int

    @property
    def duration_seconds(self) -> int:
        return self.minutes * 60


@dataclass(frozen=True)
class TimerTemplate:
    name: str
    steps: tuple[TimerStep, ...]
    cycles: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "cycles": self.cycles,
            "steps": [
                {"name": step.name, "minutes": step.minutes} for step in self.steps
            ],
        }

    @classmethod
    def from_dict(cls, data: Any) -> "TimerTemplate":
        if not isinstance(data, dict):
            raise ValueError("Cada modelo deve ser um objeto.")

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("O nome do modelo não pode ficar vazio.")

        cycles = data.get("cycles", 1)
        if not _is_positive_integer(cycles):
            raise ValueError("O número de ciclos deve ser um inteiro positivo.")

        raw_steps = data.get("steps")
        if raw_steps is None and _is_positive_integer(data.get("minutes")):
            raw_steps = [{"name": "Temporizador", "minutes": data["minutes"]}]
        if not isinstance(raw_steps, list) or not raw_steps:
            raise ValueError("Cada modelo deve ter pelo menos uma etapa.")

        steps = tuple(_parse_step(step) for step in raw_steps)
        return cls(name=name.strip(), steps=steps, cycles=cycles)


def _parse_step(data: Any) -> TimerStep:
    if not isinstance(data, dict):
        raise ValueError("Cada etapa deve ser um objeto.")
    name = data.get("name")
    minutes = data.get("minutes")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("O nome de cada etapa não pode ficar vazio.")
    if not _is_positive_integer(minutes):
        raise ValueError("A duração de cada etapa deve ser um inteiro positivo.")
    return TimerStep(name=name.strip(), minutes=minutes)


def _is_positive_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0
