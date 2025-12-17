import flet as ft
from models.libros import registrar_libro, libros
from models.clientes import clientes

class InventoryView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        # self.bgcolor = "#FFFFFF"
        
        # Inputs
        self.titulo_input = ft.TextField(label="Título", border_color=ft.colors.OUTLINE, width=300)
        self.autor_input = ft.TextField(label="Autor", border_color=ft.colors.OUTLINE, width=200)
        self.isbn_input = ft.TextField(label="ISBN", border_color=ft.colors.OUTLINE, width=300)
        self.msg = ft.Text(size=12)
        
        self.add_btn = ft.ElevatedButton(
            "Agregar Libro", 
            on_click=self._agregar_libro,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
        
        self.list_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.content = self._build_content()
        self._refresh_ui()

    def _build_content(self):
        return ft.Column([
            ft.Text("Inventario", size=30, weight="bold", color=ft.colors.ON_BACKGROUND),
            ft.Divider(height=20, color="transparent"),
            
            # Form
            ft.Container(
                content=ft.Column([
                    ft.Text("Nuevo Libro", size=16, weight="bold", color=ft.colors.ON_SURFACE),
                    ft.Row([self.titulo_input, self.autor_input, self.isbn_input], wrap=True),
                    ft.Row([
                        self.add_btn,
                        self.msg
                    ])
                ], spacing=15),
                padding=20,
                border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
                border_radius=10
            ),
            
            ft.Divider(height=30, color="transparent"),
            ft.Text("Libros Registrados", size=16, weight="bold", color=ft.colors.ON_BACKGROUND),
            self.list_view
        ], expand=True)

    def _agregar_libro(self, e):
        res = registrar_libro(self.titulo_input.value, self.autor_input.value, self.isbn_input.value)
        if res:
            self.msg.value = "Libro agregado."
            self.msg.color = "green"
            self.titulo_input.value = ""
            self.autor_input.value = ""
            self.isbn_input.value = ""
            self._refresh_ui()
        else:
            self.msg.value = "Error: Datos inválidos o ISBN duplicado."
            self.msg.color = "red"
        self.msg.update()
        self.titulo_input.update()
        self.autor_input.update()
        self.isbn_input.update()

    def _refresh_ui(self):
        # Validation Logic: Disable if no clients
        if not clientes:
            self.add_btn.disabled = True
            self.add_btn.text = "Requiere Clientes para Agregar"
            self.msg.value = "⚠️ Debes crear al menos un cliente antes de registrar libros."
            self.msg.color = ft.colors.ERROR
        else:
            self.add_btn.disabled = False
            self.add_btn.text = "Agregar Libro"
            self.msg.value = ""

        self.list_view.controls.clear()
        if not libros:
            self.list_view.controls.append(ft.Text("No hay libros registrados.", color=ft.colors.ON_SURFACE_VARIANT))
        else:
            for l in libros:
                estado = "Disponible" if l.get("disponible", True) else "Prestado"
                color_estado = ft.colors.GREEN if estado == "Disponible" else ft.colors.RED
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.PRIMARY),
                            ft.Text(f"{l['titulo']} - {l['autor']}", weight="bold", color=ft.colors.ON_SURFACE, expand=True),
                            ft.Container(
                                content=ft.Text(estado, size=12, color=ft.colors.ON_PRIMARY),
                                bgcolor=color_estado,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=5
                    )
                )
        if self.page:
            self.list_view.update()
            self.add_btn.update()
            self.msg.update()
