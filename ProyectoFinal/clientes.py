import flet as ft
from models import Cliente
from state import clientes


def clientes_view(page: ft.Page):

    # ---------- Campos de entrada ----------
    nombre_input = ft.TextField(label="Nombre", width=250)
    apellido_input = ft.TextField(label="Apellido", width=250)
    cedula_input = ft.TextField(label="Cédula", width=250)

    mensaje_error = ft.Text(color="red")

    lista_clientes = ft.ListView(expand=True, spacing=10)

    # ---------- Funciones ----------
    def actualizar_lista():
        lista_clientes.controls.clear()

        for cliente in clientes:
            lista_clientes.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(cliente.nombre, weight="bold"),
                            ft.Text(cliente.apellido),
                            ft.Text(f"Cédula: {cliente.cedula}")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8
                )
            )
        page.update()

    def validar_texto(texto):
        return texto.isalpha()

    def registrar_cliente(e):
        nombre = nombre_input.value.strip()
        apellido = apellido_input.value.strip()
        cedula = cedula_input.value.strip()

        # Validación campos vacíos
        if not nombre or not apellido or not cedula:
            mensaje_error.value = "Todos los campos son obligatorios."
            page.update()
            return

        # Validar texto
        if not validar_texto(nombre) or not validar_texto(apellido):
            mensaje_error.value = "Nombre y apellido solo deben contener letras."
            page.update()
            return

        # Evitar duplicados por cédula
        for c in clientes:
            if c.cedula == cedula:
                mensaje_error.value = "Ya existe un cliente con esta cédula."
                page.update()
                return

        # Registrar cliente
        nuevo_cliente = Cliente(nombre, apellido, cedula)
        clientes.append(nuevo_cliente)

        # Limpiar campos
        nombre_input.value = ""
        apellido_input.value = ""
        cedula_input.value = ""
        mensaje_error.value = ""

        actualizar_lista()

    # ---------- Vista ----------
    vista = ft.Column(
        controls=[
            ft.Text("Gestión de Clientes", size=22, weight="bold"),
            nombre_input,
            apellido_input,
            cedula_input,
            ft.ElevatedButton("Registrar Cliente", on_click=registrar_cliente),
            mensaje_error,
            ft.Divider(),
            ft.Text("Clientes Registrados", size=18),
            lista_clientes
        ],
        spacing=10
    )

    actualizar_lista()
    return vista
