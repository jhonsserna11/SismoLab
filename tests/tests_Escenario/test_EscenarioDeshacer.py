from datetime import datetime, timezone

from src.logic.Escenario import Escenario
from src.domain.Zona import Zona

from src.structures.Nodo import Key

def crear_escenario():
    reloj = datetime(
        2026, 9, 23, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        48,
        40,
        3,
        72,
        reloj
    )

    return escenario

def crear_escenario_con_zonas():
    escenario = crear_escenario()

    zona1 = Zona(
        1,
        "Zona poblada",
        0.0,
        500.0,
        0.0,
        500.0,
        True
    )
    zona2 = Zona(
            2,
            "Zona poblada",
            501.0,
            1000.0,
            501.0,
            1000.0,
            True
        )
    zona3 = Zona(
            3,
            "Zona no poblada",
            0.0,
            500.0,
            501.0,
            1000.0,
            True
        )
    zona4 = Zona(
            4,
            "Zona no poblada",
            501.0,
            1000.0,
            0.0,
            500.0,
            True
        )

    for zona in [zona1, zona2, zona3, zona4]: escenario.zonas.append(zona) 

    return escenario

def test_deshacer_CrearEvento():
    print("-------------------------- test_deshacer_CrearEvento --------------------------\n")
    escenario = crear_escenario_con_zonas()

    assert escenario.avl.raiz is None

    escenario.crearEvento(1, 5.0, 200.0, 100.0, 300.0, datetime(2026, 10, 1, 10, 0, 0, tzinfo=timezone.utc), ["EST-2"])

    assert escenario.avl.raiz is not None
    assert escenario.avl.raiz.evento.id == 1

    print(f"pila: {escenario.pila_deshacer}")
    escenario.deshacer()
    print(f"pila despues de deshacer: {escenario.pila_deshacer}")
    print(escenario.avl.raiz)
    assert escenario.avl.raiz == None
test_deshacer_CrearEvento()
print("test deshacer_CrearEvento: OK\n\n")


def test_deshacer_correccion():
    print("-------------------------- test_deshacer_correccion --------------------------\n")
    escenario = crear_escenario_con_zonas()

    escenario.crearEvento(1, 5.0, 200.0, 100.0, 300.0, datetime(2026, 10, 1, 10, 0, 0, tzinfo=timezone.utc), ["EST-2"])
    escenario.crearEvento(2, 7.0, 100.0, 700.0, 500.0, datetime(2026, 11, 1, 4, 0, 10, tzinfo=timezone.utc), ["EST-1", "EST-2"])
    escenario.crearEvento(3, 2.0, 500.0, 900.3, 308.4, datetime(2026, 10, 2, 5, 20, 38, tzinfo=timezone.utc), ["EST-2"])

    print(F"raiz inicial: {escenario.avl.raiz.evento.id}")
    print(f"izq inicial: {escenario.avl.raiz.izq.evento.id}")
    print(f"der inicial: {escenario.avl.raiz.der.evento.id}\n")

    assert escenario.avl.raiz.evento.id == 1
    assert escenario.avl.raiz.izq.evento.id == 3
    assert escenario.avl.raiz.der.evento.id == 2

    print("ejecutar correccion")
    escenario.corregirEvento(2, 3.0)

    print(f"raiz post correccion: {escenario.avl.raiz.evento.id}")
    print(f"izq post correccion: {escenario.avl.raiz.izq.evento.id}")
    print(f"der post correccion: {escenario.avl.raiz.der.evento.id}\n")

    assert escenario.avl.raiz.evento.id == 2
    assert escenario.avl.raiz.izq.evento.id == 3
    assert escenario.avl.raiz.der.evento.id == 1

    print("ejecutar deshacer")
    escenario.deshacer()

    print(f"raiz al deshacer: {escenario.avl.raiz.evento.id}")
    print(f"izq al deshacer: {escenario.avl.raiz.izq.evento.id}")
    print(f"der al deshacer: {escenario.avl.raiz.der.evento.id}\n")
    assert escenario.avl.raiz.evento.id == 1
    assert escenario.avl.raiz.izq.evento.id == 3
    assert escenario.avl.raiz.der.evento.id == 2
test_deshacer_correccion()
print("test deshacer_correccion: OK\n\n")


def test_deshacer_eliminar():
    print("-------------------------- test_deshacer_correccion --------------------------\n")
    escenario = crear_escenario_con_zonas()
    escenario.crearEvento(1, 5.0, 200.0, 100.0, 300.0, datetime(2026, 10, 1, 10, 0, 0, tzinfo=timezone.utc), ["EST-2"])
    escenario.crearEvento(2, 7.0, 100.0, 700.0, 500.0, datetime(2026, 11, 1, 4, 0, 10, tzinfo=timezone.utc), ["EST-1", "EST-2"])
    escenario.crearEvento(3, 2.0, 500.0, 900.3, 308.4, datetime(2026, 10, 2, 5, 20, 38, tzinfo=timezone.utc), ["EST-2"])

    print(escenario.avl.raiz.izq.key)
    key = Key(1, 2.0, 3)

    print("ejecutar eliminación")
    escenario.eliminacionIndividual(key)

    assert escenario.avl.raiz.evento.id == 1
    assert escenario.avl.raiz.izq is None
    assert escenario.avl.raiz.der.evento.id == 2
    assert escenario.eliminados == {3}

    escenario.deshacer()

    assert escenario.avl.raiz.evento.id == 1
    assert escenario.avl.raiz.izq.evento.id == 3
    assert escenario.avl.raiz.der.evento.id == 2
    assert escenario.eliminados == set()
test_deshacer_eliminar()
print("test test_deshacer_eliminar: OK\n\n")