import os
import sys
from datetime import datetime, timezone

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.domain.Evento import Evento
from src.domain.Reporte import Reporte
from src.logic.Escenario import Escenario


def crear_escenario():
    reloj = datetime(2026, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    return Escenario(48, 40, 3, 72, reloj)


def test_reporte_id_desconocido_registra_evento():
    escenario = crear_escenario()
    reporte = Reporte(
        10,
        1,
        5.5,
        20.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        "EST-01",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "registrado"
    assert escenario.avl.peso() == 1
    assert escenario.avl.encontrarNodo(10) is not None


test_reporte_id_desconocido_registra_evento()
print("test reporte id desconocido registra evento: OK")


def test_reporte_revision_mayor_actualiza_evento():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(20, 4.0, 15.0, 50.0, 50.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)

    reporte = Reporte(
        20,
        2,
        6.0,
        25.0,
        70.0,
        60.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "actualizado"
    nodo = escenario.avl.encontrarNodo(20)
    assert nodo.evento.magnitud == 6.0
    assert nodo.evento.revision == 2


test_reporte_revision_mayor_actualiza_evento()
print("test reporte revision mayor actualiza evento: OK")


def test_reporte_revision_igual_datos_iguales_confirma_evento():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(30, 5.0, 20.0, 100.0, 100.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)

    reporte = Reporte(
        30,
        1,
        5.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "confirmado"
    assert "EST-02" in escenario.avl.encontrarNodo(30).evento.estaciones


test_reporte_revision_igual_datos_iguales_confirma_evento()
print("test reporte revision igual datos iguales confirma evento: OK")


def test_reporte_revision_igual_datos_distintos_rechaza_conflicto():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(40, 5.0, 20.0, 100.0, 100.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)

    reporte = Reporte(
        40,
        1,
        5.0,
        25.0,
        100.0,
        100.0,
        fecha,
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "conflicto"
    assert escenario.avl.encontrarNodo(40).evento.profundidad == 20.0


test_reporte_revision_igual_datos_distintos_rechaza_conflicto()
print("test reporte revision igual datos distintos rechaza conflicto: OK")


def test_reporte_revision_menor_descarta_reporte():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(50, 5.0, 20.0, 100.0, 100.0, fecha, 3, ["EST-01"])
    escenario._crearEvento(evento)

    reporte = Reporte(
        50,
        2,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 11, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "antiguo"
    assert escenario.avl.encontrarNodo(50).evento.revision == 3


test_reporte_revision_menor_descarta_reporte()
print("test reporte revision menor descarta reporte: OK")


def test_reporte_archivado_reactivado_con_revision_mayor():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(60, 4.0, 15.0, 50.0, 50.0, fecha, 1, ["EST-01"])
    escenario.historico.append(evento)

    reporte = Reporte(
        60,
        2,
        5.0,
        20.0,
        80.0,
        80.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "reactivado"
    assert escenario.avl.encontrarNodo(60) is not None
    assert evento not in escenario.historico


test_reporte_archivado_reactivado_con_revision_mayor()
print("test reporte archivado reactivado con revision mayor: OK")


def test_reporte_eliminado_se_rechaza():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(70, 4.0, 15.0, 50.0, 50.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)
    escenario.eliminados.add(70)

    reporte = Reporte(
        70,
        2,
        5.0,
        20.0,
        80.0,
        80.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)

    assert resultado["estado"] == "eliminado"
    assert resultado["accion"] == "rechazar"


test_reporte_eliminado_se_rechaza()
print("test reporte eliminado se rechaza: OK")
