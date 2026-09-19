from src.structures.Bst import Bst
from src.structures.Nodo import Key


def crear_claves():
    return {
        "raiz": Key(2, 5.0, 2),
        "izquierda": Key(1, 4.0, 1),
        "derecha": Key(3, 6.0, 3),
        "izquierda_izquierda": Key(0, 3.0, 0),
        "izquierda_derecha": Key(1, 4.5, 4),
        "derecha_izquierda": Key(2, 5.5, 5),
        "derecha_derecha": Key(4, 7.0, 6),
    }


crear_claves()
print("crear_claves: OK")


def crear_arbol_completo():
    claves = crear_claves()
    arbol = Bst()
    for nombre in (
        "raiz",
        "izquierda",
        "derecha",
        "izquierda_izquierda",
        "izquierda_derecha",
        "derecha_izquierda",
        "derecha_derecha",
    ):
        arbol.insertar(claves[nombre])
    return arbol, claves


crear_arbol_completo()
print("crear_arbol_completo: OK")


def test_arbol_nuevo_esta_vacio():
    arbol = Bst()

    assert arbol.raiz is None
    assert arbol.altura() == -1
    assert arbol.cantidad_nodos() == 0


test_arbol_nuevo_esta_vacio()
print("test arbol nuevo esta vacio: OK")


def test_insertar_un_nodo():
    arbol = Bst()
    clave = Key(1, 4.5, 1)

    arbol.insertar(clave)

    assert arbol.raiz is not None
    assert arbol.raiz.key == clave
    assert arbol.raiz.izq is None
    assert arbol.raiz.der is None
    assert arbol.altura() == 0
    assert arbol.cantidad_nodos() == 1


test_insertar_un_nodo()
print("test insertar un nodo: OK")


def test_insertar_construye_subarboles_izquierdo_y_derecho():
    arbol, claves = crear_arbol_completo()

    assert arbol.raiz.key == claves["raiz"]
    assert arbol.raiz.izq.key == claves["izquierda"]
    assert arbol.raiz.der.key == claves["derecha"]
    assert arbol.raiz.izq.izq.key == claves["izquierda_izquierda"]
    assert arbol.raiz.izq.der.key == claves["izquierda_derecha"]
    assert arbol.raiz.der.izq.key == claves["derecha_izquierda"]
    assert arbol.raiz.der.der.key == claves["derecha_derecha"]
    assert arbol.altura() == 2
    assert arbol.cantidad_nodos() == 7


test_insertar_construye_subarboles_izquierdo_y_derecho()
print("test insertar construye subarboles izquierdo y derecho: OK")


def test_insertar_duplicado_no_agrega_nodo():
    arbol = Bst()
    clave = Key(1, 4.5, 1)

    arbol.insertar(clave)
    arbol.insertar(clave)

    assert arbol.cantidad_nodos() == 1
    assert arbol.raiz.key == clave
    assert arbol.raiz.izq is None
    assert arbol.raiz.der is None


test_insertar_duplicado_no_agrega_nodo()
print("test insertar duplicado no agrega nodo: OK")


def test_buscar_en_arbol_vacio_devuelve_none():
    assert Bst().buscar(Key(1, 4.5, 1)) is None


test_buscar_en_arbol_vacio_devuelve_none()
print("test buscar en arbol vacio devuelve None: OK")


def test_buscar_devuelve_el_nodo_correcto():
    arbol, claves = crear_arbol_completo()

    resultado = arbol.buscar(claves["derecha_izquierda"])

    assert resultado is arbol.raiz.der.izq
    assert resultado.key == claves["derecha_izquierda"]


test_buscar_devuelve_el_nodo_correcto()
print("test buscar devuelve el nodo correcto: OK")


def test_buscar_clave_inexistente_devuelve_none():
    arbol, _ = crear_arbol_completo()

    assert arbol.buscar(Key(5, 8.0, 8)) is None


test_buscar_clave_inexistente_devuelve_none()
print("test buscar clave inexistente devuelve None: OK")


def test_encontrar_minimo_recorre_hacia_la_izquierda():
    arbol, claves = crear_arbol_completo()

    minimo = arbol._encontrar_minimo(arbol.raiz)

    assert minimo.key == claves["izquierda_izquierda"]


test_encontrar_minimo_recorre_hacia_la_izquierda()
print("test encontrar minimo recorre hacia la izquierda: OK")


def test_eliminar_hoja():
    arbol, claves = crear_arbol_completo()

    arbol.eliminar(claves["izquierda_izquierda"])

    assert arbol.buscar(claves["izquierda_izquierda"]) is None
    assert arbol.raiz.izq.izq is None
    assert arbol.cantidad_nodos() == 6


test_eliminar_hoja()
print("test eliminar hoja: OK")


def test_eliminar_nodo_con_un_hijo_derecho():
    arbol = Bst()
    raiz = Key(2, 5.0, 2)
    padre = Key(1, 4.0, 1)
    hijo = Key(0, 3.0, 0)
    for clave in (raiz, padre, hijo):
        arbol.insertar(clave)

    arbol.eliminar(padre)

    assert arbol.raiz.izq.key == hijo
    assert arbol.cantidad_nodos() == 2


