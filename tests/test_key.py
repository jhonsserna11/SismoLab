from src.structures.Nodo import Key

def test_equalKeys():
    k1 = Key(3, 5.0, 1)
    k2 = Key(3, 5.0, 1)
    assert k1 == k2
test_equalKeys()
print("Prueba test_equalKeys: OK")


def test_Prioridad_menorKey():
    k1 = Key(2, 9.0, 2)
    k2 = Key(3, 1.0, 1)
    assert k1 < k2
test_Prioridad_menorKey()
print("Prueba Prioridad_test_menorKey: OK")

def test_Prioridad_mayorKey():
    k1 = Key(2, 9.0, 1)
    k2 = Key(3, 1.0, 2)
    assert k2 > k1
test_Prioridad_mayorKey()
print("Prueba Prioridad_test_mayorKey: OK")


def test_Magnitud_menorKey():
    k1 = Key(2, 6.5, 1)
    k2 = Key(2, 6.0, 2)
    assert k2 < k1
test_Magnitud_menorKey()
print("test_Magnitud_menorKey: OK")

def test_Magnitud_mayorKey():
    k1 = Key(2, 6.5, 1)
    k2 = Key(2, 6.0, 100)
    assert k2 < k1
test_Magnitud_mayorKey()
print("test_Magnitud_mayorKey: OK")


def test_Id_menorKey():
    k1 = Key(2, 7.0, 1)
    k2 = Key(2, 7.0, 2)
    assert k1 < k2
test_Id_menorKey()
print("test_Id_menorKey: OK")

def test_Id_mayorKey():
    k1 = Key(2, 5.0, 1)
    k2 = Key(2, 5.0, 100)
    assert k2 > k1
test_Id_mayorKey()
print("test_Id_mayorKey: OK")