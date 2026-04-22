import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Laboratorio 07 - Ricorsione"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None

        # graphical elements
        self._title = None
        self.dd_mese: ft.Dropdown = None
        self.btn_umidita: ft.ElevatedButton = None
        self.btn_calcola_sequenza: ft.ElevatedButton = None
        self.lst_result: ft.ListView = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analisi meteo", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        self.dd_mese = ft.Dropdown(options=[ft.dropdown.Option(key="1", text="gennaio"),
                                            ft.dropdown.Option(key="2", text="febbraio"),
                                            ft.dropdown.Option(key="3", text="marzo"),
                                            ft.dropdown.Option(key="4", text="aprile"),
                                            ft.dropdown.Option(key="5", text="maggio"),
                                            ft.dropdown.Option(key="6", text="giugno"),
                                            ft.dropdown.Option(key="7", text="luglio"),
                                            ft.dropdown.Option(key="8", text="agosto"),
                                            ft.dropdown.Option(key="9", text="settembre"),
                                            ft.dropdown.Option(key="10", text="ottobre"),
                                            ft.dropdown.Option(key="11", text="novembre"),
                                            ft.dropdown.Option(key="12", text="dicembre"),],
                                   label="mese",
                                   width=200,
                                   hint_text="Selezionare un mese",
                                   on_change=self._controller.read_mese)

        self.btn_umidita = ft.ElevatedButton(text="Umidità media",
                                             tooltip="Verifica l'umidità media per città, nel mese selezionato",
                                             on_click=self._controller.handle_umidita_media)

        self.btn_calcola_sequenza = ft.ElevatedButton(text="Calcola sequenza",
                                                      tooltip="Calcola la sequenza ottimale per le analisi",
                                                      on_click=self._controller.handle_sequenza)
        row1 = ft.Row([self.dd_mese, self.btn_umidita, self.btn_calcola_sequenza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # List View where the reply is printed
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.lst_result)
        self._page.update()


    @property
    def controller(self):
        return self._controller


    @controller.setter
    def controller(self, controller):
        self._controller = controller


    def set_controller(self, controller):
        self._controller = controller


    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()


    def update_page(self):
        self._page.update()
