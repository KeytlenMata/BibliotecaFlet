import flet as ft
import unicodedata
from models.libros import registrar_libro, libros, eliminar_libro, actualizar_libro
from models.clientes import clientes

def quitar_acentos(texto):
    """Elimina acentos y caracteres especiales, y devuelve en minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

class InventoryView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        
        # Inputs
        self.titulo_input = ft.TextField(label="Título", border_color=ft.colors.OUTLINE, width=300)
        self.autor_input = ft.TextField(label="Autor", border_color=ft.colors.OUTLINE, width=200)
        self.isbn_input = ft.TextField(label="ISBN", border_color=ft.colors.OUTLINE, width=300)
        self.msg = ft.Text(size=12)
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar libro",
            hint_text="Título, autor o ISBN...",
            prefix_icon=ft.icons.SEARCH,
            width=300,
            on_change=self._on_search_change,
            border_color=ft.colors.OUTLINE
        )
        
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
            self.search_field,
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
            libros_ordenados = sorted(
                libros,
                key=lambda l: quitar_acentos(l["titulo"])
            )
            for l in libros_ordenados:
                estado = "Disponible" if l.get("disponible", True) else "Prestado"
                color_estado = ft.colors.GREEN if estado == "Disponible" else ft.colors.RED
                # ✅ Añadir botones de acción
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.PRIMARY),
                            ft.Column([
                                ft.Text(f"{l['titulo']}", weight="bold", color=ft.colors.ON_SURFACE),
                                ft.Text(f"Autor: {l['autor']}", size=13, color=ft.colors.ON_SURFACE_VARIANT),
                                ft.Text(f"ISBN: {l['isbn']}", size=12, color=ft.colors.ON_SURFACE_VARIANT),
                            ], expand=True),
                            ft.Container(
                                content=ft.Text(estado, size=12, color=ft.colors.ON_PRIMARY),
                                bgcolor=color_estado,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE_400,
                                tooltip="Editar",
                                on_click=lambda e, libro=l: self._editar_libro_dialog(libro)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                                tooltip="Eliminar",
                                on_click=lambda e, libro=l: self._eliminar_libro(libro["isbn"])
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

    def _on_search_change(self, e):
        termino = e.control.value.strip()
        self.list_view.controls.clear()

        if not termino:
            filtered_libros = sorted(
                libros,
                key=lambda l: quitar_acentos(l["titulo"])
            )
        else:
            termino_normalizado = quitar_acentos(termino)
            filtered_libros = [
                l for l in libros
                if termino_normalizado in quitar_acentos(l["titulo"]) or
                   termino_normalizado in quitar_acentos(l["autor"]) or
                   termino_normalizado in l["isbn"].lower()
            ]
            filtered_libros = sorted(
                filtered_libros,
                key=lambda l: quitar_acentos(l["titulo"])
            )

        if not filtered_libros:
            self.list_view.controls.append(
                ft.Text("No se encontraron libros.", color=ft.colors.ON_SURFACE_VARIANT)
            )
        else:
            for l in filtered_libros:
                estado = "Disponible" if l.get("disponible", True) else "Prestado"
                color_estado = ft.colors.GREEN if estado == "Disponible" else ft.colors.RED
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.PRIMARY),
                            ft.Column([
                                ft.Text(f"{l['titulo']}", weight="bold", color=ft.colors.ON_SURFACE),
                                ft.Text(f"Autor: {l['autor']}", size=13, color=ft.colors.ON_SURFACE_VARIANT),
                                ft.Text(f"ISBN: {l['isbn']}", size=12, color=ft.colors.ON_SURFACE_VARIANT),
                            ], expand=True),
                            ft.Container(
                                content=ft.Text(estado, size=12, color=ft.colors.ON_PRIMARY),
                                bgcolor=color_estado,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE_400,
                                tooltip="Editar",
                                on_click=lambda e, libro=l: self._editar_libro_dialog(libro)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                                tooltip="Eliminar",
                                on_click=lambda e, libro=l: self._eliminar_libro(libro["isbn"])
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=5
                    )
                )

        if self.page:
            self.list_view.update()

    # === NUEVOS MÉTODOS ===

    def _editar_libro_dialog(self, libro):
        titulo_field = ft.TextField(label="Título", value=libro["titulo"], width=250)
        autor_field = ft.TextField(label="Autor", value=libro["autor"], width=250)
        
        def guardar(e):
            exito = actualizar_libro(libro["isbn"], titulo_field.value, autor_field.value)
            if exito:
                self._refresh_ui()
                dialog.open = False
                self.page.update()
            else:
                self.msg.value = "Error: campos vacíos o ISBN no encontrado."
                self.msg.color = "red"
                self.msg.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Editar Libro"),
            content=ft.Column([titulo_field, autor_field], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo(dialog)),
                ft.TextButton("Guardar", on_click=guardar)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _cerrar_dialogo(self, dialog):
        dialog.open = False
        self.page.update()

    def _eliminar_libro(self, isbn):
        def confirmar(e):
            exito = eliminar_libro(isbn)
            if exito:
                self._refresh_ui()
            else:
                self.msg.value = "No se puede eliminar: el libro está prestado."
                self.msg.color = "red"
                self.msg.update()
            self.page.close_dialog()
        
        dialog = ft.AlertDialog(
            title=ft.Text("¿Eliminar libro?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog()),
                ft.TextButton("Eliminar", on_click=confirmar, style=ft.ButtonStyle(color=ft.colors.RED))
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()