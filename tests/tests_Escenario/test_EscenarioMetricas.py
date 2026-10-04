from src.structures.Avl import Avl
from src.structures.Nodo import Key

from src.logic.Escenario import Escenario

from src.domain.Reporte import Reporte

from datetime import datetime, timezone

def test_metricas_rotaciones_avl():
    # LL rotation.
    avl = Avl()
    avl.insertar(Key(1, 5, 1), None, False)
    avl.insertar(Key(1, 4, 2), None, False)
    avl.insertar(Key(1, 3, 3), None, False)

    assert avl.metricas["casos_LL"] == 1
    assert avl.metricas["casos_RR"] == 0
    assert avl.metricas["casos_LR"] == 0
    assert avl.metricas["casos_RL"] == 0
    assert avl.metricas["giros_derecha"] == 1
    assert avl.metricas["giros_izquierda"] == 0

    # RR rotation.
    avl = Avl()
    avl.insertar(Key(1, 3, 1), None, False)
    avl.insertar(Key(1, 4, 2), None, False)
    avl.insertar(Key(1, 5, 3), None, False)

    assert avl.metricas["casos_RR"] == 1
    assert avl.metricas["giros_izquierda"] == 1

    # LR rotation.
    avl = Avl()
    avl.insertar(Key(1, 5, 1), None, False)
    avl.insertar(Key(1, 3, 2), None, False)
    avl.insertar(Key(1, 4, 3), None, False)

    assert avl.metricas["casos_LR"] == 1
    assert avl.metricas["giros_izquierda"] == 1
    assert avl.metricas["giros_derecha"] == 1

    # RL rotation.
    avl = Avl()
    avl.insertar(Key(1, 3, 1), None, False)
    avl.insertar(Key(1, 5, 2), None, False)
    avl.insertar(Key(1, 4, 3), None, False)

    assert avl.metricas["casos_RL"] == 1
    assert avl.metricas["giros_derecha"] == 1
    assert avl.metricas["giros_izquierda"] == 1
test_metricas_rotaciones_avl()
print("test metricas_rotaciones_avl: OK")


def test_indicadores_estructura_escenario():
    reloj = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)

    escenario = Escenario(
        w=48,
        r=40,
        l=0,
        t=72,
        reloj=reloj
    )

    fecha = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)

    escenario.crearEvento(
        1, 4.0, 100.0, 0.0, 0.0, fecha, ["EST-01"]
    )

    escenario.crearEvento(
        2, 5.0, 20.0, 0.0, 0.0, fecha, ["EST-02"]
    )

    escenario.crearEvento(
        3, 6.0, 10.0, 0.0, 0.0, fecha, ["EST-03"]
    )

    indicadores = escenario.obtenerIndicadores()

    assert indicadores["eventos_activos"] == 3
    assert indicadores["eventos_historicos"] == 0

    assert indicadores["altura_avl"] >= 0
    assert indicadores["hojas"] >= 1

    assert len(indicadores["inorden"]) == 3
    assert len(indicadores["preorden"]) == 3
    assert len(indicadores["postorden"]) == 3
    assert len(indicadores["anchura"]) == 3

    prioridades = indicadores["eventos_por_prioridad"]

    assert prioridades[1]["cantidad"] == 1
    assert prioridades[2]["cantidad"] == 1
    assert prioridades[3]["cantidad"] == 1

    assert indicadores["eventos_pendientes"]["cantidad"] == 3

test_indicadores_estructura_escenario()
print("test indicadores_estructura_escenario: OK")


