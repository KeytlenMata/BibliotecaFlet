import flet as ft
import unicodedata
from models.clientes import registrar_cliente, clientes, eliminar_cliente, actualizar_cliente

def quitar_acentos(texto):
    """Elimina acentos y caracteres especiales, y devuelve en minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

class ClientesView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        
        # Inputs
        self.nombre_input = ft.TextField(label="Nombre", border_color=ft.colors.OUTLINE, width=250)
        self.apellido_input = ft.TextField(label="Apellido", border_color=ft.colors.OUTLINE, width=250)
        self.cedula_input = ft.TextField(label="Cédula", border_color=ft.colors.OUTLINE, width=250)
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar cliente",
            hint_text="Nombre, apellido o cédula...",
            prefix_icon=ft.icons.SEARCH,
            width=300,
            on_change=self._on_search_change,
            border_color=ft.colors.OUTLINE
        )
        
        self.msg = ft.Text(size=12)
        
        self.list_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.content = self._build_content()
        self._refresh_list()

    def _build_content(self):
        return ft.Column([
            ft.Text("Clientes", size=30, weight="bold", color=ft.colors.ON_BACKGROUND),
            ft.Divider(height=20, color="transparent"),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Nuevo Cliente", size=16, weight="bold", color=ft.colors.ON_SURFACE),
                    ft.Row([self.nombre_input, self.apellido_input, self.cedula_input], wrap=True),
                    ft.Row([
                        ft.ElevatedButton(
                            "Agregar Cliente", 
                            on_click=self._agregar_cliente,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5)
                            )
                        ),
                        self.msg
                    ])
                ], spacing=15),
                padding=20,
                border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
                border_radius=10
            ),
            
            ft.Divider(height=30, color="transparent"),
            ft.Text("Lista de Clientes", size=16, weight="bold", color=ft.colors.ON_BACKGROUND),
            self.search_field,
            self.list_view
        ], expand=True)

    def _agregar_cliente(self, e):
        res = registrar_cliente(self.nombre_input.value, self.apellido_input.value, self.cedula_input.value)
        if res == "":
            self.msg.value = "Cliente agregado."
            self.msg.color = "green"
            self.nombre_input.value = ""
            self.apellido_input.value = ""
            self.cedula_input.value = ""
            self._refresh_list()
        else:
            self.msg.value = res
            self.msg.color = "red"
        self.msg.update()
        self.nombre_input.update()
        self.apellido_input.update()
        self.cedula_input.update()

    def _refresh_list(self):
        self.list_view.controls.clear()
        if not clientes:
            self.list_view.controls.append(ft.Text("No hay clientes registrados.", color="#787774"))
        else:
            clientes_ordenados = sorted(
                clientes,
                key=lambda c: (quitar_acentos(c.apellido), quitar_acentos(c.nombre))
            )
            for c in clientes_ordenados:
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.PERSON, color=ft.colors.PRIMARY),
                            ft.Column([
                                ft.Text(f"{c.nombre} {c.apellido}", weight="bold", color=ft.colors.ON_SURFACE),
                                ft.Text(f"Cédula: {c.cedula}", size=13, color=ft.colors.ON_SURFACE_VARIANT),
                            ], expand=True),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE_400,
                                tooltip="Editar",
                                on_click=lambda e, cliente=c: self._editar_cliente_dialog(cliente)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                                tooltip="Eliminar",
                                on_click=lambda e, cliente=c: self._eliminar_cliente(cliente.cedula)
                            )
                        ], spacing=15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=5
                    )
                )
        if self.page:
            self.list_view.update()

    def _on_search_change(self, e):
        termino = e.control.value.strip()
        self.list_view.controls.clear()

        if not termino:
            filtered_clientes = sorted(
                clientes,
                key=lambda c: (quitar_acentos(c.apellido), quitar_acentos(c.nombre))
            )
        else:
            termino_normalizado = quitar_acentos(termino)
            filtered_clientes = [
                c for c in clientes
                if termino_normalizado in quitar_acentos(c.nombre) or
                   termino_normalizado in quitar_acentos(c.apellido) or
                   termino_normalizado in c.cedula.lower()
            ]
            filtered_clientes = sorted(
                filtered_clientes,
                key=lambda c: (quitar_acentos(c.apellido), quitar_acentos(c.nombre))
            )

        if not filtered_clientes:
            self.list_view.controls.append(
                ft.Text("No se encontraron clientes.", color="#787774")
            )
        else:
            for c in filtered_clientes:
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.PERSON, color=ft.colors.PRIMARY),
                            ft.Column([
                                ft.Text(f"{c.nombre} {c.apellido}", weight="bold", color=ft.colors.ON_SURFACE),
                                ft.Text(f"Cédula: {c.cedula}", size=13, color=ft.colors.ON_SURFACE_VARIANT),
                            ], expand=True),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE_400,
                                tooltip="Editar",
                                on_click=lambda e, cliente=c: self._editar_cliente_dialog(cliente)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                                tooltip="Eliminar",
                                on_click=lambda e, cliente=c: self._eliminar_cliente(cliente.cedula)
                            )
                        ], spacing=15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=5
                    )
                )

        if self.page:
            self.list_view.update()

    def _editar_cliente_dialog(self, cliente):
        nombre_field = ft.TextField(label="Nombre", value=cliente.nombre, width=200)
        apellido_field = ft.TextField(label="Apellido", value=cliente.apellido, width=200)
        
        def guardar(e):
            exito = actualizar_cliente(cliente.cedula, nombre_field.value, apellido_field.value)
            if exito:
                self._refresh_list()
                dialog.open = False
                self.page.update()
            else:
                self.msg.value = "Error: campos vacíos o contienen números."
                self.msg.color = "red"
                self.msg.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Editar Cliente"),
            content=ft.Column([nombre_field, apellido_field], tight=True),
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

    def _eliminar_cliente(self, cedula):
        # ✅ VALIDACIÓN DE PRÉSTAMOS ACTIVOS (sin import circular)
        from models.prestamos import prestamos
        tiene_prestamos_activos = any(
            p.get("activo", False) and p["cedula"] == cedula
            for p in prestamos
        )

        def confirmar(e):
            if tiene_prestamos_activos:
                self.msg.value = "No se puede eliminar: cliente tiene préstamos activos."
                self.msg.color = "red"
                self.msg.update()
                self.page.close_dialog()
                return

            exito = eliminar_cliente(cedula)
            if exito:
                self._refresh_list()
            else:
                self.msg.value = "Error al eliminar cliente."
                self.msg.color = "red"
                self.msg.update()
            self.page.close_dialog()
        
        dialog = ft.AlertDialog(
            title=ft.Text("¿Eliminar cliente?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog()),
                ft.TextButton("Eliminar", on_click=confirmar, style=ft.ButtonStyle(color=ft.colors.RED))
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()