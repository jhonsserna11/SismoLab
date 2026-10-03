import json
from datetime import datetime, timezone
from decimal import Decimal

from src.logic.Escenario import Escenario
from src.domain.Zona import Zona
from src.domain.Estacion import Estacion


def crear_estado_inicial():

    reloj = datetime(
        2026, 10, 1, 10, 0, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        w=48,
        r=40,
        l=3,
        t=72,
        reloj=reloj
    )

    # Zonas
    zonas = [
        Zona(1, "Zona poblada 1", 0.0, 500.0, 0.0, 500.0, True),
        Zona(2, "Zona poblada 2", 501.0, 1000.0, 501.0, 1000.0, True),
        Zona(3, "Zona no poblada 1", 0.0, 500.0, 501.0, 1000.0, False),
        Zona(4, "Zona no poblada 2", 501.0, 1000.0, 0.0, 500.0, False),
    ]

    escenario.zonas.extend(zonas)

    # Estaciones
    estaciones = [
        Estacion("EST-1", "Manizales"),
        Estacion("EST-2", "Medellín"),
        Estacion("EST-3", "Bogotá"),
        Estacion("EST-4", "Armenia"),
    ]

    escenario.estaciones.extend(estaciones)

    # Eventos iniciales
    escenario.crearEvento(
        100,
        Decimal("5.0"),
        Decimal("20.0"),
        Decimal("100.0"),
        Decimal("100.0"),
        datetime(2026, 10, 1, 9, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )

    escenario.crearEvento(
        200,
        Decimal("6.0"),
        Decimal("30.0"),
        Decimal("600.0"),
        Decimal("600.0"),
        datetime(2026, 10, 1, 9, 10, 0, tzinfo=timezone.utc),
        ["EST-2"]
    )

    escenario.crearEvento(
        300,
        Decimal("4.0"),
        Decimal("50.0"),
        Decimal("200.0"),
        Decimal("700.0"),
        datetime(2026, 10, 1, 9, 20, 0, tzinfo=timezone.utc),
        ["EST-3"]
    )

    return escenario


if __name__ == "__main__":
    from pathlib import Path

    escenario = crear_estado_inicial()

    assert escenario.avl.peso() == 3, (
        f"Se esperaban 3 eventos en el AVL, pero hay {escenario.avl.peso()}"
    )

    assert escenario.bst.cantidad_nodos() == 3, (
        f"Se esperaban 3 eventos en el BST, pero hay {escenario.bst.cantidad_nodos()}"
    )

    datos = escenario.guardarEscenario()

    ruta = Path(__file__).resolve().parent.parent / "data" / "estado_inicial.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print("Estado inicial creado correctamente.")
    print(f"Eventos AVL: {escenario.avl.peso()}")
    print(f"Eventos BST: {escenario.bst.cantidad_nodos()}")
    print(f"Raíz AVL: {datos['avl']['raiz']}")
    print(f"Raíz BST: {datos['bst']['raiz']}")
    print(f"Estado inicial guardado en: {ruta}")