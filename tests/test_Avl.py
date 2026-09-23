from src.structures.Avl import Avl
from src.structures.Nodo import Key
from src.structures.Nodo import Nodo

from src.domain.Evento import Evento
from datetime import datetime, timezone

def crear_evento(id_evento):
    return Evento(
        id_evento,
        5.0,
        20.0,
        100.0,
        100.0,
        datetime(2026, 9, 22, 12, 0, 0, tzinfo=timezone.utc),
        1,
        "EST-01"
    )

def test_insercion():
    arbol = Avl()
    key = (3, 4.5, 1)
    arbol.insertar(key, crear_evento(1))

    assert arbol.raiz is not None
    assert arbol.raiz.key == key
test_insercion()
print("test insercion: OK")

def test_insercion_simple():
    arbol = Avl()
    k1 = Key(1, 3.5, 1)
    k2 = Key(2, 3.5, 2)
    k3 = Key(2, 3.5, 3)

    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k3, crear_evento(3))

    assert arbol.raiz.key == k2
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k3
    assert arbol.raiz.altura == 1
    assert arbol.altura() == 1
test_insercion_simple()
print("test insercion simple: OK")

def test_insercion_rotacionLL():
    arbol = Avl()
    k1 = Key(2, 5.0, 1)
    k2 = Key(2, 5.0, 2)
    k3 = Key(2, 5.2, 3)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k1, crear_evento(1))

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k3
test_insercion_rotacionLL()
print("test insercion_rotacionLL: OK")

def test_insercion_rotacionRR():
    arbol = Avl()
    k1 = Key(1, 5.0, 1)
    k2 = Key(2, 7.0, 2)
    k3 = Key(2, 7.4, 3)

    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k3, crear_evento(3))

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k3
test_insercion_rotacionRR()
print("test insercion_rotacionRR: OK")

def test_insercion_rotacionLR():
    arbol = Avl()
    k1 = Key(1, 5.1, 1)
    k2 = Key(1, 5.3, 2)
    k3 = Key(2, 8.0, 3)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k2, crear_evento(2))

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k3
test_insercion_rotacionLR()
print("test insercion_rotacionLR: OK")

def test_insercion_rotacionRL():
    arbol = Avl()
    k1 = Key(1, 5.1, 1)
    k2 = Key(1, 5.4, 2)
    k3 = Key(2, 8.0, 3)

    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k2, crear_evento(2))

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k3
test_insercion_rotacionRL()
print("test insercion_rotacionRL: OK")

def test_eliminacion_simple():
    arbol = Avl()
    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 6.0, 3)

    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))

    arbol.eliminar(k1)

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq == None
    assert arbol.raiz.der.key == k3
test_eliminacion_simple()
print("test eliminacion_simple: OK")

def test_eliminacion_conUnHijo():
    arbol = Avl()
    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 6.5, 3)
    k4 = Key(2, 6.8, 4)

    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k4, crear_evento(4))

    arbol.eliminar(k3)

    assert arbol.raiz.key == k2
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der.key == k4
    assert arbol.altura() == 1
test_eliminacion_conUnHijo()
print("test eliminacion_conUnHijo: OK")

def test_eliminacion_conDosHijos():
    arbol = Avl()
    k1 = Key(1, 6.0, 1)
    k3 = Key(2, 6.5, 3)
    k4 = Key(2, 6.8, 4)
    k5 = Key(3, 7.0, 5)
    k6 = Key(3, 7.1, 6)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k5, crear_evento(5))
    arbol.insertar(k4, crear_evento(4))
    arbol.insertar(k6, crear_evento(6))

    arbol.eliminar(k3)

    assert arbol.raiz.key == k4
    assert arbol.raiz.evento.id == k4.id_key
    assert arbol.raiz.der.key == k5
    assert arbol.raiz.izq.key == k1
test_eliminacion_conDosHijos()
print("test eliminacion_conDosHijos: OK")