def test_metricas_acumulativas():
    reloj = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)

    escenario = Escenario(
        w=48,
        r=40,
        l=3,
        t=72,
        reloj=reloj
    )

    fecha = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)

    escenario.crearEvento(
        1, 4.0, 100.0, 0.0, 0.0, fecha, ["EST-01"]
    )

    # Manual correction.
    escenario.corregirEvento(
        1,
        magnitud=4.2
    )

    assert escenario.metricas["correcciones_aceptadas"] == 1

    # A report with a newer revision is accepted.
    reporte = Reporte(
        id_evento=1,
        magnitud=4.3,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=3,
        estacion="EST-02"
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "actualizado"
    assert escenario.metricas["correcciones_aceptadas"] == 2

    # A report with an older revision is discarded.
    reporte_antiguo = Reporte(
        id_evento=1,
        magnitud=4.3,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=1,
        estacion="EST-03"
    )

    escenario.procesarReporte(reporte_antiguo)

    assert escenario.metricas["reportes_descartados"] == 1

    # A conflicting report has the same revision but different data.

    reporte_conflicto = Reporte(
        id_evento=1,
        magnitud=5.9,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=3,
        estacion="EST-04"
    )

    escenario.procesarReporte(reporte_conflicto)

    assert escenario.metricas["conflictos"] == 1
test_metricas_acumulativas()
print("test metricas_acumulativas: OK")


def test_limite_L_acceso_costoso():
    escenario = Escenario(
        48,
        40,
        2,
        72,
        datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    )

    eventos = [
        (1, 6.0),
        (2, 6.1),
        (3, 6.2),
        (4, 6.3),
        (5, 6.4),
        (6, 6.5),
        (7, 6.6),
        (8, 6.7),
        (9, 6.8),
        (10, 6.9),
        (11, 7.0),
        (12, 7.1),
        (13, 7.2),
        (14, 7.3),
        (15, 7.4),
    ]

    for id_evento, magnitud in eventos:
        escenario.crearEvento(
            id_evento,
            magnitud,
            100.0,
            0.0,
            0.0,
            datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc),
            []
        )

    indicadores = escenario.obtenerIndicadores()

    nodos_profundidad = escenario.avl.nodos_con_profundidad()

    profundidades = {
        nodo.key.id_key: profundidad
        for nodo, profundidad in nodos_profundidad
    }

    assert 2 in profundidades.values()
    assert 3 in profundidades.values()

    costosos = indicadores["eventos_costosos"]

    ids_costosos = {
        evento["id"]
        for evento in costosos["eventos"]
    }

    # The threshold is exclusive: depth equal to L is not costly.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 2:
            assert nodo.key.id_key not in ids_costosos

    # Nodes deeper than L are costly.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 3:
            assert nodo.key.id_key in ids_costosos
test_limite_L_acceso_costoso()
print("test limite_L_acceso_costoso: OK")

def test_consultar_evento_reporta_nodos_avl_examinados():
    escenario = Escenario(
        48,
        40,
        3,
        72,
        datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    )
    fecha = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)

    for id_evento, magnitud in [(1, 4.0), (2, 5.0), (3, 6.0), (4, 4.5)]:
        escenario.crearEvento(
            id_evento,
            magnitud,
            100.0,
            0.0,
            0.0,
            fecha,
            []
        )

    id_raiz = escenario.avl.raiz.evento.id
    resultado = escenario.consultarEvento(id_raiz)

    profundidad, visitas_profundidad = escenario.avl.nivel_de_un_nodoConConteo(
        escenario.avl.raiz.key
    )
    assert profundidad == 0
    assert resultado["nodos_avl_examinados"] == escenario.avl.peso() + 1 + visitas_profundidad
    assert resultado["asociaciones"]["candidatos"] == []
    assert resultado["asociaciones"]["asociado"] is None

test_consultar_evento_reporta_nodos_avl_examinados()
print("test consultar evento reporta nodos AVL examinados: OK")

def crear_escenario_consultas(cantidad=7, limite=0):
    escenario = Escenario(
        48,
        40,
        limite,
        72,
        datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    )
    fecha_base = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)
    for id_evento in range(1, cantidad + 1):
        escenario.crearEvento(
            id_evento,
            float(id_evento),
            float(id_evento * 10),
            0.0,
            0.0,
            fecha_base,
            []
        )
    return escenario