test_eliminar_nodo_con_un_hijo_derecho()
print("test eliminar nodo con un hijo derecho: OK")


def test_eliminar_nodo_con_un_hijo_izquierdo():
    arbol = Bst()
    raiz = Key(1, 4.0, 1)
    padre = Key(2, 5.0, 2)
    hijo = Key(3, 6.0, 3)
    for clave in (raiz, padre, hijo):
        arbol.insertar(clave)

    arbol.eliminar(padre)

    assert arbol.raiz.der.key == hijo
    assert arbol.cantidad_nodos() == 2


test_eliminar_nodo_con_un_hijo_izquierdo()
print("test eliminar nodo con un hijo izquierdo: OK")


def test_eliminar_nodo_con_dos_hijos_usa_sucesor_inorden():
    arbol, claves = crear_arbol_completo()

    arbol.eliminar(claves["raiz"])

    assert arbol.raiz.key == claves["derecha_izquierda"]
    assert arbol.raiz.izq.key == claves["izquierda"]
    assert arbol.raiz.der.key == claves["derecha"]
    assert arbol.raiz.der.izq is None
    assert arbol.cantidad_nodos() == 6


test_eliminar_nodo_con_dos_hijos_usa_sucesor_inorden()
print("test eliminar nodo con dos hijos usa sucesor inorden: OK")


def test_eliminar_raiz_unica_deja_arbol_vacio():
    arbol = Bst()
    clave = Key(1, 4.5, 1)
    arbol.insertar(clave)

    arbol.eliminar(clave)

    assert arbol.raiz is None
    assert arbol.altura() == -1
    assert arbol.cantidad_nodos() == 0


test_eliminar_raiz_unica_deja_arbol_vacio()
print("test eliminar raiz unica deja arbol vacio: OK")


def test_eliminar_clave_inexistente_no_cambia_el_arbol():
    arbol, claves = crear_arbol_completo()
    altura_antes = arbol.altura()
    cantidad_antes = arbol.cantidad_nodos()

    arbol.eliminar(Key(9, 9.0, 9))

    assert arbol.raiz.key == claves["raiz"]
    assert arbol.altura() == altura_antes
    assert arbol.cantidad_nodos() == cantidad_antes


test_eliminar_clave_inexistente_no_cambia_el_arbol()
print("test eliminar clave inexistente no cambia el arbol: OK")


def test_eliminar_en_arbol_vacio_no_falla():
    arbol = Bst()

    arbol.eliminar(Key(1, 4.5, 1))

    assert arbol.raiz is None


test_eliminar_en_arbol_vacio_no_falla()
print("test eliminar en arbol vacio no falla: OK")


def test_recorrido_preorden():
    arbol, claves = crear_arbol_completo()

    resultado = arbol.preorden()

    esperado = [
        claves["raiz"],
        claves["izquierda"],
        claves["izquierda_izquierda"],
        claves["izquierda_derecha"],
        claves["derecha"],
        claves["derecha_izquierda"],
        claves["derecha_derecha"],
    ]
    assert resultado == esperado


test_recorrido_preorden()
print("test recorrido preorden: OK")


def test_recorrido_inorden():
    arbol, claves = crear_arbol_completo()

    resultado = arbol.inorden()

    esperado = [
        claves["izquierda_izquierda"],
        claves["izquierda"],
        claves["izquierda_derecha"],
        claves["raiz"],
        claves["derecha_izquierda"],
        claves["derecha"],
        claves["derecha_derecha"],
    ]
    assert resultado == esperado


test_recorrido_inorden()
print("test recorrido inorden: OK")


def test_recorrido_posorden():
    arbol, claves = crear_arbol_completo()

    resultado = arbol.posorden()

    esperado = [
        claves["izquierda_izquierda"],
        claves["izquierda_derecha"],
        claves["izquierda"],
        claves["derecha_izquierda"],
        claves["derecha_derecha"],
        claves["derecha"],
        claves["raiz"],
    ]
    assert resultado == esperado


test_recorrido_posorden()
print("test recorrido posorden: OK")


def test_recorridos_de_arbol_vacio():
    arbol = Bst()

    assert arbol.preorden() == []
    assert arbol.inorden() == []
    assert arbol.posorden() == []


test_recorridos_de_arbol_vacio()
print("test recorridos de arbol vacio: OK")


def test_profundidad_de_nodos():
    arbol, claves = crear_arbol_completo()

    assert arbol.profundidad(claves["raiz"]) == 0
    assert arbol.profundidad(claves["izquierda_derecha"]) == 2
    assert arbol.profundidad(claves["derecha_derecha"]) == 2


test_profundidad_de_nodos()
print("test profundidad de nodos: OK")


def test_profundidad_de_clave_inexistente_es_menos_uno():
    arbol, _ = crear_arbol_completo()

    assert arbol.profundidad(Key(9, 9.0, 9)) == -1


test_profundidad_de_clave_inexistente_es_menos_uno()
print("test profundidad de clave inexistente es menos uno: OK")


def test_profundidad_en_arbol_vacio_es_menos_uno():
    assert Bst().profundidad(Key(1, 4.5, 1)) == -1


test_profundidad_en_arbol_vacio_es_menos_uno()
print("test profundidad en arbol vacio es menos uno: OK")
