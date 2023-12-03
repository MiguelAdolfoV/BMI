import random

class Producto:
    nombres_productos = ["Bottle Label", "Bottle Smooth", "Can Round", "Can Slim", "Candy Bar", "Milk Carton Large", "Milk Carton Small", "Punch Straw Drink", "Snack Bag"]

    def __init__(self, nombre):
        self.nombre = nombre
        self.posicion = None  # La posición se generará después
        self.precio = self.generar_precio()

    def generar_posicion(self, posiciones_asignadas):
        # Generar un número aleatorio entre 1 y 9 para la posición sin repetir
        posicion_propuesta = random.randint(1, 9)
        while posicion_propuesta in posiciones_asignadas:
            posicion_propuesta = random.randint(1, 9)
        return posicion_propuesta

    def generar_precio(self):
        # Generar un número aleatorio en intervalos de 100 entre 100 y 1000
        return random.randrange(100, 1001, 100)

    @classmethod
    def generar_productos(cls):
        posiciones_asignadas = set()
        productos = []

        for nombre in cls.nombres_productos:
            producto = cls(nombre)
            producto.posicion = producto.generar_posicion(posiciones_asignadas)
            posiciones_asignadas.add(producto.posicion)
            productos.append(producto)

        return productos

    @classmethod
    def productos_aleatorios(cls, n):
        productos_disponibles = cls.generar_productos()

        if n > len(productos_disponibles):
            raise ValueError("No hay suficientes productos disponibles.")

        productos_seleccionados = random.sample(productos_disponibles, n)

        return productos_seleccionados
