import flet as ft

class Sidebar(ft.Container):
    def __init__(self, app, on_nav_change, on_theme_toggle=None):
        super().__init__()
        self.app = app
        self.on_nav_change = on_nav_change
        self.width = 250
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.padding = 20
        self.content = ft.Column(
            controls=[
                self._build_header(),
                ft.Divider(color="transparent", height=20),
                self._build_nav_item("Dashboard", ft.icons.DASHBOARD_OUTLINED, 0),
                self._build_nav_item("Clientes", ft.icons.PEOPLE_OUTLINE, 1),
                self._build_nav_item("Inventario", ft.icons.BOOK_OUTLINED, 2),
                self._build_nav_item("Préstamos", ft.icons.SWAP_HORIZ, 3),
                # --- Tema eliminado: solo modo oscuro ---
            ],
            spacing=5
        )

    def _build_header(self):
        return ft.Row(
            [
                ft.Icon(ft.icons.LIBRARY_BOOKS, color=ft.colors.PRIMARY),
                ft.Text("Biblioteca", weight="bold", color=ft.colors.ON_SURFACE, size=16),
            ],
            alignment=ft.MainAxisAlignment.START
        )

    def _build_nav_item(self, text, icon, index):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=ft.colors.ON_SURFACE),
                    ft.Text(text, color=ft.colors.ON_SURFACE, size=14),
                ],
                spacing=10
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            border_radius=5,
            ink=True,
            on_click=lambda e: self.on_nav_change(index),
            on_hover=lambda e: self._on_hover_item(e),
        )

    def _on_hover_item(self, e):
        e.control.bgcolor = ft.colors.SECONDARY_CONTAINER if e.data == "true" else "transparent"
        e.control.update()