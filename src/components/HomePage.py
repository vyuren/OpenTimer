from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from src.components.timeButton import TimeButton
from src.services.TimerService import TimerDisplay


class HomePage(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        display: TimerDisplay,
        on_timer_action: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color="transparent")
        self._on_timer_action = on_timer_action
        self.grid_columnconfigure(0, weight=1)
        for row in range(5):
            self.grid_rowconfigure(row, weight=1)

        self.step_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16)
        )
        self.clock_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=58, weight="bold")
        )
        self.timer_button = TimeButton(
            self,
            text="",
            width=176,
            height=176,
            corner_radius=88,
            command=self._on_timer_action,
        )
        self.update_display(display)

    def update_display(self, display: TimerDisplay) -> None:
        self.timer_button.configure(
            text="Parar" if display.running else "Concluir",
        )

        if display.mode is None:
            self.step_label.grid_forget()
            self.clock_label.grid_forget()
            self.timer_button.configure(text="Iniciar cronômetro")
            self.timer_button.grid(row=2, column=0)
            return

        if display.mode == "sequence":
            step_text = display.step_name or "Contagem regressiva"
            if display.cycle is not None and display.total_cycles is not None:
                step_text += f"  ·  Ciclo {display.cycle}/{display.total_cycles}"
            self.step_label.configure(text=step_text)
            self.step_label.grid(row=1, column=0, pady=(0, 8))
        else:
            self.step_label.grid_forget()

        hours, remainder = divmod(display.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clock_label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.clock_label.grid(row=2, column=0, pady=8)
        self.timer_button.grid(row=3, column=0, pady=(16, 0))
