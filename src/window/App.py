from tkinter import messagebox

import customtkinter as ctk

from src.components.AppearancePage import AppearancePage
from src.components.HomePage import HomePage
from src.components.TemplatesPage import TemplatesPage
from src.models.TimerTemplate import TimerTemplate
from src.services.SettingsStore import AppSettings, SettingsStore
from src.services.TimerService import TimerService


class OpenTimerApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.settings_store = SettingsStore()
        try:
            self.settings = self.settings_store.load()
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Erro ao carregar configurações",
                f"Não foi possível carregar as configurações:\n{error}\n\n"
                "O aplicativo será iniciado com as configurações padrão.",
                parent=self,
            )
            self.settings = AppSettings(theme="dark", templates=())

        ctk.set_appearance_mode(self.settings.theme)
        self.timer = TimerService()
        self.home_page: HomePage | None = None

        self.title("OpenTimer")
        self.geometry("620x720")
        self.minsize(480, 560)

        self._build_navigation()
        self._show_home()
        self.after(250, self._update_timer)

    def _build_navigation(self) -> None:
        navigation = ctk.CTkFrame(self, corner_radius=0)
        navigation.pack(fill="x")
        ctk.CTkLabel(
            navigation, text="OpenTimer", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=(20, 24), pady=16)

        for label, page in (
            ("Início", self._show_home),
            ("Modelos", self._show_templates),
            ("Aparência", self._show_appearance),
        ):
            ctk.CTkButton(
                navigation,
                text=label,
                width=100,
                command=page,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray25"),
            ).pack(side="left", padx=4, pady=12)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=24, pady=24)

    def _display_page(self, page: ctk.CTkFrame) -> None:
        page.pack(fill="both", expand=True)
        self.home_page = page if isinstance(page, HomePage) else None

    def _show_home(self) -> None:
        self._clear_content()
        self._display_page(
            HomePage(self.content, self.timer.display(), self._timer_action)
        )

    def _show_templates(self) -> None:
        self._clear_content()
        self._display_page(
            TemplatesPage(
                self.content,
                self.settings.templates,
                self._save_template,
                self._delete_template,
                self._start_template,
            )
        )

    def _show_appearance(self) -> None:
        self._clear_content()
        self._display_page(
            AppearancePage(self.content, self.settings.theme, self._change_theme)
        )

    def _clear_content(self) -> None:
        self.home_page = None
        for child in self.content.winfo_children():
            child.destroy()

    def _persist_settings(self, settings: AppSettings) -> bool:
        try:
            self.settings_store.save(settings)
        except OSError as error:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar as configurações:\n{error}",
                parent=self,
            )
            return False
        self.settings = settings
        return True

    def _save_template(self, template: TimerTemplate) -> bool:
        if any(
            saved.name.casefold() == template.name.casefold()
            for saved in self.settings.templates
        ):
            messagebox.showwarning(
                "Nome já utilizado",
                "Já existe um modelo com esse nome.",
                parent=self,
            )
            return False

        return self._persist_settings(
            AppSettings(
                theme=self.settings.theme,
                templates=self.settings.templates + (template,),
            )
        )

    def _delete_template(self, template: TimerTemplate) -> bool:
        return self._persist_settings(
            AppSettings(
                theme=self.settings.theme,
                templates=tuple(
                    saved for saved in self.settings.templates if saved != template
                ),
            )
        )

    def _change_theme(self, selected_theme: str) -> None:
        theme = "light" if selected_theme == "Claro" else "dark"
        settings = AppSettings(theme=theme, templates=self.settings.templates)
        if self._persist_settings(settings):
            ctk.set_appearance_mode(theme)

    def _start_template(self, template: TimerTemplate) -> None:
        self.timer.start_template(template)
        self._show_home()

    def _timer_action(self) -> None:
        display = self.timer.display()
        if display.running or display.mode == "sequence":
            self.timer.stop()
        else:
            self.timer.start_stopwatch()
        if self.home_page is not None:
            self.home_page.update_display(self.timer.display())

    def _update_timer(self) -> None:
        if self.timer.update():
            messagebox.showinfo(
                "Tempo concluído",
                "Todas as etapas do modelo foram concluídas.",
                parent=self,
            )
        if self.home_page is not None:
            self.home_page.update_display(self.timer.display())
        self.after(250, self._update_timer)


if __name__ == "__main__":
    app = OpenTimerApp()
    app.mainloop()