def test_eliminacion_Raiz():
    arbol = Avl()
    k1 = Key(1, 2.0, 1)
    k2 = Key(1, 4.3, 2)
    k3 = Key(2, 5.0, 3)

    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k3, crear_evento(3))

    arbol.eliminar(k2)

    assert arbol.raiz.key == k3
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der == None
test_eliminacion_Raiz()
print("test eliminacion_raiz: OK")

def test_eliminacion_keyInexistente():
    arbol = Avl()
    k1 = Key(1, 3.6, 1)
    k2 = Key(1, 3.8, 2)
    k3 = Key(2, 5.4, 3)
    k4 = Key(2, 5.5, 4)

    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k1,crear_evento(1))
    arbol.insertar(k3, crear_evento(3))

    arbol.eliminar(k4)

    assert arbol.raiz.key == k2
test_eliminacion_keyInexistente()
print("test eliminacion_keyInexistente: OK")

def test_duplicados():
    arbol = Avl()
    k1 = Key(1, 4.5, 1)
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k1, crear_evento(1))

    assert arbol.raiz.key == k1
    assert arbol.raiz.izq == None
    assert arbol.raiz.der == None
test_duplicados()
print("test duplicados: OK")

def test_peso():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 7.0, 3)
    k4 = Key(1, 8.0, 4)
    k5 = Key(1, 9.0, 5)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k5, crear_evento(5))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k4, crear_evento(4))

    assert arbol.peso() == 5
test_peso()
print("test peso: OK")

def test_nivelNodo():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 7.0, 3)
    k4 = Key(1, 8.0, 4)
    k5 = Key(1, 9.0, 5)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k5, crear_evento(5))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k4, crear_evento(4))

    assert arbol.nivel_de_un_nodo(k3) == 0
    assert arbol.nivel_de_un_nodo(k1) == 1
    assert arbol.nivel_de_un_nodo(k5) == 1
    assert arbol.nivel_de_un_nodo(k2) == 2
    assert arbol.nivel_de_un_nodo(k4) == 2
test_nivelNodo()
print("test nivelNodo: OK")

def test_nivelNodo_Inexistente():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)

    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k2, crear_evento(2))

    k_inexistente = Key(1, 7.0, 3)

    assert arbol.nivel_de_un_nodo(k_inexistente) == -1
test_nivelNodo_Inexistente()
print("test nivelNodo_inexistente: OK")

def test_cantidad_de_nodos_por_nivel():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 7.0, 3)
    k4 = Key(1, 8.0, 4)
    k5 = Key(1, 9.0, 5)

    arbol.insertar(k3, crear_evento(3))
    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k5, crear_evento(5))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k4, crear_evento(4))

    conteo = arbol.cantidad_de_nodos_por_nivel()

    assert conteo[0] == 1
    assert conteo[1] == 2
    assert conteo[2] == 2
test_cantidad_de_nodos_por_nivel()
print("test cantidad_de_nodos_por_nivel: OK")

def test_arbol_vacio():
    arbol = Avl()

    assert arbol.altura() == -1
    assert arbol.peso() == 0
    assert arbol.cantidad_de_nodos_por_nivel() == {}
    assert arbol.nivel_de_un_nodo(Key(1, 5.0, 1)) == -1
test_arbol_vacio()
print("test arbol_vacio: OK")

def test_insertar_duplicado():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)

    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k1, crear_evento(1))

    assert arbol.peso() == 1
    assert arbol.raiz.key == k1
    assert arbol.raiz.izq is None
    assert arbol.raiz.der is None
test_insertar_duplicado()
print("test insertar_duplicado: OK")

def test_eliminar_nodo_inexistente():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 7.0, 3)

    arbol.insertar(k1, crear_evento(1))
    arbol.insertar(k2, crear_evento(2))
    arbol.insertar(k3, crear_evento(3))

    k_inexistente = Key(1, 8.0, 4)

    peso_antes = arbol.peso()
    altura_antes = arbol.altura()

    arbol.eliminar(k_inexistente)

    assert arbol.peso() == peso_antes
    assert arbol.altura() == altura_antes
test_eliminar_nodo_inexistente()
print("test eliminar_nodo_inexistente: OK")