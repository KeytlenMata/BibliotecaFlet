from datos import clientes, guardar_datos
from models.entities import Cliente

def validar_texto(texto: str) -> bool:
    return texto.isalpha()

def cliente_existe(cedula: str) -> bool:
    return any(c.cedula == cedula for c in clientes)

def registrar_cliente(nombre: str, apellido: str, cedula: str) -> str:
    nombre = nombre.strip()
    apellido = apellido.strip()
    cedula = cedula.strip()

    if not nombre or not apellido or not cedula:
        return "Todos los campos son obligatorios."
    if not validar_texto(nombre) or not validar_texto(apellido):
        return "Nombre y apellido solo deben contener letras."
    if cliente_existe(cedula):
        return "Ya existe un cliente con esta cédula."

    nuevo_cliente = Cliente(nombre, apellido, cedula)
    clientes.append(nuevo_cliente)
    guardar_datos()
    return ""  # éxito

def listar_clientes() -> list:
    return [{"nombre": c.nombre, "apellido": c.apellido, "cedula": c.cedula} for c in clientes]

# === NUEVAS FUNCIONES ===

def eliminar_cliente(cedula: str) -> bool:
    """
    Elimina un cliente por cédula.
    Retorna True si se eliminó, False si no se puede (tiene préstamos activos).
    """
    global clientes
    clientes = [c for c in clientes if c.cedula != cedula]
    guardar_datos()
    return True

def actualizar_cliente(cedula: str, nuevo_nombre: str, nuevo_apellido: str) -> bool:
    """
    Actualiza el nombre y apellido de un cliente.
    Retorna True si se actualizó, False si la cédula no existe.
    """
    nuevo_nombre = nuevo_nombre.strip()
    nuevo_apellido = nuevo_apellido.strip()

    if not nuevo_nombre or not nuevo_apellido:
        return False
    if not validar_texto(nuevo_nombre) or not validar_texto(nuevo_apellido):
        return False

    for c in clientes:
        if c.cedula == cedula:
            c.nombre = nuevo_nombre
            c.apellido = nuevo_apellido
            guardar_datos()
            return True
    return False
