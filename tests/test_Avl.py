from src.structures.Avl import Avl
from src.structures.Nodo import Key
from src.structures.Nodo import Nodo

def test_insercion():
    arbol = Avl()
    key = (3, 4.5, 1)
    arbol.insertar(key)

    assert arbol.raiz is not None
    assert arbol.raiz.key == key
test_insercion()
print("test insercion: OK")

def test_insercion_simple():
    arbol = Avl()
    k1 = Key(1, 3.5, 1)
    k2 = Key(2, 3.5, 2)
    k3 = Key(2, 3.5, 3)

    arbol.insertar(k2)
    arbol.insertar(k1)
    arbol.insertar(k3)

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

    arbol.insertar(k3)
    arbol.insertar(k2)
    arbol.insertar(k1)

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

    arbol.insertar(k1)
    arbol.insertar(k2)
    arbol.insertar(k3)

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

    arbol.insertar(k3)
    arbol.insertar(k1)
    arbol.insertar(k2)

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

    arbol.insertar(k1)
    arbol.insertar(k3)
    arbol.insertar(k2)

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

    arbol.insertar(k2)
    arbol.insertar(k3)
    arbol.insertar(k1)

    arbol.eliminar(k1)

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq == None
    assert arbol.raiz.der.key == k3
test_eliminacion_simple()
print("test eliminacion_simple: OK")