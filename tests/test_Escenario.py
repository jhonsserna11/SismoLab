from datetime import datetime, timezone

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


# ================================================================
# CREAR Y CONSULTAR
# ================================================================

def test_crear_y_consultar_evento():
    escenario = crear_escenario_con_zona_poblada()

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
        ["EST-01"]
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


# ================================================================
# ID TESTS
# ================================================================

def test_id_duplicado():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    escenario.crearEvento(
        1,
        6.0,
        10.0,
        200.0,
        200.0,
        fecha,
        ["EST-02"]
    )

    assert escenario.avl.peso() == 1

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == 5.0
    assert nodo.evento.estaciones == ["EST-01"]
test_id_duplicado()
print("test id duplicado: OK")


def test_id_no_entero():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
    assert escenario.historico == []
    assert escenario.eliminados == set()
test_id_no_entero()
print("test id no entero: OK")


def test_id_menor_que_uno():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_id_menor_que_uno()
print("test id menor que uno: OK")


def test_id_mayor_que_limite():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_id_mayor_que_limite()
print("test id mayor que limite: OK")


def test_id_limites_validos():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    escenario.crearEvento(
        999999,
        5.0,
        20.0,
        200.0,
        200.0,
        fecha,
        ["EST-02"]
    )

    assert escenario.avl.peso() == 2
    assert escenario.avl.encontrarNodo(1) is not None
    assert escenario.avl.encontrarNodo(999999) is not None
test_id_limites_validos()
print("test id limites validos: OK")


# ================================================================
# MAGNITUD TESTS
# ================================================================

def test_magnitud_minima():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == -2.0
    assert nodo.key.prioridad == 1
test_magnitud_minima()
print("test magnitud minima: OK")


def test_magnitud_maxima():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.magnitud == 10.0
    assert nodo.key.prioridad == 3
test_magnitud_maxima()
print("test magnitud maxima: OK")


def test_magnitud_fuera_de_rango_inferior():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_magnitud_fuera_de_rango_inferior()
print("test magnitud fuera de rango inferior: OK")


def test_magnitud_fuera_de_rango_superior():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_magnitud_fuera_de_rango_superior()
print("test magnitud fuera de rango superior: OK")


def test_magnitud_mas_de_un_decimal():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_magnitud_mas_de_un_decimal()
print("test magnitud mas de un decimal: OK")


# ================================================================
# PROFUNDIDAD TESTS
# ================================================================

def test_profundidad_minima():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.profundidad == 0.0
test_profundidad_minima()
print("test profundidad minima: OK")


def test_profundidad_maxima():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.profundidad == 700.0
test_profundidad_maxima()
print("test profundidad maxima: OK")


def test_profundidad_fuera_de_rango_inferior():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_profundidad_fuera_de_rango_inferior()
print("test profundidad fuera de rango inferior: OK")


def test_profundidad_fuera_de_rango_superior():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_profundidad_fuera_de_rango_superior()
print("test profundidad fuera de rango superior: OK")


def test_profundidad_mas_de_un_decimal():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_profundidad_mas_de_un_decimal()
print("test profundidad mas de un decimal: OK")


# ================================================================
# EPICENTRO
# ================================================================

def test_coordenadas_minimas():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.zonax == 0.0
    assert nodo.evento.zonay == 0.0
test_coordenadas_minimas()
print("test coordenadas minimas: OK")


def test_coordenadas_maximas():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.zonax == 1000.0
    assert nodo.evento.zonay == 1000.0
test_coordenadas_maximas()
print("test coordenadas maximas: OK")


def test_zonax_fuera_de_rango():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_zonax_fuera_de_rango()
print("test zonax fuera de rango: OK")


def test_zonay_fuera_de_rango():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_zonay_fuera_de_rango()
print("test zonay fuera de rango: OK")


def test_coordenada_mas_de_un_decimal():
    escenario = crear_escenario()

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
        ["EST-01"]
    )

    assert escenario.avl.peso() == 0
test_coordenada_mas_de_un_decimal()
print("test coordenada mas de un decimal: OK")


# ================================================================
# PRIORIDADES
# ================================================================

def test_prioridad_menor_a_4_5():
    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        4.4,
        100.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 1
test_prioridad_menor_a_4_5()
print("test prioridad_menor_a_4_5: OK")


def test_prioridad_4_5_con_profundidad_mayor_a_30():
    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        4.5,
        30.1,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 2
