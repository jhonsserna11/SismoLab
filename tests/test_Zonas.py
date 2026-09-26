import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.domain.Zonas import Zona


def test_zona_creacion_basica():
    zona = Zona(1, "Norte", 10, 20, 30, 40, True)

    assert zona.id_zona == 1
    assert zona.nombre == "Norte"
    assert zona.x_min == 10
    assert zona.x_max == 20
    assert zona.y_min == 30
    assert zona.y_max == 40
    assert zona.poblada is True

test_zona_creacion_basica()
print("test_zona_creacion_basica: OK")


def test_zona_contiene_punto():
    zona = Zona("A", "Sur", 0, 100, 0, 50)

    assert zona.contiene(25, 25) is True
    assert zona.contiene(150, 30) is False
    assert zona.contiene(0, 0) is True

test_zona_contiene_punto()
print("test_zona_contiene_punto: OK")


def test_zona_ordena_coordenadas():
    zona = Zona(2, "Este", 200, 100, 400, 300)

    assert zona.x_min == 100
    assert zona.x_max == 200
    assert zona.y_min == 300
    assert zona.y_max == 400

test_zona_ordena_coordenadas()
print("test_zona_ordena_coordenadas: OK")


def test_zona_metodos_auxiliares():
    zona = Zona(3, "Centro", 50, 80, 60, 90, poblada=False)

    assert zona.es_poblada() is False
    assert zona.obtener_datos() == {
        "id_zona": 3,
        "nombre": "Centro",
        "x_min": 50,
        "x_max": 80,
        "y_min": 60,
        "y_max": 90,
        "poblada": False,
    }
    assert (75, 75) in zona
    assert (10, 10) not in zona

test_zona_metodos_auxiliares()
print("test_zona_metodos_auxiliares: OK")


def test_zona_validacion_errores():
    try:
        Zona(object(), "Zona", 0, 10, 0, 10)
        assert False
    except TypeError:
        pass

    try:
        Zona(4, "   ", 0, 10, 0, 10)
        assert False
    except ValueError:
        pass

    try:
        Zona(5, "Fuera", "error", 10, 0, 10)
        assert False
    except TypeError:
        pass

    try:
        Zona(6, "Fuera", 0, 10, 0, 1101)
        assert False
    except ValueError:
        pass

    try:
        Zona(7, "Fuera", 10, 0, 0, 10)
        assert False
    except Exception:
        pass

test_zona_validacion_errores()
print("test_zona_validacion_errores: OK")
