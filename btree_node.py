class BTreeNode:
    def __init__(self, order, leaf=True):
        self.order = order          # Grado mínimo (t) del árbol B
        self.leaf = leaf            # True si el nodo es hoja
        self.keys = []              # Lista de claves (IDs de proveedores)
        self.values = []            # Lista de objetos Provider, paralela a keys
        self.children = []          # Lista de hijos (BTreeNode), vacía si es hoja

    # Insertar una clave/valor en un nodo que no está lleno
    def insert_non_full(self, key, value):
        index = len(self.keys) - 1

        if self.leaf:
            # Inserción directa en hoja, manteniendo orden
            self.keys.append(0)    
            self.values.append(None)
            while index >= 0 and key < self.keys[index]:
                self.keys[index + 1] = self.keys[index]
                self.values[index + 1] = self.values[index]
                index -= 1
            self.keys[index + 1] = key
            self.values[index + 1] = value
        else:
            # Nodo interno: buscar hijo adecuado
            while index >= 0 and key < self.keys[index]:
                index -= 1
            child_index = index + 1

            # Si el hijo está lleno, dividirlo antes de continuar
            if len(self.children[child_index].keys) == (2 * self.order) - 1:
                self.split_child(child_index)
                if key > self.keys[child_index]:
                    child_index += 1

            # Insertar recursivamente en el hijo correspondiente
            self.children[child_index].insert_non_full(key, value)

    # Dividir un hijo que está lleno
    def split_child(self, child_index):
        t = self.order
        full_child = self.children[child_index]
        new_right = BTreeNode(t, leaf=full_child.leaf)

        # Guardar la mediana antes de recortar
        median_key = full_child.keys[t - 1]
        median_value = full_child.values[t - 1]

        # El nodo derecho toma las claves/valores después de la mediana
        new_right.keys = full_child.keys[t:]
        new_right.values = full_child.values[t:]

        # El nodo izquierdo se queda con las claves/valores anteriores a la mediana
        full_child.keys = full_child.keys[:t - 1]
        full_child.values = full_child.values[:t - 1]

        # Repartir hijos si no es hoja
        if not full_child.leaf:
            new_right.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

        # Insertar mediana y nuevo hijo en el nodo padre
        self.children.insert(child_index + 1, new_right)
        self.keys.insert(child_index, median_key)
        self.values.insert(child_index, median_value)

    # Recolectar todos los proveedores del árbol en orden (inorden)
    def collect_values(self, result_list):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].collect_values(result_list)
            result_list.append(self.values[i])
        if not self.leaf:
            self.children[len(self.keys)].collect_values(result_list)

    # Buscar proveedores por tipo de servicio 
    def search_by_service(self, service_lower, result_list):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].search_by_service(service_lower, result_list)
            if self.values[i].service.lower() == service_lower:
                result_list.append(self.values[i])
        if not self.leaf:
            self.children[len(self.keys)].search_by_service(service_lower, result_list)
