import flet as ft
from datos import libros, prestamos
from models.clientes import clientes

class DashboardView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        # self.bgcolor = "#FFFFFF" # Remove to inherit theme background
        self.content = self._build_content()
    
    def _build_content(self):
        active_loans = len([p for p in prestamos if p.get("activo", True)])
        
        return ft.Column([
            ft.Text("Dashboard", size=30, weight="bold", color=ft.colors.ON_BACKGROUND),
            ft.Divider(height=20, color="transparent"),
            ft.Row(
                [
                    self._build_stat_card("Libros", str(len(libros)), ft.icons.BOOK),
                    self._build_stat_card("Clientes", str(len(clientes)), ft.icons.PEOPLE),
                    self._build_stat_card("Préstamos Activos", str(active_loans), ft.icons.SWAP_HORIZ),
                ],
                spacing=20
            )
        ])

    def _build_stat_card(self, title, value, icon):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=30, color=ft.colors.PRIMARY),
                ft.Text(value, size=40, weight="bold", color=ft.colors.ON_SURFACE),
                ft.Text(title, size=16, color=ft.colors.ON_SURFACE_VARIANT),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=150,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            padding=20,
            alignment=ft.alignment.center
        )
