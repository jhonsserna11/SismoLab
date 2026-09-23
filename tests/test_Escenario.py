from datetime import datetime, timezone

from src.logic.Escenario import Escenario


def test_crear_y_consultar_evento():
    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["status"] == "activo"
    assert resultado["magnitud"] == 5.0
    assert resultado["profundidad"] == 20.0
    assert resultado["zonax"] == 100.0
    assert resultado["zonay"] == 100.0
    assert resultado["revision"] == 1
    assert resultado["estaciones"] == ["EST-01"]
    assert resultado["poblada"] is True
    assert resultado["prioridad"] == 3
    assert resultado["estado"] == "Pendiente"
test_crear_y_consultar_evento()
print("test crear y consultar evento: OK")

""" Id tests -------------------------------------------------------"""
def test_id_duplicado():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    escenario.crearEvento(
        1,
        6.0,
        10.0,
        200.0,
        200.0,
        fecha,
        "EST-02"
    )

    assert escenario.avl.peso() == 1

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == 5.0
    assert nodo.evento.estaciones == ["EST-01"]
test_id_duplicado()
print("test id duplicado: OK")

def test_id_no_entero():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        "1",
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
    assert escenario.historico == []
    assert escenario.eliminados == set()
test_id_no_entero()
print("test id no entero: OK")

def test_id_menor_que_uno():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        0,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_id_menor_que_uno()
print("test id menor que uno: OK")

def test_id_mayor_que_limite():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1000000,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_id_mayor_que_limite()
print("test id mayor que limite: OK")

def test_id_limites_validos():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    escenario.crearEvento(
        999999,
        5.0,
        20.0,
        200.0,
        200.0,
        fecha,
        "EST-02"
    )

    assert escenario.avl.peso() == 2
    assert escenario.avl.encontrarNodo(1) is not None
    assert escenario.avl.encontrarNodo(999999) is not None
test_id_limites_validos()
print("test id limites validos: OK")


""" Magnitud tests --------------------------------------------------"""
def test_magnitud_minima():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        -2.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == -2.0
    assert nodo.key.prioridad == 1
test_magnitud_minima()
print("test magnitud minima: OK")
def test_magnitud_maxima():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        10.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == 10.0
    assert nodo.key.prioridad == 3
test_magnitud_maxima()
print("test magnitud maxima: OK")

def test_magnitud_fuera_de_rango_inferior():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        -2.1,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_magnitud_fuera_de_rango_inferior()
print("test magnitud fuera de rango inferior: OK")

def test_magnitud_fuera_de_rango_superior():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        10.1,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_magnitud_fuera_de_rango_superior()
print("test magnitud fuera de rango superior: OK")

def test_magnitud_mas_de_un_decimal():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.25,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_magnitud_mas_de_un_decimal()
print("test magnitud mas de un decimal: OK")


""" Profundidad tests ----------------------------------------------- """
def test_profundidad_minima():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        0.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.profundidad == 0.0
test_profundidad_minima()
print("test profundidad minima: OK")

def test_profundidad_maxima():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        700.0,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.profundidad == 700.0
test_profundidad_maxima()
print("test profundidad maxima: OK")

def test_profundidad_fuera_de_rango_inferior():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        -0.1,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_profundidad_fuera_de_rango_inferior()
print("test profundidad fuera de rango inferior: OK")

def test_profundidad_fuera_de_rango_superior():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        700.1,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_profundidad_fuera_de_rango_superior()
print("test profundidad fuera de rango superior: OK")

def test_profundidad_mas_de_un_decimal():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.25,
        100.0,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_profundidad_mas_de_un_decimal()
print("test profundidad mas de un decimal: OK")


""" Epicentro coordenadas tests ------------------------------------- """
def test_coordenadas_minimas():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        0.0,
        0.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.zonax == 0.0
    assert nodo.evento.zonay == 0.0
test_coordenadas_minimas()
print("test coordenadas minimas: OK")

def test_coordenadas_maximas():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        1000.0,
        1000.0,
        fecha,
        "EST-01"
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.zonax == 1000.0
    assert nodo.evento.zonay == 1000.0
test_coordenadas_maximas()
print("test coordenadas maximas: OK")

def test_zonax_fuera_de_rango():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        -0.1,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_zonax_fuera_de_rango()
print("test zonax fuera de rango: OK")

def test_zonay_fuera_de_rango():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        1000.1,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_zonay_fuera_de_rango()
print("test zonay fuera de rango: OK")

def test_coordenada_mas_de_un_decimal():

    escenario = Escenario()

    fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.25,
        100.0,
        fecha,
        "EST-01"
    )

    assert escenario.avl.peso() == 0
test_coordenada_mas_de_un_decimal()
print("test coordenada mas de un decimal: OK")


""" prioridades """
def test_prioridad_menor_a_4_5():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        4.4,
        100.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 1
test_prioridad_menor_a_4_5()
print("test prioridad_menor_a_4_5: OK")

def test_prioridad_4_5_con_profundidad_mayor_a_30():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        4.5,
        30.1,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 2
test_prioridad_4_5_con_profundidad_mayor_a_30()
print("test prioridad_4_5_con_profundidad_mayor_a_30: OK")

def test_prioridad_4_5_con_profundidad_30():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        4.5,
        30.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_4_5_con_profundidad_30()
print("test prioridad_4_5_con_profundidad_30: OK")

def test_prioridad_mayor_a_4_5_con_profundidad_mayor_a_30():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        5.0,
        30.1,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 2
test_prioridad_mayor_a_4_5_con_profundidad_mayor_a_30()
print("test test_prioridad_mayor_a_4_5_con_profundidad_mayor_a_30: OK")

def test_prioridad_mayor_a_4_5_con_profundidad_30():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        5.0,
        30.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_mayor_a_4_5_con_profundidad_30()
print("test prioridad_mayor_a_4_5_con_profundidad_30: OK")

def test_prioridad_magnitud_6_siempre_es_3():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        6.0,
        700.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_magnitud_6_siempre_es_3()
print("test prioridad_magnitud_6_siempre_es_3: OK")

def test_prioridad_magnitud_mayor_a_6():
    escenario = Escenario()

    escenario.crearEvento(
        1,
        6.1,
        700.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01"
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_magnitud_mayor_a_6()
print("test prioridad_magnitud_mayor_a_6: OK")