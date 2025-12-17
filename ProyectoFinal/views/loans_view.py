import flet as ft
from models.prestamos import prestar_libro, devolver_libro, prestamos
from models.libros import libros
from models.clientes import clientes

class LoansView(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = 30
        self.expand = True
        
        # Inputs
        self.libro_dropdown = ft.Dropdown(
            label="Libro", 
            width=300, 
            border_color=ft.colors.OUTLINE, 
            filled=True,
        )
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente", 
            width=300, 
            border_color=ft.colors.OUTLINE, 
            filled=True,
        )
        self.dias_input = ft.TextField(label="Días", value="7", width=100, border_color=ft.colors.OUTLINE)
        self.msg = ft.Text(size=12)
        
        # ✅ Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar préstamo",
            hint_text="Cliente o título del libro...",
            prefix_icon=ft.icons.SEARCH,
            width=300,
            on_change=self._on_search_change,
            border_color=ft.colors.OUTLINE
        )
        
        self.list_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.content = self._build_content()
        self._refresh_ui()

    def _build_content(self):
        return ft.Column([
            ft.Text("Préstamos", size=30, weight="bold", color=ft.colors.ON_BACKGROUND),
            ft.Divider(height=20, color="transparent"),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Nuevo Préstamo", size=16, weight="bold", color=ft.colors.ON_SURFACE),
                    ft.Row([self.libro_dropdown, self.cliente_dropdown, self.dias_input], wrap=True),
                    ft.Row([
                        ft.ElevatedButton(
                            "Realizar Préstamo", 
                            on_click=self._prestar,
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
            ft.Text("Préstamos Activos", size=16, weight="bold", color=ft.colors.ON_BACKGROUND),
            self.search_field,  # ✅ Campo de búsqueda insertado aquí
            self.list_view
        ], expand=True)

    def _prestar(self, e):
        if not self.libro_dropdown.value or not self.cliente_dropdown.value:
            self.msg.value = "Selecciona libro y cliente."
            self.msg.color = "red"
            self.msg.update()
            return

        try:
            dias = int(self.dias_input.value)
        except ValueError:
            self.msg.value = "Días debe ser un número."
            self.msg.color = "red"
            self.msg.update()
            return

        res = prestar_libro(self.libro_dropdown.value, self.cliente_dropdown.value, dias)
        if res:
            self.msg.value = "Préstamo realizado."
            self.msg.color = "green"
            self._refresh_ui()
        else:
            self.msg.value = "Error al realizar préstamo."
            self.msg.color = "red"
        self.msg.update()

    def _devolver(self, isbn):
        devolver_libro(isbn)
        self._refresh_ui()

    def _refresh_ui(self):
        # Update dropdowns
        self.libro_dropdown.options = [
            ft.dropdown.Option(l["isbn"], f"{l['titulo']} ({l['isbn']})")
            for l in libros if l.get("disponible", True)
        ]
        self.cliente_dropdown.options = [
            ft.dropdown.Option(c.cedula, f"{c.nombre} {c.apellido}")
            for c in clientes
        ]

        # Mostrar todos los préstamos (sin filtro)
        self._display_loans(prestamos)

        if self.page:
            self.libro_dropdown.update()
            self.cliente_dropdown.update()
            self.list_view.update()

    def _display_loans(self, loan_list):
        """Muestra una lista dada de préstamos (usado por _refresh_ui y _on_search_change)"""
        self.list_view.controls.clear()
        active_loans = [p for p in loan_list if p.get("activo", True)]
        
        if not active_loans:
            self.list_view.controls.append(ft.Text("No hay préstamos activos.", color="#787774"))
        else:
            for p in active_loans:
                libro = next((l for l in libros if l["isbn"] == p["codigo"]), {})
                cliente = next((c for c in clientes if c.cedula == p["cedula"]), None)
                if libro and cliente:
                    self.list_view.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"{libro['titulo']}", weight="bold", color=ft.colors.ON_SURFACE),
                                    ft.Text(f"Cliente: {cliente.nombre} {cliente.apellido}", size=12, color=ft.colors.ON_SURFACE_VARIANT)
                                ]),
                                ft.ElevatedButton(
                                    "Devolver", 
                                    on_click=lambda e, isbn=libro["isbn"]: self._devolver(isbn),
                                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.RED_600)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=15,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            border_radius=5
                        )
                    )

    def _on_search_change(self, e):
        termino = e.control.value.strip().lower()
        if not termino:
            # Mostrar todos
            self._display_loans(prestamos)
        else:
            # Filtrar por cliente o título del libro
            filtered_loans = []
            for p in prestamos:
                if not p.get("activo", True):
                    continue
                libro = next((l for l in libros if l["isbn"] == p["codigo"]), {})
                cliente = next((c for c in clientes if c.cedula == p["cedula"]), None)
                if libro and cliente:
                    # Buscar en título o nombre completo del cliente
                    if (termino in libro["titulo"].lower() or
                        termino in cliente.nombre.lower() or
                        termino in cliente.apellido.lower() or
                        termino in f"{cliente.nombre} {cliente.apellido}".lower()):
                        filtered_loans.append(p)
            self._display_loans(filtered_loans)
        
        if self.page:
            self.list_view.update()
