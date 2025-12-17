import flet as ft
from models.clientes import registrar_cliente, clientes

class ClientesView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        # self.bgcolor = "#FFFFFF"
        
        # Inputs
        self.nombre_input = ft.TextField(label="Nombre", border_color=ft.colors.OUTLINE, width=250)
        self.apellido_input = ft.TextField(label="Apellido", border_color=ft.colors.OUTLINE, width=250)
        self.cedula_input = ft.TextField(label="Cédula", border_color=ft.colors.OUTLINE, width=250)
        self.msg = ft.Text(size=12)
        
        self.list_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.content = self._build_content()
        self._refresh_list()

    def _build_content(self):
        return ft.Column([
            ft.Text("Clientes", size=30, weight="bold", color=ft.colors.ON_BACKGROUND),
            ft.Divider(height=20, color="transparent"),
            
            # Form
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
            for c in clientes:
                self.list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.PERSON, color=ft.colors.PRIMARY),
                            ft.Text(f"{c.nombre} {c.apellido}", weight="bold", color=ft.colors.ON_SURFACE),
                            ft.Text(f"ID: {c.cedula}", color=ft.colors.ON_SURFACE_VARIANT),
                        ], spacing=20),
                        padding=15,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=5
                    )
                )
        if self.page:
            self.list_view.update()
