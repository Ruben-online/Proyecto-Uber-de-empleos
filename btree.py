from btree_node import BTreeNode

class BTree:
    def __init__(self, order):
        self.order = order
        self.root = BTreeNode(order, leaf=True)  # Inicialmente solo raíz

    # Inserción de clave/valor en el árbol
    def insert(self, key, value):
        root = self.root
        # Si la raíz está llena, crear nueva raíz y dividir
        if len(root.keys) == (2 * self.order) - 1:
            new_root = BTreeNode(self.order, leaf=False)
            new_root.children.append(root)
            new_root.split_child(0)
            self.root = new_root
            self.root.insert_non_full(key, value)
        else:
            root.insert_non_full(key, value)

    # Recolectar todos los proveedores del árbol
    def collect_all(self):
        result = []
        self.root.collect_values(result)
        return result

    # Buscar proveedores por servicio
    def search_by_service(self, service):
        result = []
        self.root.search_by_service(service.strip().lower(), result)
        return result
