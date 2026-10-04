from datetime import datetime, timezone, timedelta

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

def crear_escenario_con_zona_poblada():
    escenario = crear_escenario()

    zona = Zona(
        1,
        "Zona poblada",
        0.0,
        500.0,
        0.0,
        500.0,
        True
    )

    escenario.zonas.append(zona)

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


def test_obtener_rama_archivable_arbol_completo():
    escenario = crear_escenario()

    evento1 = Evento(
        1, 4.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 20, 10, 0, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    evento2 = Evento(
        2, 3.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 20, 11, 0, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    evento3 = Evento(
        3, 2.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 20, 9, 0, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    escenario._crearEvento(evento1)
    escenario._crearEvento(evento2)
    escenario._crearEvento(evento3)

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["elegible"] is True
    assert resultado["cantidad"] == 3
    assert resultado["mejor"] is not None
    assert resultado["mejor"]["cantidad"] == 3
    assert resultado["mejor"]["nodo"] is escenario.avl.raiz
test_obtener_rama_archivable_arbol_completo()
print("test obtener_rama_archivable_arbol_completo: OK")

def test_obtener_rama_archivable_raiz_no_elegible():
    escenario = crear_escenario()

    evento1 = Evento(
        1, 4.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    evento2 = Evento(
        2, 3.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 20, 11, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    evento3 = Evento(
        3, 5.0, 100.0, 100.0, 100.0,
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )

    escenario._crearEvento(evento1)
    escenario._crearEvento(evento2)
    escenario._crearEvento(evento3)

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["elegible"] is False
    assert resultado["mejor"] is not None
    assert resultado["mejor"]["nodo"].key.id_key == 2
    assert resultado["mejor"]["cantidad"] == 1
test_obtener_rama_archivable_raiz_no_elegible()
print("test obtener_rama_archivable_raiz_no_elegible: OK")

def test_obtener_rama_archivable_arbol_10_eventos():
    escenario = crear_escenario()

    # Eligibility requires age strictly greater than T (72 hours).
    # Events 5-7 are 74 hours old; the others are exactly 72 hours old.

    fechas = [
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
    ]

    for i in range(1, 11):
        evento = Evento(
            i,
            3.0,
            20.0,
            100.0,
            100.0,
            fechas[i - 1],
            1,
            ["EST-01"]
        )

        escenario._crearEvento(evento)

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["elegible"] is False
    assert resultado["mejor"] is not None
    assert resultado["mejor"]["nodo"].key.id_key == 6
    assert resultado["mejor"]["cantidad"] == 3
test_obtener_rama_archivable_arbol_10_eventos()
print("test obtener_rama_archivable_arbol_10_eventos: OK")

def test_obtener_rama_archivable_multiples_candidatos():
    escenario = crear_escenario()

    # Equal magnitudes and depths make IDs determine key order; only dates affect eligibility.

    fecha_no_elegible = datetime(
        2026, 9, 20, 12, 0, tzinfo=timezone.utc
    )

    fecha_elegible = datetime(
        2026, 9, 20, 10, 0, tzinfo=timezone.utc
    )

    fechas = {
        1: fecha_no_elegible,
        2: fecha_no_elegible,
        3: fecha_no_elegible,
        4: fecha_no_elegible,

        5: fecha_elegible,
        6: fecha_elegible,
        7: fecha_elegible,

        8: fecha_no_elegible,

        9: fecha_elegible,
        10: fecha_elegible,
        11: fecha_elegible,

        12: fecha_no_elegible,

        13: fecha_elegible,
        14: fecha_elegible,
        15: fecha_elegible,
    }

    for i in range(1, 16):
        evento = Evento(
            i,
            3.0,
            20.0,
            100.0,
            100.0,
            fechas[i],
            1,
            ["EST-01"]
        )

        escenario._crearEvento(evento)

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["elegible"] is False
    assert resultado["mejor"] is not None

    # Equal-size, equal-depth candidates are resolved by the greatest root ID.

    assert resultado["mejor"]["cantidad"] == 3
    assert resultado["mejor"]["nodo"].key.id_key == 14
test_obtener_rama_archivable_multiples_candidatos()
print("test obtener_rama_archivable_multiples_candidatos: OK")

def test_archivar_rama():
    reloj = datetime(2026, 9, 26, 12, 0, 0, tzinfo=timezone.utc)
    escenario = Escenario(48, 40, 3, 72, reloj)

    fecha = reloj - timedelta(hours=100)

    escenario.crearEvento(
        2, 4.0, 100.0, 100.0, 100.0,
        fecha, ["EST-01"]
    )

    escenario.crearEvento(
        1, 4.0, 100.0, 200.0, 200.0,
        fecha, ["EST-01"]
    )

    escenario.crearEvento(
        3, 4.0, 100.0, 300.0, 300.0,
        fecha, ["EST-01"]
    )

    claves = {
        1: escenario.avl.encontrarNodo(1).key,
        2: escenario.avl.encontrarNodo(2).key,
        3: escenario.avl.encontrarNodo(3).key,
    }

    resultado = escenario.obtenerRamaArchivable()
    nodo_raiz = resultado["mejor"]["nodo"]

    escenario.archivarRama(nodo_raiz)

    assert {evento.id for evento in escenario.historico} == {1, 2, 3}

    assert escenario.avl.encontrarNodo(1) is None
    assert escenario.avl.encontrarNodo(2) is None
    assert escenario.avl.encontrarNodo(3) is None

    assert escenario.bst.buscar(claves[1]) is None
    assert escenario.bst.buscar(claves[2]) is None
    assert escenario.bst.buscar(claves[3]) is None
test_archivar_rama()
print("test archivar_rama: OK")


def test_no_hay_rama_archivable():
    reloj = datetime(2026, 9, 26, 12, 0, 0, tzinfo=timezone.utc)
    escenario = Escenario(48, 40, 3, 72, reloj)

    fecha = reloj - timedelta(hours=100)

    escenario.crearEvento(
        1, 5.0, 100.0, 100.0, 100.0,
        fecha, ["EST-01"]
    )

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["mejor"] is None
test_no_hay_rama_archivable()
print("test no_hay_rama_archivable: OK")

def test_no_archiva_eventos_si_no_hay_rama_elegible():
    reloj = datetime(2026, 9, 26, 12, 0, 0, tzinfo=timezone.utc)
    escenario = Escenario(48, 40, 3, 72, reloj)

    fecha = reloj - timedelta(hours=100)

    escenario.crearEvento(
        1, 5.0, 100.0, 100.0, 100.0,
        fecha, ["EST-01"]
    )

    escenario.crearEvento(
        2, 6.0, 100.0, 200.0, 200.0,
        fecha, ["EST-01"]
    )

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["mejor"] is None
    assert escenario.historico == []
test_no_archiva_eventos_si_no_hay_rama_elegible()
print("test no_archiva_eventos_si_no_hay_rama_elegible: OK")

def test_archivar_subarbol_con_reorganizacion():
    escenario = crear_escenario()

    reloj = escenario.reloj
    fecha_elegible = reloj - timedelta(hours=100)
    fecha_no_elegible = reloj - timedelta(hours=72)

    ids = [8, 4, 12, 2, 6, 14]

    for id_evento in ids:
        if id_evento in [2, 4, 6]:
            fecha = fecha_elegible
        else:
            fecha = fecha_no_elegible

        evento = Evento(
            id_evento,
            4.0,
            100.0,
            100.0,
            100.0,
            fecha,
            1,
            ["EST-01"]
        )

        escenario._crearEvento(evento)

    assert escenario.avl.raiz.key.id_key == 8
    assert escenario.avl.raiz.izq.key.id_key == 4
    assert escenario.avl.raiz.der.key.id_key == 12
    assert escenario.avl.raiz.izq.izq.key.id_key == 2
    assert escenario.avl.raiz.izq.der.key.id_key == 6
    assert escenario.avl.raiz.der.der.key.id_key == 14

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["mejor"] is not None
    assert resultado["mejor"]["nodo"].key.id_key == 4
    assert resultado["mejor"]["cantidad"] == 3

    claves = {
        id_evento: escenario.avl.encontrarNodo(id_evento).key
        for id_evento in [2, 4, 6, 8, 12, 14]
    }
    rama = resultado["mejor"]["nodo"]

    escenario.archivarRama(rama)

    ids_historico = sorted(
        evento.id for evento in escenario.historico
    )

    assert ids_historico == [2, 4, 6]

    # Events outside the selected subtree must remain active.
    assert escenario.avl.encontrarNodo(8) is not None
    assert escenario.avl.encontrarNodo(12) is not None
    assert escenario.avl.encontrarNodo(14) is not None

    assert escenario.avl.encontrarNodo(2) is None
    assert escenario.avl.encontrarNodo(4) is None
    assert escenario.avl.encontrarNodo(6) is None

    assert escenario.bst.buscar(claves[2]) is None
    assert escenario.bst.buscar(claves[4]) is None
    assert escenario.bst.buscar(claves[6]) is None

    assert escenario.bst.buscar(claves[8]) is not None
    assert escenario.bst.buscar(claves[12]) is not None
    assert escenario.bst.buscar(claves[14]) is not None

    assert escenario.bst.cantidad_nodos() == 3
test_archivar_subarbol_con_reorganizacion()
print("test archivar_rama_con_reorganizacion: OK")

def test_archivar_subarbol_con_reorganizacion_():
    escenario = crear_escenario()

    reloj = escenario.reloj
    fecha_elegible = reloj - timedelta(hours=100)
    fecha_no_elegible = reloj - timedelta(hours=72)

    ids = [8, 4, 12, 2, 6, 14]

    for id_evento in ids:
        if id_evento in [2, 4, 6]:
            fecha = fecha_elegible
        else:
            fecha = fecha_no_elegible

        evento = Evento(
            id_evento,
            4.0,
            100.0,
            100.0,
            100.0,
            fecha,
            1,
            ["EST-01"]
        )

        escenario._crearEvento(evento)

    assert escenario.avl.raiz.key.id_key == 8
    assert escenario.avl.raiz.izq.key.id_key == 4
    assert escenario.avl.raiz.der.key.id_key == 12
    assert escenario.avl.raiz.izq.izq.key.id_key == 2
    assert escenario.avl.raiz.izq.der.key.id_key == 6
    assert escenario.avl.raiz.der.der.key.id_key == 14

    resultado = escenario.obtenerRamaArchivable()

    assert resultado["mejor"] is not None
    assert resultado["mejor"]["nodo"].key.id_key == 4
    assert resultado["mejor"]["cantidad"] == 3

    rama = resultado["mejor"]["nodo"]

    escenario.archivarRama(rama)

    ids_historico = sorted(
        evento.id for evento in escenario.historico
    )

    assert ids_historico == [2, 4, 6]

    assert escenario.avl.encontrarNodo(2) is None
    assert escenario.avl.encontrarNodo(4) is None
    assert escenario.avl.encontrarNodo(6) is None

    assert escenario.avl.encontrarNodo(8) is not None
    assert escenario.avl.encontrarNodo(12) is not None
    assert escenario.avl.encontrarNodo(14) is not None


test_archivar_subarbol_con_reorganizacion_()
print("test archivar_subarbol_con_reorganizacion_: OK")
