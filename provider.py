# Clase que representa a un proveedor de servicios
class Provider:
    def __init__(self, id, name, service, location, rating):
        self.id = id                 # ID
        self.name = name             # Nombre del trabajador
        self.service = service       # Tipo de servicio
        self.location = location     # Ubicación
        self.rating = rating         # Calificación (1 a 5)

    # String para imprimir información completa
    def __str__(self):
        return (
            f"ID: {self.id} | Nombre: {self.name} | Servicio: {self.service} | "
            f"Ubicación: {self.location} | Calificación: {self.rating}"
        )
