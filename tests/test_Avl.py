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
        ["EST-01"]
    )

def test_insercion():
    arbol = Avl()
    key = Key(3, 4.5, 1)
    arbol.insertar(key, crear_evento(1), False)

    assert arbol.raiz is not None
    assert arbol.raiz.key == key
test_insercion()
print("test insercion: OK")

def test_insercion_simple():
    arbol = Avl()
    k1 = Key(1, 3.5, 1)
    k2 = Key(2, 3.5, 2)
    k3 = Key(2, 3.5, 3)

    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k3, crear_evento(3), False)

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

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k1, crear_evento(1), False)

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

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k3, crear_evento(3), False)

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

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k2, crear_evento(2), False)

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

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k2, crear_evento(2), False)

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

    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)

    arbol.eliminar(k1, False)

    assert arbol.raiz.key == k2
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq is None
    assert arbol.raiz.der.key == k3
test_eliminacion_simple()
print("test eliminacion_simple: OK")

def test_eliminacion_conUnHijo():
    arbol = Avl()
    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 6.5, 3)
    k4 = Key(2, 6.8, 4)

    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k4, crear_evento(4), False)

    arbol.eliminar(k3, False)

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

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k5, crear_evento(5), False)
    arbol.insertar(k4, crear_evento(4), False)
    arbol.insertar(k6, crear_evento(6), False)

    arbol.eliminar(k3, False)

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

    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k3, crear_evento(3), False)

    arbol.eliminar(k2, False)

    assert arbol.raiz.key == k3
    assert arbol.raiz.izq.key == k1
    assert arbol.raiz.der is None
test_eliminacion_Raiz()
print("test eliminacion_raiz: OK")

def test_eliminacion_keyInexistente():
    arbol = Avl()
    k1 = Key(1, 3.6, 1)
    k2 = Key(1, 3.8, 2)
    k3 = Key(2, 5.4, 3)
    k4 = Key(2, 5.5, 4)

    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k3, crear_evento(3), False)

    arbol.eliminar(k4, False)

    assert arbol.raiz.key == k2
test_eliminacion_keyInexistente()
print("test eliminacion_keyInexistente: OK")

def test_duplicados():
    arbol = Avl()
    k1 = Key(1, 4.5, 1)

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k1, crear_evento(1), False)

    assert arbol.raiz.key == k1
    assert arbol.raiz.izq is None
    assert arbol.raiz.der is None
test_duplicados()
print("test duplicados: OK")

def test_peso():
    arbol = Avl()

    k1 = Key(1, 5.0, 1)
    k2 = Key(1, 6.0, 2)
    k3 = Key(1, 7.0, 3)
    k4 = Key(1, 8.0, 4)
    k5 = Key(1, 9.0, 5)

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k5, crear_evento(5), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k4, crear_evento(4), False)

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

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k5, crear_evento(5), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k4, crear_evento(4), False)

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

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k2, crear_evento(2), False)

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

    arbol.insertar(k3, crear_evento(3), False)
    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k5, crear_evento(5), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k4, crear_evento(4), False)

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

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k1, crear_evento(1), False)

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

    arbol.insertar(k1, crear_evento(1), False)
    arbol.insertar(k2, crear_evento(2), False)
    arbol.insertar(k3, crear_evento(3), False)

    k_inexistente = Key(1, 8.0, 4)

    peso_antes = arbol.peso()
    altura_antes = arbol.altura()

    arbol.eliminar(k_inexistente, False)

    assert arbol.peso() == peso_antes
    assert arbol.altura() == altura_antes
test_eliminar_nodo_inexistente()
print("test eliminar_nodo_inexistente: OK")

