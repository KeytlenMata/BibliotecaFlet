import flet as ft
from components.sidebar import Sidebar
from views.dashboard_view import DashboardView
from views.clientes_view import ClientesView
from views.inventory_view import InventoryView
from views.loans_view import LoansView
from datos import cargar_datos

def main(page: ft.Page):
    # Cargar datos al iniciar la app
    cargar_datos()

    page.title = "Sistema de Biblioteca Profesional"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.dark_theme = ft.Theme(color_scheme_seed="blue")
    
    page.window_width = 1200
    page.window_height = 800

    # Content Area
    content_area = ft.Container(expand=True, padding=0)

    def change_view(index):
        # Re-instantiate view to ensure fresh data
        if index == 0:
            content_area.content = DashboardView()
        elif index == 1:
            content_area.content = ClientesView()
        elif index == 2:
            content_area.content = InventoryView()
        elif index == 3:
            content_area.content = LoansView()
        content_area.update()

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    # Initialize Sidebar and Layout
    sidebar = Sidebar(page, change_view, toggle_theme)
    
    page.add(
        ft.Row(
            [
                sidebar,
                content_area
            ],
            expand=True,
            spacing=0
        )
    )

    # Set initial view
    change_view(0)

if __name__ == "__main__":
    ft.app(target=main)
