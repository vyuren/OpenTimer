from collections.abc import Callable
from tkinter import messagebox
from typing import Any

import customtkinter as ctk

from src.models.TimerTemplate import TimerStep, TimerTemplate


class TemplatesPage(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master: Any,
        templates: tuple[TimerTemplate, ...],
        on_save: Callable[[TimerTemplate], bool],
        on_delete: Callable[[TimerTemplate], bool],
        on_start: Callable[[TimerTemplate], None],
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._templates = templates
        self._on_save = on_save
        self._on_delete = on_delete
        self._on_start = on_start
        self._step_inputs: list[tuple[ctk.CTkEntry, ctk.CTkEntry]] = []
        self.grid_columnconfigure(0, weight=1)
        self._build_form()
        self.template_list = ctk.CTkFrame(self, fg_color="transparent")
        self.template_list.grid(row=3, column=0, sticky="ew")
        self.template_list.grid_columnconfigure(0, weight=1)
        self._build_template_list()

    def _build_form(self) -> None:
        ctk.CTkLabel(
            self,
            text="Modelos de tempo",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w", pady=(8, 6))
        ctk.CTkLabel(
            self,
            text="Combine etapas e repita a sequência em ciclos.",
            text_color=("gray35", "gray70"),
        ).grid(row=1, column=0, sticky="w", pady=(0, 14))

        form = ctk.CTkFrame(self)
        form.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        form.grid_columnconfigure(0, weight=1)

        self.name_entry = ctk.CTkEntry(form, placeholder_text="Nome do modelo")
        self.name_entry.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="ew")
        self.cycles_entry = ctk.CTkEntry(
            form, placeholder_text="Ciclos", width=110
        )
        self.cycles_entry.insert(0, "1")
        self.cycles_entry.grid(row=0, column=1, padx=(0, 12), pady=(12, 8))

        ctk.CTkLabel(form, text="Etapas", anchor="w").grid(
            row=1, column=0, columnspan=2, padx=12, pady=(4, 4), sticky="ew"
        )
        self.stages_frame = ctk.CTkFrame(form, fg_color="transparent")
        self.stages_frame.grid(
            row=2, column=0, columnspan=2, padx=8, sticky="ew"
        )
        self.stages_frame.grid_columnconfigure(0, weight=1)
        self._add_step_row()

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=3, column=0, columnspan=2, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(
            actions,
            text="Adicionar etapa",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray25"),
            command=self._add_step_row,
        ).pack(side="left")
        ctk.CTkButton(
            actions,
            text="Salvar modelo",
            command=self._save_template,
        ).pack(side="right")

    def _add_step_row(self, values: tuple[str, str] = ("", "")) -> None:
        row = len(self._step_inputs)
        name_entry = ctk.CTkEntry(
            self.stages_frame, placeholder_text=f"Etapa {row + 1}"
        )
        if values[0]:
            name_entry.insert(0, values[0])
        name_entry.grid(row=row, column=0, padx=4, pady=4, sticky="ew")

        minutes_entry = ctk.CTkEntry(
            self.stages_frame, placeholder_text="Minutos", width=100
        )
        if values[1]:
            minutes_entry.insert(0, values[1])
        minutes_entry.grid(row=row, column=1, padx=4, pady=4)

        remove_button = ctk.CTkButton(
            self.stages_frame,
            text="×",
            width=32,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray25"),
            command=lambda entry=name_entry: self._remove_step_row(entry),
        )
        remove_button.grid(row=row, column=2, padx=4, pady=4)
        self._step_inputs.append((name_entry, minutes_entry))

    def _remove_step_row(self, target: ctk.CTkEntry) -> None:
        values = [
            (name.get(), minutes.get())
            for name, minutes in self._step_inputs
            if name is not target
        ]
        self._rebuild_step_rows(values)

    def _rebuild_step_rows(self, values: list[tuple[str, str]]) -> None:
        for child in self.stages_frame.winfo_children():
            child.destroy()
        self._step_inputs.clear()
        for row_values in values:
            self._add_step_row(row_values)

    def _save_template(self) -> None:
        name = self.name_entry.get().strip()
        if not name:
            return self._warn("Informe um nome para o modelo.")
        if any(
            template.name.casefold() == name.casefold()
            for template in self._templates
        ):
            return self._warn("Já existe um modelo com esse nome.")

        try:
            cycles_text = self.cycles_entry.get().strip()
            if not cycles_text:
                return self._warn("Informe quantos ciclos o modelo deve executar.")
            cycles = int(cycles_text)

            steps_list: list[TimerStep] = []
            for step_name, minutes in self._step_inputs:
                step_name_text = step_name.get().strip()
                minutes_text = minutes.get().strip()
                if not step_name_text:
                    return self._warn("Informe um nome para cada etapa.")
                if not minutes_text:
                    return self._warn("Informe a duração de cada etapa.")
                steps_list.append(
                    TimerStep(name=step_name_text, minutes=int(minutes_text))
                )
            steps = tuple(steps_list)
            template = TimerTemplate.from_dict(
                {
                    "name": name,
                    "cycles": cycles,
                    "steps": [
                        {"name": step.name, "minutes": step.minutes}
                        for step in steps
                    ],
                }
            )
        except ValueError as error:
            return self._warn(str(error))

        if self._on_save(template):
            self._templates += (template,)
            self.name_entry.delete(0, "end")
            self.cycles_entry.delete(0, "end")
            self.cycles_entry.insert(0, "1")
            self._rebuild_step_rows([("", "")])
            self._build_template_list()

    def _build_template_list(self) -> None:
        for child in self.template_list.winfo_children():
            child.destroy()
        ctk.CTkLabel(
            self.template_list,
            text="Modelos salvos",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, sticky="w", pady=(4, 8))
        if not self._templates:
            ctk.CTkLabel(
                self.template_list,
                text="Nenhum modelo salvo ainda.",
                text_color=("gray35", "gray70"),
            ).grid(row=1, column=0, sticky="w", pady=8)
            return

        for row, template in enumerate(self._templates, start=1):
            card = ctk.CTkFrame(self.template_list)
            card.grid(row=row, column=0, sticky="ew", pady=5)
            card.grid_columnconfigure(0, weight=1)
            stage_summary = " → ".join(
                f"{step.name} ({step.minutes} min)" for step in template.steps
            )
            ctk.CTkLabel(
                card,
                text=(
                    f"{template.name} · {template.cycles} ciclos\n{stage_summary}"
                ),
                anchor="w",
                justify="left",
            ).grid(row=0, column=0, padx=12, pady=10, sticky="ew")
            ctk.CTkButton(
                card,
                text="Iniciar",
                width=78,
                command=lambda saved=template: self._on_start(saved),
            ).grid(row=0, column=1, padx=4, pady=8)
            ctk.CTkButton(
                card,
                text="Remover",
                width=78,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray25"),
                command=lambda saved=template: self._remove_template(saved),
            ).grid(row=0, column=2, padx=(0, 8), pady=8)

    def _remove_template(self, template: TimerTemplate) -> None:
        if self._on_delete(template):
            self._templates = tuple(
                saved for saved in self._templates if saved != template
            )
            self._build_template_list()

    def _warn(self, message: str) -> None:
        messagebox.showwarning("Modelo inválido", message, parent=self)
