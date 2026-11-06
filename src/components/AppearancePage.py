from collections.abc import Callable
from typing import Any

import customtkinter as ctk


class AppearancePage(ctk.CTkFrame):
    def __init__(
        self, master: Any, theme: str, on_theme_change: Callable[[str], None]
    ) -> None:
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(
            self,
            text="Aparência",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(anchor="w", pady=(8, 20))
        ctk.CTkLabel(
            self,
            text="Escolha o tema do aplicativo.",
            text_color=("gray35", "gray70"),
        ).pack(anchor="w", pady=(0, 12))

        self.theme_selector = ctk.CTkSegmentedButton(
            self,
            values=["Claro", "Escuro"],
            command=on_theme_change,
        )
        self.theme_selector.set("Claro" if theme == "light" else "Escuro")
        self.theme_selector.pack(anchor="w")
