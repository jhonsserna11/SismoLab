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


def test_reporte_fecha_no_utc_o_con_microsegundos_se_rechaza():
    escenario = crear_escenario()
    fecha_naive = datetime(2026, 9, 22, 12, 0, 0)
    fecha_con_micro = datetime(2026, 9, 22, 12, 0, 0, 123456, tzinfo=timezone.utc)

    reporte_naive = Reporte(
        11,
        1,
        5.5,
        20.0,
        100.0,
        100.0,
        fecha_naive,
        "EST-01",
    )
    reporte_micro = Reporte(
        12,
        1,
        5.5,
        20.0,
        100.0,
        100.0,
        fecha_con_micro,
        "EST-01",
    )

    assert escenario.procesarReporte(reporte_naive)["estado"] == "desconocido"
    assert escenario.procesarReporte(reporte_micro)["estado"] == "desconocido"


test_reporte_fecha_no_utc_o_con_microsegundos_se_rechaza()
print("test reporte fecha no utc o con microsegundos se rechaza: OK")


def test_reporte_invalido_no_modifica_el_escenario():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(13, 5.0, 20.0, 100.0, 100.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)

    reporte_invalido = Reporte(
        13,
        2,
        11.0,
        20.0,
        100.0,
        100.0,
        fecha,
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte_invalido)

    assert resultado["estado"] == "desconocido"
    nodo = escenario.avl.encontrarNodo(13)
    assert nodo is not None
    assert nodo.evento.magnitud == 5.0
    assert nodo.evento.revision == 1
    assert nodo.evento.estaciones == ["EST-01"]
    assert len(escenario.historico) == 0
    assert 13 not in escenario.eliminados


test_reporte_invalido_no_modifica_el_escenario()
print("test reporte invalido no modifica el escenario: OK")


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


def test_reporte_revision_mayor_vuelve_evento_a_pendiente():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(21, 4.0, 15.0, 50.0, 50.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)
    escenario.marcarRevisado(21)

    reporte = Reporte(
        21,
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
    assert escenario.avl.encontrarNodo(21).evento.estado == "Pendiente"


test_reporte_revision_mayor_vuelve_evento_a_pendiente()
print("test reporte revision mayor vuelve evento a pendiente: OK")


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
    nodo = escenario.avl.encontrarNodo(30)

    assert resultado["estado"] == "confirmado"
    assert nodo.evento.revision == 1
    assert nodo.evento.magnitud == 5.0
    assert nodo.evento.profundidad == 20.0
    assert "EST-02" in nodo.evento.estaciones
    assert nodo.evento.estaciones.count("EST-02") == 1


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


def test_reporte_conflicto_no_modifica_evento():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(41, 5.0, 20.0, 100.0, 100.0, fecha, 1, ["EST-01"])
    escenario._crearEvento(evento)

    original = {
        "magnitud": evento.magnitud,
        "profundidad": evento.profundidad,
        "zonax": evento.zonax,
        "zonay": evento.zonay,
        "fecha": evento.fechaHora,
        "revision": evento.revision,
        "estaciones": evento.estaciones.copy(),
        "key": escenario.avl.encontrarNodo(41).key,
    }

    reporte = Reporte(
        41,
        1,
        5.0,
        25.0,
        100.0,
        100.0,
        fecha,
        "EST-02",
    )

    resultado = escenario.procesarReporte(reporte)
    nodo = escenario.avl.encontrarNodo(41)

    assert resultado["estado"] == "conflicto"
    assert nodo.evento.magnitud == original["magnitud"]
    assert nodo.evento.profundidad == original["profundidad"]
    assert nodo.evento.zonax == original["zonax"]
    assert nodo.evento.zonay == original["zonay"]
    assert nodo.evento.fechaHora == original["fecha"]
    assert nodo.evento.revision == original["revision"]
    assert nodo.evento.estaciones == original["estaciones"]
    assert nodo.key == original["key"]
    assert "EST-02" not in nodo.evento.estaciones


test_reporte_conflicto_no_modifica_evento()
print("test reporte conflicto no modifica evento: OK")


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
    nodo = escenario.avl.encontrarNodo(60)

    assert resultado["estado"] == "reactivado"
    assert nodo is not None
    assert nodo.evento.estado == "Pendiente"
    assert evento not in escenario.historico


test_reporte_archivado_reactivado_con_revision_mayor()
print("test reporte archivado reactivado con revision mayor: OK")


def test_reporte_archivado_con_revision_igual_o_menor_no_reactiva():
    escenario = crear_escenario()
    fecha = datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc)
    evento = Evento(61, 4.0, 15.0, 50.0, 50.0, fecha, 2, ["EST-01"])
    escenario.historico.append(evento)

    reporte_igual = Reporte(
        61,
        2,
        5.0,
        20.0,
        80.0,
        80.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )
    reporte_menor = Reporte(
        61,
        1,
        5.0,
        20.0,
        80.0,
        80.0,
        datetime(2026, 9, 22, 13, 0, 0, tzinfo=timezone.utc),
        "EST-02",
    )

    assert escenario.procesarReporte(reporte_igual)["estado"] == "archivado"
    assert escenario.procesarReporte(reporte_menor)["estado"] == "archivado"
    assert 61 in [e.id for e in escenario.historico]


test_reporte_archivado_con_revision_igual_o_menor_no_reactiva()
print("test reporte archivado con revision igual o menor no reactiva: OK")


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
    assert escenario.avl.encontrarNodo(70) is not None


test_reporte_eliminado_se_rechaza()
print("test reporte eliminado se rechaza: OK")
