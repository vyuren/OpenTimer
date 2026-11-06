import customtkinter as ctk


class TimeButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("height", 56)
        kwargs.setdefault("font", ctk.CTkFont(size=16, weight="bold"))
        super().__init__(master, **kwargs)
