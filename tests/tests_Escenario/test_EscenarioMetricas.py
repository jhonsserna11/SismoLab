from src.structures.Avl import Avl
from src.structures.Nodo import Key

from src.logic.Escenario import Escenario

from src.domain.Reporte import Reporte

from datetime import datetime, timezone

def test_metricas_rotaciones_avl():
    # LL
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

    # RR
    avl = Avl()
    avl.insertar(Key(1, 3, 1), None, False)
    avl.insertar(Key(1, 4, 2), None, False)
    avl.insertar(Key(1, 5, 3), None, False)

    assert avl.metricas["casos_RR"] == 1
    assert avl.metricas["giros_izquierda"] == 1

    # LR
    avl = Avl()
    avl.insertar(Key(1, 5, 1), None, False)
    avl.insertar(Key(1, 3, 2), None, False)
    avl.insertar(Key(1, 4, 3), None, False)

    assert avl.metricas["casos_LR"] == 1
    assert avl.metricas["giros_izquierda"] == 1
    assert avl.metricas["giros_derecha"] == 1

    # RL
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

    # --------------------------------
    # Corrección manual
    # --------------------------------

    escenario.corregirEvento(
        1,
        magnitud=4.2
    )

    assert escenario.metricas["correcciones_aceptadas"] == 1

    # --------------------------------
    # Reporte con revisión mayor
    # --------------------------------

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

    # --------------------------------
    # Reporte antiguo
    # --------------------------------

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

    # --------------------------------
    # Conflicto
    # misma revisión, datos diferentes
    # --------------------------------

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

    # El árbol debe alcanzar profundidad 3.
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

    # Profundidad 2 == L -> NO es costoso.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 2:
            assert nodo.key.id_key not in ids_costosos

    # Profundidad 3 > L -> SÍ es costoso.
    for nodo, profundidad in nodos_profundidad:
        if profundidad == 3:
            assert nodo.key.id_key in ids_costosos
test_limite_L_acceso_costoso()
print("test limite_L_acceso_costoso: OK")