def test_modoestres_VerificarPostOrden():
    arbol = Avl()

    k10 = Key(1, 2, 10)
    k20 = Key(1, 2, 20)
    k15 = Key(1, 2, 15)
    k30 = Key(1, 2, 30)
    k25 = Key(1, 2, 25)
    k40 = Key(1, 2, 40)
    k22 = Key(1, 2, 22)
    k27 = Key(1, 2, 27)
    k50 = Key(1, 2, 50)

    arbol.insertar(k10, crear_evento(10), True)
    arbol.insertar(k20, crear_evento(20), True)
    arbol.insertar(k15, crear_evento(15), True)
    arbol.insertar(k30, crear_evento(30), True)
    arbol.insertar(k25, crear_evento(25), True)
    arbol.insertar(k40, crear_evento(40), True)
    arbol.insertar(k22, crear_evento(22), True)
    arbol.insertar(k27, crear_evento(27), True)
    arbol.insertar(k50, crear_evento(50), True)

    arbol.raiz = arbol._recuperar(arbol.raiz)
    inorder = []
    arbol._inOrder(arbol.raiz, inorder)

    ids_inorder = [key.id_key for key in inorder]

    assert ids_inorder == [10, 15, 20, 22, 25, 27, 30, 40, 50]
test_modoestres_VerificarPostOrden()
print("test modoestres_VerificarPostOrden: ")

def test_recuperacion_arbol_desbalanceado():

    arbol = Avl()

    ids = [10, 20, 30, 15, 25, 40, 22, 27, 50]

    for id_evento in ids:
        key = Key(1, 2, id_evento)
        arbol.insertar(key, crear_evento(id_evento), True)

    assert arbol.altura() == 4
    assert arbol._factor_balance(arbol.raiz) == -4

    arbol.raiz = arbol._recuperar(arbol.raiz)

    assert arbol.raiz.key.id_key == 20
    assert arbol.raiz.altura == 3

    assert arbol.peso() == 9

    claves = []

    def guardar_inorder(nodo):
        if nodo is None:
            return
        guardar_inorder(nodo.izq)
        claves.append(nodo.key.id_key)
        guardar_inorder(nodo.der)

    guardar_inorder(arbol.raiz)

    assert claves == [10, 15, 20, 22, 25, 27, 30, 40, 50]

    def verificar_avl(nodo):
        if nodo is None:
            return

        balance = arbol._factor_balance(nodo)

        assert -1 <= balance <= 1

        verificar_avl(nodo.izq)
        verificar_avl(nodo.der)

    verificar_avl(arbol.raiz)
test_recuperacion_arbol_desbalanceado()
print("test recuperacion_arbol_desbalanceado: OK")


def test_auditoria_detecta_orden_global_incorrecto():
    arbol = Avl()
    arbol.insertar(Key(1, 5.0, 20), crear_evento(20), True)
    arbol.insertar(Key(1, 5.0, 10), crear_evento(10), True)
    arbol.insertar(Key(1, 5.0, 30), crear_evento(30), True)
    arbol.raiz.izq.der = Nodo(Key(1, 5.0, 25), crear_evento(25))

    reporte = arbol.verificarEstructura(True)
    registro = next(
        evento for evento in reporte["eventos_inconsistentes"]
        if evento["id"] == 25
    )
    assert not reporte["valido"]
    assert "Clave fuera del límite superior global" in registro["errores"]
test_auditoria_detecta_orden_global_incorrecto()
print("test auditoria orden global: OK")


def test_auditoria_distingue_desbalance_en_estres():
    arbol = Avl()
    for id_evento in (1, 2, 3):
        arbol.insertar(Key(1, 5.0, id_evento), crear_evento(id_evento), True)

    reporte_estres = arbol.verificarEstructura(True)
    reporte_normal = arbol.verificarEstructura(False)
    assert reporte_estres["valido"]
    assert not reporte_estres["equilibrado"]
    assert any(evento["advertencias"] for evento in reporte_estres["eventos_inconsistentes"])
    assert not reporte_normal["valido"]
    assert any(
        "Factor de balance" in error
        for evento in reporte_normal["eventos_inconsistentes"]
        for error in evento["errores"]
    )
test_auditoria_distingue_desbalance_en_estres()
print("test auditoria modo estres: OK")


