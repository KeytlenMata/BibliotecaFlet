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
    
    # === TEMA OSCURO FIJO ===
    page.theme_mode = ft.ThemeMode.DARK
    
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_400,
            secondary=ft.colors.AMBER_300,
            error=ft.colors.RED_600,
            surface=ft.colors.GREY_800,
            background=ft.colors.GREY_900,
            on_primary=ft.colors.WHITE,
            on_secondary=ft.colors.GREY_900,
            on_background=ft.colors.WHITE,
            on_surface=ft.colors.WHITE70,
            outline=ft.colors.GREY_600,
        ),
        font_family="Segoe UI",
        use_material3=True
    )
    
    page.bgcolor = ft.colors.GREY_900

    page.window_width = 1200
    page.window_height = 800

    # Content Area
    content_area = ft.Container(expand=True, padding=0)

    def change_view(index):
        if index == 0:
            content_area.content = DashboardView()
        elif index == 1:
            content_area.content = ClientesView()
        elif index == 2:
            content_area.content = InventoryView()
        elif index == 3:
            content_area.content = LoansView()
        content_area.update()

    # Initialize Sidebar and Layout
    sidebar = Sidebar(page, change_view, None)  # Sin toggle de tema
    
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