def test_consultas_top_k_y_rangos_inclusivos():
    escenario = crear_escenario_consultas()
    escenario.marcarRevisado(7)

    primeros = escenario.consultarPrimerosPendientes(2)
    assert [evento["id"] for evento in primeros["eventos"]] == [6, 5]
    assert primeros["nodos_avl_examinados"] <= escenario.avl.peso()
    assert len(escenario.consultarPrimerosPendientes(100)["eventos"]) == 6

    magnitudes = escenario.consultarPorMagnitud(2, 4)
    assert {evento["id"] for evento in magnitudes["eventos"]} == {2, 3, 4}
    assert magnitudes["nodos_avl_examinados"] == escenario.avl.peso()

    inicio = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)
    fin = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)
    profundidad = escenario.consultarPorProfundidadYFechas(30, inicio, fin)
    assert {evento["id"] for evento in profundidad["eventos"]} == {1, 2, 3}
    assert profundidad["nodos_avl_examinados"] == escenario.avl.peso()

    clave_antes = escenario.avl.encontrarNodo(7).key
    escenario.marcarRevisado(6)
    assert escenario.avl.encontrarNodo(7).key == clave_antes


test_consultas_top_k_y_rangos_inclusivos()
print("test consultas top k y rangos inclusivos: OK")


def test_asociaciones_indican_estado_y_referencias_inversas():
    escenario = Escenario(
        48,
        40,
        3,
        72,
        datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    )
    fecha_anterior = datetime(2026, 9, 28, 9, 0, tzinfo=timezone.utc)
    fecha_posterior = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)
    escenario.crearEvento(1, 6.0, 20.0, 0.0, 0.0, fecha_anterior, [])
    escenario.crearEvento(2, 4.0, 20.0, 0.0, 0.0, fecha_posterior, [])

    nodo_archivado = escenario.avl.encontrarNodo(1)
    escenario.historico.append(nodo_archivado.evento)
    escenario.avl.eliminar(nodo_archivado.key, escenario.modo_estres)
    escenario.bst.eliminar(nodo_archivado.key)

    asociaciones = escenario.consultarAsociaciones(2)
    assert asociaciones["candidatos"] == [{"id": 1, "estado": "archivado"}]
    assert asociaciones["referencia_elegida"] == {"id": 1, "estado": "archivado"}
    assert asociaciones["referenciado_por"] == [{"id": 2, "estado": "activo"}]
    assert asociaciones["nodos_avl_examinados"] > 0


test_asociaciones_indican_estado_y_referencias_inversas()
print("test asociaciones indican estado y referencias inversas: OK")


def test_eventos_costosos_reportan_busqueda_por_clave():
    escenario = crear_escenario_consultas(cantidad=7, limite=0)
    costosos = escenario.consultarEventosCostosos()

    assert costosos["limite"] == 0
    assert costosos["eventos"]
    for evento in costosos["eventos"]:
        assert evento["prioridad"] == 3
        assert evento["profundidad_nodo"] > evento["limite"]
        assert evento["nodos_visitados_busqueda"] == evento["profundidad_nodo"] + 1
    assert costosos["nodos_avl_examinados"] == (
        escenario.avl.peso()
        + sum(evento["nodos_visitados_busqueda"] for evento in costosos["eventos"])
    )


test_eventos_costosos_reportan_busqueda_por_clave()
print("test eventos costosos reportan busqueda por clave: OK")


def test_comparar_ordenes_avl_bst_mismas_claves():
    escenario = crear_escenario_consultas(cantidad=7)
    resultados = escenario.compararOrdenesInsercion()

    ascendente = resultados["ascendente"]
    assert ascendente["altura_bst"] == 6
    assert ascendente["altura_avl"] < ascendente["altura_bst"]
    assert ascendente["comparaciones_bst"] > ascendente["comparaciones_avl"]
    assert ascendente["hojas_avl"] > 0
    assert ascendente["hojas_bst"] == 1
    assert len(ascendente["comparaciones_por_clave"]) == 7


