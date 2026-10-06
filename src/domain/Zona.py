from decimal import Decimal

# Defines a rectangular scenario region and provides boundary and population queries.
class Zona:
    ESCENARIO_MIN = 0.0
    ESCENARIO_MAX = 1000.0

    # Validates and normalizes the zone identifier, name, coordinate bounds, and population flag.
    def __init__(self, id_zona, nombre, x_min, x_max, y_min, y_max, poblada=False):

        if not isinstance(id_zona, (int, str)):
            raise TypeError("El identificador de la zona debe ser int o str")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la zona es obligatorio")


        for valor, nombre_campo in [
            (x_min, "x_min"),
            (x_max, "x_max"),
            (y_min, "y_min"),
            (y_max, "y_max"),
        ]:
            if isinstance(valor, bool) or not isinstance(valor, (int, float, Decimal)):
                raise TypeError(f"{nombre_campo} debe ser numérico")

        x_min = float(x_min)
        x_max = float(x_max)
        y_min = float(y_min)
        y_max = float(y_max)

        if not (self.ESCENARIO_MIN <= x_min <= self.ESCENARIO_MAX and self.ESCENARIO_MIN <= x_max <= self.ESCENARIO_MAX):
            raise ValueError("Las coordenadas x deben estar dentro del escenario: 0 <= x <= 1000")
        if not (self.ESCENARIO_MIN <= y_min <= self.ESCENARIO_MAX and self.ESCENARIO_MIN <= y_max <= self.ESCENARIO_MAX):
            raise ValueError("Las coordenadas y deben estar dentro del escenario: 0 <= y <= 1000")

        if x_min > x_max:
            x_min, x_max = x_max, x_min
        if y_min > y_max:
            y_min, y_max = y_max, y_min

        self.id_zona = id_zona
        self.nombre = nombre.strip()
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.poblada = bool(poblada)

    # Checks whether a point lies within the zone bounds, including their edges.
    def contiene(self, x, y):

        if isinstance(x, bool) or not isinstance(x, (int, float, Decimal)):
            raise TypeError("La coordenada x del epicentro debe ser numérica")
        if isinstance(y, bool) or not isinstance(y, (int, float, Decimal)):
            raise TypeError("La coordenada y del epicentro debe ser numérica")
        x = float(x)
        y = float(y)
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def es_poblada(self):
        return self.poblada

    def obtener_datos(self):
        return {
            "id_zona": self.id_zona,
            "nombre": self.nombre,
            "x_min": self.x_min,
            "x_max": self.x_max,
            "y_min": self.y_min,
            "y_max": self.y_max,
            "poblada": self.poblada,
        }

    def __contains__(self, punto):

        if not isinstance(punto, (tuple, list)) or len(punto) != 2:
            return False

        x, y = punto
        return self.contiene(x, y)

    def __repr__(self):
        return (
            f"Zona(id_zona={self.id_zona!r}, nombre={self.nombre!r}, "
            f"x_min={self.x_min}, x_max={self.x_max}, "
            f"y_min={self.y_min}, y_max={self.y_max}, poblada={self.poblada})"
        )

    def __str__(self):
        return self.__repr__()


Zonas = Zona

__all__ = ["Zona", "Zonas"]
