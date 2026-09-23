from src.domain.Evento import Evento
from decimal import Decimal
from datetime import datetime, timezone

def test_crearEvento():
    evento = Evento(10, 9.3, 10.2, 100, 350, datetime(2026, 10, 1, 12, 45, 34, tzinfo=timezone.utc), 1, "Est-1")

    assert evento.id == 10
    assert type(evento.magnitud) is Decimal
    assert type(evento.profundidad) is Decimal
    assert type(evento.zonax) is Decimal
    assert type(evento.zonay) is Decimal
    assert evento.estado == "Pendiente"
    assert evento.estacion == "Est-1"
    assert type(evento.fechaHora) is datetime
test_crearEvento()
print("test crearEvento: OK")

def test_crearEvento_magnitudMasdeUnDecimal():
    try:
        evento = Evento(10, 9.31, 10.2, 100, 350, datetime(2026, 10, 1, 12, 45, 34, tzinfo=timezone.utc), 1, "Est-1")
    except ValueError:
        print("test crearEvento_magnitudMasdeUnDecimal: OK")
        return
    print("test crearEvento_magnitudMasdeUnDecimal: FALLÓ")
test_crearEvento_magnitudMasdeUnDecimal()

def test_crearEvento_Entero():
    evento = Evento(10, 9.3, 10, 100, 350, datetime(2026, 10, 1, 12, 45, 34, tzinfo=timezone.utc), 1, "Est-1")

    assert str(evento.profundidad) == "10.0"
test_crearEvento_Entero()
print("test crearEvento_Entero: OK")


def test_calcularPrioridad3():
    evento = Evento(1, 6.0, 10.0, 100, 300, datetime(2026, 10, 1, 10, 59, 34, tzinfo=timezone.utc), 1,"Est-1")

    p = evento.calcularPrioridad(False)
    assert p == 3
test_calcularPrioridad3()
print("test calcularPrioridad3: OK")

def test_calcularPrioridad2():
    evento = Evento(1, 5.0, 100.0, 100, 300, datetime(2026, 10, 1, 10, 59, 34, tzinfo=timezone.utc), 1, "Est-1")

    p = evento.calcularPrioridad(False)
    assert p == 2
test_calcularPrioridad2()
print("test calcularPrioridad2: OK")

def test_calcularPrioridad1():
    evento = Evento(1, 4.4, 100.0, 100, 300, datetime(2026, 10, 1, 10, 59, 34, tzinfo=timezone.utc), 1, "Est-1")

    p = evento.calcularPrioridad(False)
    assert p == 1
test_calcularPrioridad1()
print("test calcularPrioridad1: OK")


def test_esCandidato_valido():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 120, 300,
        datetime(2026, 10, 1, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_valido()
print("test esCandidato_valido: OK")

def test_esCandidato_mismaMagnitud():
    eventoA = Evento(
        1, 4.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_mismaMagnitud()
print("test esCandidato_mismaMagnitud: OK")

def test_esCandidato_ocurreDespues():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_ocurreDespues()
print("test esCandidato_ocurreDespues: OK")

def test_esCandidato_ocurreExacto2diasDespues():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 100, 300,
        datetime(2026, 10, 3, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_ocurreExacto2diasDespues()
print("test esCandidato_ocurreExacto2diasDespues: OK")

def test_esCandidato_distanciaMaxima():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 140, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_distanciaMaxima()
print("test esCandidato_distanciaMaxima: OK")

def test_esCandidato_distanciaMaximaMasDecimal():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 140.1, 300,
        datetime(2026, 10, 1, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_distanciaMaximaMasDecimal()
print("test esCandidato_distanciaMaximaMasDecimal: OK")

def test_esCandidato_ocurreAlMismoTiempo():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 140, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_ocurreAlMismoTiempo()
print("test esCandidato_ocurreAlMismoTiempo: OK")

def test_esCandidato_ocurreUnSegundoDespues():
    eventoA = Evento(
        1, 5.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 13, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 140, 300,
        datetime(2026, 10, 1, 13, 00, 1, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_ocurreUnSegundoDespues()
print("test esCandidato_ocurreUnSegundoDespues: OK")

def test_esCandidato_distanciaLejana():
    eventoA = Evento(
        1, 4.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 3.0, 100.0, 500, 400,
        datetime(2026, 10, 2, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_distanciaLejana()
print("test esCandidato_distanciaLejana: OK")

def test_esCandidato_magnitudMenor():
    eventoA = Evento(
        1, 2.0, 100.0, 100, 300,
        datetime(2026, 10, 1, 10, 00, 00, tzinfo=timezone.utc),
        1, "Est-1"
    )

    eventoB = Evento(
        2, 4.0, 100.0, 120, 300,
        datetime(2026, 10, 1, 12, 00, 00, tzinfo=timezone.utc),
        1, "Est-2"
    )

    assert not eventoA.esCandidato(eventoB, 48, 40)
test_esCandidato_magnitudMenor()
print("test esCandidato_magnitudMenor: OK")