test_comparar_ordenes_avl_bst_mismas_claves()
print("test comparar ordenes AVL y BST con mismas claves: OK")

def test_metrica_correccion_al_reactivar_archivado():

    reloj = datetime(
        2026, 9, 28, 12, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        w=48,
        r=40,
        l=3,
        t=72,
        reloj=reloj
    )

    fecha = datetime(
        2026, 9, 28, 10, 0,
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

    nodo = escenario.avl.encontrarNodo(1)

    # Move the event from both active trees into history.
    escenario.historico.append(nodo.evento)
    escenario.avl.eliminar(nodo.key, escenario.modo_estres)
    escenario.bst.eliminar(nodo.key)

    reporte = Reporte(
        id_evento=1,
        magnitud=6.0,
        profundidad=20.0,
        zonax=100.0,
        zonay=100.0,
        fecha=fecha,
        nRevision=2,
        estacion="EST-02"
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "reactivado"
    assert escenario.metricas["correcciones_aceptadas"] == 1
    assert escenario.avl.encontrarNodo(1) is not None
    assert len(escenario.historico) == 0
test_metrica_correccion_al_reactivar_archivado()
print("test metrica correccion al reactivar archivado: OK")

def test_metricas_rotaciones_avl():

    # LL rotation.
    avl = Avl()

    avl.insertar(Key(1, 5, 1), None, False)
    avl.insertar(Key(1, 4, 2), None, False)
    avl.insertar(Key(1, 3, 3), None, False)

    assert avl.metricas["casos_LL"] == 1
    assert avl.metricas["casos_RR"] == 0
    assert avl.metricas["casos_LR"] == 0
    assert avl.metricas["casos_RL"] == 0
    assert avl.metricas["giros_derecha"] == 1
    assert avl.metricas["giros_izquierda"] == 0

    # RR rotation.
    avl = Avl()

    avl.insertar(Key(1, 3, 1), None, False)
    avl.insertar(Key(1, 4, 2), None, False)
    avl.insertar(Key(1, 5, 3), None, False)

    assert avl.metricas["casos_RR"] == 1
    assert avl.metricas["giros_izquierda"] == 1

    # LR rotation.
    avl = Avl()

    avl.insertar(Key(1, 5, 1), None, False)
    avl.insertar(Key(1, 3, 2), None, False)
    avl.insertar(Key(1, 4, 3), None, False)

    assert avl.metricas["casos_LR"] == 1
    assert avl.metricas["giros_izquierda"] == 1
    assert avl.metricas["giros_derecha"] == 1

    # RL rotation.
    avl = Avl()

    avl.insertar(Key(1, 3, 1), None, False)
    avl.insertar(Key(1, 5, 2), None, False)
    avl.insertar(Key(1, 4, 3), None, False)

    assert avl.metricas["casos_RL"] == 1
    assert avl.metricas["giros_derecha"] == 1
    assert avl.metricas["giros_izquierda"] == 1
test_metricas_rotaciones_avl()
print("test metricas_rotaciones_avl: OK")

def test_indicadores_estructura_escenario():

    reloj = datetime(
        2026, 9, 28, 12, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        w=48,
        r=40,
        l=0,
        t=72,
        reloj=reloj
    )

    fecha = datetime(
        2026, 9, 28, 10, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1, 4.0, 100.0, 0.0, 0.0,
        fecha, ["EST-01"]
    )

    escenario.crearEvento(
        2, 5.0, 20.0, 0.0, 0.0,
        fecha, ["EST-02"]
    )

    escenario.crearEvento(
        3, 6.0, 10.0, 0.0, 0.0,
        fecha, ["EST-03"]
    )

    indicadores = escenario.obtenerIndicadores()

    assert indicadores["eventos_activos"] == 3
    assert indicadores["eventos_historicos"] == 0

    assert indicadores["altura_avl"] >= 0
    assert indicadores["hojas"] >= 1

    assert len(indicadores["inorden"]) == 3
    assert len(indicadores["preorden"]) == 3
    assert len(indicadores["postorden"]) == 3
    assert len(indicadores["anchura"]) == 3

    prioridades = indicadores["eventos_por_prioridad"]

    assert prioridades[1]["cantidad"] == 1
    assert prioridades[2]["cantidad"] == 1
    assert prioridades[3]["cantidad"] == 1

    assert indicadores["eventos_pendientes"]["cantidad"] == 3
test_indicadores_estructura_escenario()
print("test indicadores_estructura_escenario: OK")

def test_metricas_acumulativas():

    reloj = datetime(
        2026, 9, 28, 12, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        w=48,
        r=40,
        l=3,
        t=72,
        reloj=reloj
    )

    fecha = datetime(
        2026, 9, 28, 10, 0,
        tzinfo=timezone.utc
    )

    escenario.crearEvento(
        1,
        4.0,
        100.0,
        0.0,
        0.0,
        fecha,
        ["EST-01"]
    )

    # Manual correction.
    escenario.corregirEvento(
        1,
        magnitud=4.2
    )

    assert escenario.metricas["correcciones_aceptadas"] == 1

    # A report with a newer revision is accepted.
    reporte = Reporte(
        id_evento=1,
        magnitud=4.3,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=3,
        estacion="EST-02"
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "actualizado"
    assert escenario.metricas["correcciones_aceptadas"] == 2

    # A report with an older revision is discarded.
    reporte_antiguo = Reporte(
        id_evento=1,
        magnitud=4.3,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=1,
        estacion="EST-03"
    )

    escenario.procesarReporte(reporte_antiguo)

    assert escenario.metricas["reportes_descartados"] == 1

    # A conflicting report has the same revision but different data.
    reporte_conflicto = Reporte(
        id_evento=1,
        magnitud=5.9,
        profundidad=100.0,
        zonax=0.0,
        zonay=0.0,
        fecha=fecha,
        nRevision=3,
        estacion="EST-04"
    )

    escenario.procesarReporte(reporte_conflicto)

    assert escenario.metricas["conflictos"] == 1
test_metricas_acumulativas()
print("test metricas_acumulativas: OK")

def test_limite_L_acceso_costoso():

    escenario = Escenario(
        48,
        40,
        2,
        72,
        datetime(
            2026, 9, 28, 12, 0,
            tzinfo=timezone.utc
        )
    )

    eventos = [
        (1, 6.0),
        (2, 6.1),
        (3, 6.2),
        (4, 6.3),
        (5, 6.4),
        (6, 6.5),
        (7, 6.6),
        (8, 6.7),
        (9, 6.8),
        (10, 6.9),
        (11, 7.0),
        (12, 7.1),
        (13, 7.2),
        (14, 7.3),
        (15, 7.4),
    ]

    for id_evento, magnitud in eventos:

        escenario.crearEvento(
            id_evento,
            magnitud,
            100.0,
            0.0,
            0.0,
            datetime(
                2026, 9, 28, 12, 0,
                tzinfo=timezone.utc
            ),
            []
        )

    indicadores = escenario.obtenerIndicadores()

    nodos_profundidad = escenario.avl.nodos_con_profundidad()

    profundidades = {
        nodo.key.id_key: profundidad
        for nodo, profundidad in nodos_profundidad
    }

    assert 2 in profundidades.values()
    assert 3 in profundidades.values()

    costosos = indicadores["eventos_costosos"]

    ids_costosos = {
        evento["id"]
        for evento in costosos["eventos"]
    }

    # The threshold is exclusive: depth equal to L is not costly.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 2:
            assert nodo.key.id_key not in ids_costosos

    # Nodes deeper than L are costly.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 3:
            assert nodo.key.id_key in ids_costosos
test_limite_L_acceso_costoso()
print("test limite_L_acceso_costoso: OK")