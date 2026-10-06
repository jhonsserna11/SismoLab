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


# ================================================================
# CREATE AND QUERY
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


def test_auditoria_escenario_valida_asociacion_y_detecta_prioridad():
    escenario = crear_escenario()
    anterior = Evento(
        1, 6.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 23, 10, 0, tzinfo=timezone.utc),
        1, ["EST-01"]
    )
    posterior = Evento(
        2, 5.0, 20.0, 100.0, 100.0,
        datetime(2026, 9, 23, 11, 0, tzinfo=timezone.utc),
        1, ["EST-02"]
    )
    escenario._crearEvento(anterior)
    escenario._crearEvento(posterior)

    reporte = escenario.verificarEstructura()
    assert reporte["valido"]
    assert escenario._obtenerAsociaciones(posterior)["asociado"] is anterior

    escenario.avl.encontrarNodo(2).key.prioridad = 3
    reporte = escenario.verificarEstructura()
    assert not reporte["valido"]
    assert any(
        "prioridad de la clave no coincide" in error
        for evento in reporte["eventos_inconsistentes"]
        for error in evento["errores"]
    )

    escenario.historico.append(crear_evento(1))
    reporte = escenario.verificarEstructura()
    assert any(
        "Identificador duplicado entre activos e histórico" in error
        for evento in reporte["eventos_inconsistentes"]
        for error in evento["errores"]
    )
test_auditoria_escenario_valida_asociacion_y_detecta_prioridad()
print("test auditoria escenario: OK")


# ================================================================
# IDENTIFIER TESTS
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
# MAGNITUDE TESTS
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
# DEPTH TESTS
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
# EPICENTER
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
# PRIORITIES
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
# REVIEW STATUS
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

def test_eventos_por_prioridad():
    escenario = crear_escenario()

    escenario.crearEvento(
        1, 3.5, 50.0, 10.0, 10.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        ["EST-01"]
    )

    escenario.crearEvento(
        2, 5.0, 50.0, 20.0, 20.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        ["EST-02"]
    )

    escenario.crearEvento(
        3, 6.5, 100.0, 30.0, 30.0,
        datetime(2026, 9, 22, 14, 0, 0, tzinfo=timezone.utc),
        ["EST-03"]
    )

    escenario.crearEvento(
        4, 7.0, 20.0, 40.0, 40.0,
        datetime(2026, 9, 22, 15, 0, 0, tzinfo=timezone.utc),
        ["EST-04"]
    )

    resultado = escenario._indicadorEventosPorPrioridad()

    assert resultado[1]["cantidad"] == 1
    assert resultado[2]["cantidad"] == 1
    assert resultado[3]["cantidad"] == 2

    assert len(resultado[1]["eventos"]) == 1
    assert len(resultado[2]["eventos"]) == 1
    assert len(resultado[3]["eventos"]) == 2

    assert [evento["id"] for evento in resultado[1]["eventos"]] == [1]
    assert [evento["id"] for evento in resultado[2]["eventos"]] == [2]
    assert [evento["id"] for evento in resultado[3]["eventos"]] == [3, 4]
test_eventos_por_prioridad()
print("test eventos_por_prioridad: OK")


def test_eventos_pendientes():
    escenario = crear_escenario()

    escenario.crearEvento(
        1, 3.5, 50.0, 10.0, 10.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        ["EST-01"]
    )

    escenario.crearEvento(
        2, 5.0, 50.0, 20.0, 20.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        ["EST-02"]
    )

    escenario.crearEvento(
        3, 6.5, 100.0, 30.0, 30.0,
        datetime(2026, 9, 22, 14, 0, 0, tzinfo=timezone.utc),
        ["EST-03"]
    )

    escenario.crearEvento(
        4, 7.0, 20.0, 40.0, 40.0,
        datetime(2026, 9, 22, 15, 0, 0, tzinfo=timezone.utc),
        ["EST-04"]
    )

    escenario.marcarRevisado(2)

    resultado = escenario._indicadorEventosPendientes()

    assert resultado["cantidad"] == 3
    assert [evento["id"] for evento in resultado["eventos"]] == [1, 3, 4]
test_eventos_pendientes()
print("test eventos_pendientes: OK")

# ================================================================
# AVL - BST SYNCHRONIZATION
# ================================================================

