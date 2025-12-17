class Cliente:
    def __init__(self, nombre: str, apellido: str, cedula: str):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula

    def __repr__(self):
        return f"Cliente(nombre='{self.nombre}', apellido='{self.apellido}', cedula='{self.cedula}')"
