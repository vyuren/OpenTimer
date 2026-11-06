import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.models.TimerTemplate import TimerTemplate


SETTINGS_PATH = Path.home() / ".opentimer" / "settings.json"


@dataclass(frozen=True)
class AppSettings:
    theme: str
    templates: tuple[TimerTemplate, ...]


class SettingsStore:
    def __init__(self, path: Path = SETTINGS_PATH) -> None:
        self._path = path

    def load(self) -> AppSettings:
        try:
            with self._path.open(encoding="utf-8") as settings_file:
                data = json.load(settings_file)
        except FileNotFoundError:
            return AppSettings(theme="dark", templates=())
        except json.JSONDecodeError as error:
            raise ValueError(f"Arquivo de configurações inválido: {error}") from error

        if not isinstance(data, dict):
            raise ValueError("As configurações devem estar em um objeto JSON.")

        theme = data.get("theme", "dark")
        raw_templates = data.get("templates", [])
        if theme not in ("light", "dark"):
            raise ValueError("O tema salvo é inválido.")
        if not isinstance(raw_templates, list):
            raise ValueError("A lista de modelos salva é inválida.")

        templates = tuple(TimerTemplate.from_dict(item) for item in raw_templates)
        return AppSettings(theme=theme, templates=templates)

    def save(self, settings: AppSettings) -> None:
        data: dict[str, Any] = {
            "theme": settings.theme,
            "templates": [template.to_dict() for template in settings.templates],
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self._path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as settings_file:
            json.dump(data, settings_file, ensure_ascii=False, indent=2)
        temporary_path.replace(self._path)
