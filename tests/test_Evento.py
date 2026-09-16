from src.domain.Evento import Evento
from decimal import Decimal
from datetime import datetime, timezone

def test_crearEvento():
    evento = Evento(10, 9.3, 10.2, 100, 350, datetime(2026, 10, 1, 12, 45, 34), 1, "Est-1")

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
        evento = Evento(10, 9.31, 10.2, 100, 350, datetime(2026, 10, 1, 12, 45, 34), 1, "Est-1")
    except ValueError:
        print("test crearEvento_magnitudMasdeUnDecimal: OK")
        return
    print("test crearEvento_magnitudMasdeUnDecimal: FALLÓ")
test_crearEvento_magnitudMasdeUnDecimal()

def test_crearEvento_Entero():
    evento = Evento(10, 9.3, 10, 100, 350, datetime(2026, 10, 1, 12, 45, 34), 1, "Est-1")

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
    evento = Evento(1, 5.0, 100.0, 100, 300, datetime(2026, 10, 1, 10, 59, 34), 1, "Est-1")

    p = evento.calcularPrioridad(False)
    assert p == 2
test_calcularPrioridad2()
print("test calcularPrioridad2: OK")

def test_calcularPrioridad1():
    evento = Evento(1, 4.4, 100.0, 100, 300, datetime(2026, 10, 1, 10, 59, 34), 1, "Est-1")

    p = evento.calcularPrioridad(False)
    assert p == 1
test_calcularPrioridad1()
print("test calcularPrioridad1: OK")