def test_bst_se_sincroniza_con_creacion():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    escenario.crearEvento(
        2,
        4.0,
        30.0,
        200.0,
        200.0,
        datetime(
            2026, 9, 22, 13, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-02"]
    )

    escenario.crearEvento(
        3,
        6.0,
        10.0,
        300.0,
        300.0,
        datetime(
            2026, 9, 22, 14, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-03"]
    )

    assert escenario.avl.peso() == 3
    assert escenario.bst.cantidad_nodos() == 3
test_bst_se_sincroniza_con_creacion()
print("test bst se sincroniza con creacion: OK")


def test_bst_se_sincroniza_correccion_sin_cambio_key():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    nodo_avl = escenario.avl.encontrarNodo(1)
    key_original = nodo_avl.key

    escenario.corregirEvento(
        1,
        profundidad=25.0
    )

    nodo_avl = escenario.avl.encontrarNodo(1)
    nodo_bst = escenario.bst.buscar(key_original)

    assert nodo_avl is not None
    assert nodo_bst is not None

    assert nodo_avl.key == key_original
    assert nodo_bst.key == key_original

    assert nodo_avl.evento.profundidad == 25.0
    assert nodo_bst.evento.profundidad == 25.0

    assert escenario.avl.peso() == 1
    assert escenario.bst.cantidad_nodos() == 1
test_bst_se_sincroniza_correccion_sin_cambio_key()
print("test bst se sincroniza correccion sin cambio key: OK")


def test_bst_se_sincroniza_correccion_con_cambio_key():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    escenario.crearEvento(
        2,
        4.0,
        30.0,
        200.0,
        200.0,
        datetime(
            2026, 9, 22, 13, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-02"]
    )

    nodo_original = escenario.avl.encontrarNodo(1)
    key_original = nodo_original.key

    escenario.corregirEvento(
        1,
        magnitud=7.0
    )

    nodo_avl = escenario.avl.encontrarNodo(1)

    assert nodo_avl is not None

    nueva_key = nodo_avl.key

    assert nueva_key != key_original

    assert escenario.bst.buscar(key_original) is None

    nodo_bst = escenario.bst.buscar(nueva_key)

    assert nodo_bst is not None
    assert nodo_bst.evento.id == 1
    assert nodo_bst.evento.magnitud == 7.0

    assert escenario.avl.peso() == 2
    assert escenario.bst.cantidad_nodos() == 2
test_bst_se_sincroniza_correccion_con_cambio_key()
print("test bst se sincroniza correccion con cambio key: OK")


def test_bst_se_sincroniza_con_eliminacion():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    escenario.crearEvento(
        2,
        4.0,
        30.0,
        200.0,
        200.0,
        datetime(
            2026, 9, 22, 13, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-02"]
    )

    escenario.crearEvento(
        3,
        6.0,
        10.0,
        300.0,
        300.0,
        datetime(
            2026, 9, 22, 14, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-03"]
    )

    nodo = escenario.avl.encontrarNodo(2)
    key = nodo.key

    escenario.eliminacionIndividual(key)

    assert escenario.avl.encontrarNodo(2) is None
    assert escenario.bst.buscar(key) is None

    assert escenario.avl.peso() == 2
    assert escenario.bst.cantidad_nodos() == 2
test_bst_se_sincroniza_con_eliminacion()
print("test bst se sincroniza con eliminacion: OK")


def test_undo_restaura_avl_y_bst():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    escenario.crearEvento(
        2,
        4.0,
        30.0,
        200.0,
        200.0,
        datetime(
            2026, 9, 22, 13, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-02"]
    )

    escenario.crearEvento(
        3,
        6.0,
        10.0,
        300.0,
        300.0,
        datetime(
            2026, 9, 22, 14, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-03"]
    )

    nodo = escenario.avl.encontrarNodo(2)
    key = nodo.key

    escenario.eliminacionIndividual(key)

    assert escenario.avl.peso() == 2
    assert escenario.bst.cantidad_nodos() == 2

    escenario.deshacer()

    assert escenario.avl.peso() == 3
    assert escenario.bst.cantidad_nodos() == 3

    assert escenario.avl.encontrarNodo(2) is not None
    assert escenario.bst.buscar(key) is not None
test_undo_restaura_avl_y_bst()
print("test undo restaura avl y bst: OK")


def test_bst_se_sincroniza_con_reporte_mayor_revision():

    escenario = crear_escenario()

    escenario.crearEvento(
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(
            2026, 9, 22, 12, 0, 0,
            tzinfo=timezone.utc
        ),
        ["EST-01"]
    )

    class Reporte:
        pass

    reporte = Reporte()
    reporte.id_evento = 1
    reporte.magnitud = 7.0
    reporte.profundidad = 25.0
    reporte.zonax = 100.0
    reporte.zonay = 100.0
    reporte.fecha = datetime(
        2026, 9, 22, 12, 0, 0,
        tzinfo=timezone.utc
    )
    reporte.nRevision = 2
    reporte.estacion = "EST-02"

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "actualizado"

    nodo_avl = escenario.avl.encontrarNodo(1)

    assert nodo_avl is not None

    nodo_bst = escenario.bst.buscar(nodo_avl.key)

    assert nodo_bst is not None

    assert nodo_avl.evento.magnitud == 7.0
    assert nodo_bst.evento.magnitud == 7.0

    assert nodo_avl.evento.revision == 2
    assert nodo_bst.evento.revision == 2

    assert escenario.avl.peso() == 1
    assert escenario.bst.cantidad_nodos() == 1
test_bst_se_sincroniza_con_reporte_mayor_revision()
print("test bst se sincroniza con reporte mayor revision: OK")