def test_auditoria_detecta_altura_incorrecta():
    arbol = Avl()
    arbol.insertar(Key(1, 5.0, 1), crear_evento(1), False)
    arbol.raiz.altura = 3

    reporte = arbol.verificarEstructura()
    assert not reporte["valido"]
    assert "Altura almacenada 3; recalculada 0" in reporte["eventos_inconsistentes"][0]["errores"]
test_auditoria_detecta_altura_incorrecta()
print("test auditoria altura: OK")


def test_auditoria_detecta_identificadores_duplicados():
    arbol = Avl()
    arbol.raiz = Nodo(Key(1, 5.0, 7), crear_evento(7))
    arbol.raiz.der = Nodo(Key(2, 5.0, 7), crear_evento(7))
    arbol.raiz.altura = 1

    reporte = arbol.verificarEstructura()

    assert not reporte["valido"]
    assert sum(
        any("Identificador duplicado: 7" in error for error in evento["errores"])
        for evento in reporte["eventos_inconsistentes"]
    ) == 2
test_auditoria_detecta_identificadores_duplicados()
print("test auditoria IDs duplicados: OK")


def test_auditoria_detecta_referencia_ciclica_y_termina():
    arbol = Avl()
    arbol.raiz = Nodo(Key(1, 5.0, 1), crear_evento(1))
    arbol.raiz.izq = Nodo(Key(1, 5.0, 2), crear_evento(2))
    arbol.raiz.izq.der = arbol.raiz.izq
    arbol.raiz.altura = 1

    reporte = arbol.verificarEstructura()
    registros_repetidos = [
        evento for evento in reporte["eventos_inconsistentes"]
        if "repetido_de" in evento
    ]

    assert not reporte["valido"]
    assert len(registros_repetidos) == 1
    assert registros_repetidos[0]["id"] == 2
    assert registros_repetidos[0]["altura_recalculada"] is None
    assert reporte["nodos_visitados"] == 2
test_auditoria_detecta_referencia_ciclica_y_termina()
print("test auditoria referencia ciclica: OK")


def test_auditoria_detecta_factor_invalido_en_modo_normal():
    arbol = Avl()
    arbol.raiz = Nodo(Key(1, 5.0, 1), crear_evento(1))
    arbol.raiz.der = Nodo(Key(1, 5.0, 2), crear_evento(2))
    arbol.raiz.der.der = Nodo(Key(1, 5.0, 3), crear_evento(3))
    arbol.raiz.altura = 2
    arbol.raiz.der.altura = 1

    reporte = arbol.verificarEstructura(modo_estres=False)
    registro_raiz = next(
        evento for evento in reporte["eventos_inconsistentes"]
        if evento["id"] == 1
    )

    assert not reporte["valido"]
    assert registro_raiz["factor_balance_recalculado"] == -2
    assert any("Factor de balance" in error for error in registro_raiz["errores"])
test_auditoria_detecta_factor_invalido_en_modo_normal()
print("test auditoria factor normal: OK")


def test_auditoria_detecta_id_key_distinto_del_evento():
    arbol = Avl()
    arbol.raiz = Nodo(Key(1, 5.0, 2), crear_evento(1))

    reporte = arbol.verificarEstructura()

    assert not reporte["valido"]
    assert any(
        "El identificador de la clave no coincide con el evento" in error
        for evento in reporte["eventos_inconsistentes"]
        for error in evento["errores"]
    )
test_auditoria_detecta_id_key_distinto_del_evento()
print("test auditoria ID de clave: OK")


def test_auditoria_detecta_magnitud_key_distinta_del_evento():
    arbol = Avl()
    arbol.raiz = Nodo(Key(1, 5.5, 1), crear_evento(1))

    reporte = arbol.verificarEstructura()

    assert not reporte["valido"]
    assert any(
        "La magnitud de la clave no coincide con el evento" in error
        for evento in reporte["eventos_inconsistentes"]
        for error in evento["errores"]
    )
test_auditoria_detecta_magnitud_key_distinta_del_evento()
print("test auditoria magnitud de clave: OK")