test_prioridad_4_5_con_profundidad_mayor_a_30()
print("test prioridad_4_5_con_profundidad_mayor_a_30: OK")


def test_prioridad_4_5_con_profundidad_30():
    escenario = crear_escenario_con_zona_poblada()

    escenario.crearEvento(
        1,
        4.5,
        30.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_4_5_con_profundidad_30()
print("test prioridad_4_5_con_profundidad_30: OK")


def test_prioridad_mayor_a_4_5_con_profundidad_mayor_a_30():
    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        30.1,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 2
test_prioridad_mayor_a_4_5_con_profundidad_mayor_a_30()
print("test prioridad_mayor_a_4_5_con_profundidad_mayor_a_30: OK")


def test_prioridad_mayor_a_4_5_con_profundidad_30():
    escenario = crear_escenario_con_zona_poblada()

    escenario.crearEvento(
        1,
        5.0,
        30.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_mayor_a_4_5_con_profundidad_30()
print("test prioridad_mayor_a_4_5_con_profundidad_30: OK")


def test_prioridad_magnitud_6_siempre_es_3():
    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        6.0,
        700.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_magnitud_6_siempre_es_3()
print("test prioridad_magnitud_6_siempre_es_3: OK")


def test_prioridad_magnitud_mayor_a_6():
    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        6.1,
        700.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    resultado = escenario.consultarEvento(1)

    assert resultado["prioridad"] == 3
test_prioridad_magnitud_mayor_a_6()
print("test prioridad_magnitud_mayor_a_6: OK")


# ================================================================
# ESTADO DE ATENCION
# ================================================================

def test_creacion_deja_evento_pendiente():
    escenario = crear_escenario()

    evento = crear_evento(1)

    escenario._crearEvento(evento)

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.estado == "Pendiente"
test_creacion_deja_evento_pendiente()
print("test creacion_deja_evento_pendiente: OK")


def test_marcar_evento_como_revisado():
    escenario = crear_escenario()

    evento = crear_evento(1)

    escenario._crearEvento(evento)

    escenario.marcarRevisado(1)

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.estado == "Revisado"
test_marcar_evento_como_revisado()
print("test marcar_evento_como_revisado: OK")


def test_marcar_revisado_no_cambia_la_clave():
    escenario = crear_escenario()

    evento = crear_evento(1)

    escenario._crearEvento(evento)

    nodo = escenario.avl.encontrarNodo(1)

    clave_antes = nodo.key

    escenario.marcarRevisado(1)

    nodo_despues = escenario.avl.encontrarNodo(1)

    assert nodo_despues is not None
    assert nodo_despues.key == clave_antes
    assert nodo_despues.evento.estado == "Revisado"
test_marcar_revisado_no_cambia_la_clave()
print("test marcar_revisado_no_cambia_la_clave: OK")


def test_marcar_revisado_id_inexistente():
    escenario = crear_escenario()

    try:
        escenario.marcarRevisado(999)
        assert False
    except ValueError:
        assert True
test_marcar_revisado_id_inexistente()
print("test marcar_revisado_id_inexistente: OK")


def test_correccion_devuelve_evento_a_pendiente():
    escenario = crear_escenario()

    evento = crear_evento(1)

    escenario._crearEvento(evento)

    escenario.marcarRevisado(1)

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.estado == "Revisado"

    escenario.corregirEvento(
        1,
        magnitud=5.5
    )

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.estado == "Pendiente"
test_correccion_devuelve_evento_a_pendiente()
print("test correccion_devuelve_evento_a_pendiente: OK")

def test_correccion_invalida_no_modifica_evento():
    escenario = crear_escenario()
    evento = crear_evento(1)

    escenario._crearEvento(evento)
    escenario.marcarRevisado(1)

    nodo = escenario.avl.encontrarNodo(1)

    revision_antes = nodo.evento.revision
    magnitud_antes = nodo.evento.magnitud
    estado_antes = nodo.evento.estado
    key_antes = nodo.key

    try:
        escenario.corregirEvento(1, profundidad=800.0)
        assert False
    except ValueError:
        pass

    nodo = escenario.avl.encontrarNodo(1)

    assert nodo is not None
    assert nodo.evento.revision == revision_antes
    assert nodo.evento.magnitud == magnitud_antes
    assert nodo.evento.estado == estado_antes
    assert nodo.key == key_antes
test_correccion_invalida_no_modifica_evento()
print("test correccion_invalida_no_modifica_evento: OK")


