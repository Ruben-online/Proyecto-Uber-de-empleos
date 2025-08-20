from btree import BTree
from provider import Provider

# --- Funciones de entrada y validación ---

def get_int(prompt, min_value=None, max_value=None):
    # Solicita un número entero y valida rango si aplica
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Valor inválido. Debe ser >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Valor inválido. Debe ser <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")

def get_provider_data(existing_ids):
    # Solicita datos completos de un proveedor y valida ID único
    while True:
        provider_id = get_int("Ingrese ID: ", 1)
        if provider_id in existing_ids:
            print("Ya existe un proveedor con ese ID. Intente con otro.")
        else:
            break
    name = input("Ingrese el nombre del trabajador: ")
    service = input("Ingrese el tipo de servicio: ")
    location = input("Ingrese la ubicación del trabajador: ")
    rating = get_int("Ingrese la calificación (1 a 5): ", 1, 5)
    return Provider(provider_id, name, service, location, rating)

def print_provider_list(providers):
    # Imprime todos los proveedores de una lista 
    if not providers:
        print("No hay proveedores para mostrar.")
        return
    for provider in providers:
        print(provider)

# --- Programa principal ---

def main():
    tree = BTree(order=3)         # Árbol B con orden 3
    existing_ids = set()          # Control de IDs existentes

    # Datos de ejemplo precargados
    sample_providers = [
        {"id": 1, "name": "Carlos Pérez",   "service": "electricista", "location": "Zona 1", "rating": 5},
        {"id": 2, "name": "María López",    "service": "plomero",      "location": "Zona 10", "rating": 4},
        {"id": 3, "name": "Juan Rodríguez", "service": "programador",  "location": "Zona 4", "rating": 5},
        {"id": 4, "name": "Ana García",     "service": "carpintero",   "location": "Zona 7", "rating": 3},
        {"id": 5, "name": "Pedro Martínez", "service": "albañil",      "location": "Zona 2", "rating": 4},
        {"id": 6, "name": "Lucía Hernández","service": "diseñador",    "location": "Zona 9", "rating": 5},
        {"id": 7, "name": "Roberto Díaz",   "service": "electricista", "location": "Zona 6", "rating": 4},
        {"id": 8, "name": "Sofía Torres",   "service": "plomero",      "location": "Zona 5", "rating": 5},
        {"id": 9, "name": "Andrés Ramírez", "service": "programador",  "location": "Zona 12","rating": 3},
        {"id":10, "name": "Elena Morales",  "service": "diseñador",    "location": "Zona 3", "rating": 4},
    ]
    # Insertar proveedores de ejemplo en el árbol
    for p in sample_providers:
        provider = Provider(p["id"], p["name"], p["service"], p["location"], p["rating"])
        tree.insert(provider.id, provider)
        existing_ids.add(provider.id)

    # Menú principal
    while True:
        print("\n--- Menú Uber de empleos ---")
        print("1. Registrar proveedor")
        print("2. Buscar proveedores por servicio")
        print("3. Listar proveedores ordenados por nombre")
        print("4. Listar proveedores ordenados por calificación")
        print("5. Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            # Registrar proveedor
            provider = get_provider_data(existing_ids)
            tree.insert(provider.id, provider)
            existing_ids.add(provider.id)
            print("Proveedor agregado correctamente.")

        elif option == "2":
            # Buscar por tipo de servicio
            service_query = input("Ingrese el servicio a buscar: ")
            matches = tree.search_by_service(service_query)
            if not matches:
                print("No se encontraron proveedores para ese servicio.")
            else:
                # Ordenar resultados antes de mostrar
                print("\nSeleccione el tipo de orden:")
                print("1) Por nombre (A-Z)")
                print("2) Por calificación (descendente)")
                sub = input("Opción: ").strip()
                if sub == "1":
                    matches.sort(key=lambda p: (p.name.lower(), p.id))
                elif sub == "2":
                    matches.sort(key=lambda p: (-p.rating, p.name.lower(), p.id))
                print("\nResultados:")
                print_provider_list(matches)

        elif option == "3":
            # Listar todos los proveedores ordenados por nombre
            providers = tree.collect_all()
            providers.sort(key=lambda p: (p.name.lower(), p.id))
            print("\nProveedores (ordenados por nombre):")
            print_provider_list(providers)

        elif option == "4":
            # Listar todos los proveedores ordenados por calificación
            providers = tree.collect_all()
            providers.sort(key=lambda p: (-p.rating, p.name.lower(), p.id))
            print("\nProveedores (ordenados por calificación):")
            print_provider_list(providers)

        elif option == "5":
            # Salir del programa
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
