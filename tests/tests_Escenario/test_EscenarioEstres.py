from datetime import datetime, timezone, timedelta

from src.structures.Nodo import Key
from src.domain.Evento import Evento
from src.logic.Escenario import Escenario
from src.domain.Zona import Zona

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

    zonaPoblada = Zona(
        1,
        "Zona poblada",
        0.0,
        500.0,
        0.0,
        500.0,
        True
    )
    zonaNoPoblada = Zona(
            2,
            "Zona no poblada",
            500.1,
            1000.0,
            0.0,
            500.0,
            True
        )

    escenario.zonas.append(zonaPoblada)
    escenario.zonas.append(zonaNoPoblada)

    return escenario

def crear_evento(id_evento=1):
    return Evento(
        id_evento,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 23, 10, 0, 0,
            tzinfo=timezone.utc
        ),
        1,
        ["EST-01"]
    )

def test_insercion_modo_estres_sin_balanceo():
    escenario = crear_escenario()

    eventos = [
        Evento(
            10, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=10),
            1, ["EST-01"]
        ),
        Evento(
            20, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=9),
            1, ["EST-01"]
        ),
        Evento(
            30, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=8),
            1, ["EST-01"]
        )
    ]

    for evento in eventos:
        escenario.avl.insertar(
            Key(1, evento.magnitud, evento.id),
            evento,
            True
        )

    assert escenario.avl.raiz.key.id_key == 10
    assert escenario.avl.raiz.izq is None
    assert escenario.avl.raiz.der.key.id_key == 20
    assert escenario.avl.raiz.der.der.key.id_key == 30

    assert escenario.avl.peso() == 3
    assert escenario.avl.altura() == 2

    assert escenario.avl.raiz.key.id_key == 10
    assert escenario.avl.raiz.der.key.id_key == 20
    assert escenario.avl.raiz.der.der.key.id_key == 30
test_insercion_modo_estres_sin_balanceo()
print("test insercion modo estres sin balanceo: OK")


def test_arbol_desbalanceado_modo_estres():
    escenario = crear_escenario()

    eventos = [
        Evento(
            10, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=10),
            1, ["EST-01"]
        ),
        Evento(
            20, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=9),
            1, ["EST-01"]
        ),
        Evento(
            30, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=8),
            1, ["EST-01"]
        ),
        Evento(
            40, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=7),
            1, ["EST-01"]
        ),
        Evento(
            50, 4.0, 100.0, 100.0, 100.0,
            escenario.reloj - timedelta(hours=6),
            1, ["EST-01"]
        )
    ]

    for evento in eventos:
        escenario.avl.insertar(
            Key(1, evento.magnitud, evento.id),
            evento,
            True
        )

    assert escenario.avl.raiz.key.id_key == 10
    assert escenario.avl.raiz.der.key.id_key == 20
    assert escenario.avl.raiz.der.der.key.id_key == 30
    assert escenario.avl.raiz.der.der.der.key.id_key == 40
    assert escenario.avl.raiz.der.der.der.der.key.id_key == 50

    assert escenario.avl.peso() == 5
    assert escenario.avl.altura() == 4

    assert escenario.avl.obtenerDatosNodo(escenario.avl.raiz)["factor"] == -4
test_arbol_desbalanceado_modo_estres()
print("test arbol desbalanceado modo estres: OK")


def test_arbol_desbalanceado_modo_estres_estructura_compleja():
    escenario = crear_escenario()

    ids = [10, 20, 30, 15, 25, 40, 22, 27, 50]

    for id_evento in ids:
        evento = Evento(
            id_evento,
            4.0,
            100.0,
            100.0,
            100.0,
            escenario.reloj - timedelta(hours=10),
            1,
            ["EST-01"]
        )

        escenario.avl.insertar(
            Key(1, evento.magnitud, evento.id),
            evento,
            True
        )

    assert escenario.avl.raiz.key.id_key == 10

    nodo20 = escenario.avl.raiz.der
    assert nodo20.key.id_key == 20

    assert nodo20.izq.key.id_key == 15
    assert nodo20.der.key.id_key == 30

    nodo30 = nodo20.der
    assert nodo30.izq.key.id_key == 25
    assert nodo30.der.key.id_key == 40

    nodo25 = nodo30.izq
    assert nodo25.izq.key.id_key == 22
    assert nodo25.der.key.id_key == 27

    nodo40 = nodo30.der
    assert nodo40.izq is None
    assert nodo40.der.key.id_key == 50

    assert escenario.avl.peso() == 9
    assert escenario.avl.altura() == 4

    assert escenario.avl.obtenerDatosNodo(escenario.avl.raiz)["factor"] == -4

    assert escenario.avl.obtenerDatosNodo(nodo20)["factor"] == -2

    assert escenario.avl.obtenerDatosNodo(nodo30)["factor"] == 0

    assert escenario.avl.obtenerDatosNodo(nodo40)["factor"] == -1
test_arbol_desbalanceado_modo_estres_estructura_compleja()
print("test arbol desbalanceado modo estres estructura compleja: OK")
