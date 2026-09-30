from src.logic.Persistencia import Persistencia
from src.logic.Escenario import Escenario
from datetime import datetime, timezone
from src.domain.Zona import Zona
import json

def obtenerDict(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos

def crear_escenario():
    reloj = datetime(
        2026, 9, 23, 12, 0, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        48,
        40,
        3,
        72,
        reloj
    )

    return escenario

def crear_escenario_con_zonas():
    escenario = crear_escenario()

    zona1 = Zona(
        1,
        "Zona poblada",
        0.0,
        500.0,
        0.0,
        500.0,
        True
    )
    zona2 = Zona(
            2,
            "Zona poblada",
            501.0,
            1000.0,
            501.0,
            1000.0,
            True
        )
    zona3 = Zona(
            3,
            "Zona no poblada",
            0.0,
            500.0,
            501.0,
            1000.0,
            True
        )
    zona4 = Zona(
            4,
            "Zona no poblada",
            501.0,
            1000.0,
            0.0,
            500.0,
            True
        )

    for zona in [zona1, zona2, zona3, zona4]: escenario.zonas.append(zona) 

    return escenario

def test_cargar_inserciones():

    print("-------------------------- test_cargar_inserciones --------------------------\n")

    escenario = crear_escenario_con_zonas()
    persistencia = Persistencia()

    resultado = persistencia.cargarInserciones(
        obtenerDict("data/prueba_insercion.json"),
        escenario.zonas
    )

    avl = resultado["avl"]
    bst = resultado["bst"]

    print("\nRESULTADO AVL:")
    print(avl)

    print("\nRESULTADO BST:")
    print(bst)

    assert avl["raiz"] is not None
    assert bst["raiz"] is not None

    assert resultado["tipo"] == "inserciones"

    assert avl["altura"] >= 0
    assert bst["altura"] >= 0

    assert len(avl["nodos"]) == 3
    assert len(bst["nodos"]) == 3

    nodo1 = next(
        nodo for nodo in avl["nodos"]
        if nodo["id"] == 1
    )

    nodo2 = next(
        nodo for nodo in avl["nodos"]
        if nodo["id"] == 2
    )

    nodo3 = next(
        nodo for nodo in avl["nodos"]
        if nodo["id"] == 3
    )

    assert nodo1["evento"]["magnitud"] == 5.0
    assert nodo2["evento"]["magnitud"] == 4.1
    assert nodo3["evento"]["magnitud"] == 6.0

    assert nodo1["prioridad"] == 3
    assert nodo2["prioridad"] == 1
    assert nodo3["prioridad"] == 3

    # La carga por inserciones NO modifica el escenario actual.
    assert escenario.avl.raiz is None
    assert escenario.bst.raiz is None

    print("AVL cargado:", len(avl["nodos"]), "eventos")
    print("BST cargado:", len(bst["nodos"]), "eventos")
test_cargar_inserciones()
print("test cargar_inserciones: OK\n\n")


def test_cargar_inserciones_balancea_avl():

    print("-------------------------- test_cargar_inserciones_balancea_avl --------------------------\n")

    escenario = crear_escenario_con_zonas()
    persistencia = Persistencia()

    resultado = persistencia.cargarInserciones(
        obtenerDict("data/prueba_insercion_orden.json"),
        escenario.zonas
    )

    avl = resultado["avl"]
    bst = resultado["bst"]

    assert len(avl["nodos"]) == 4
    assert len(bst["nodos"]) == 4

    # El AVL debe permanecer balanceado.
    for nodo in avl["nodos"]:
        assert abs(nodo["factor"]) <= 1

    # El BST recibe el mismo orden pero no se balancea.
    nodo1 = next(nodo for nodo in bst["nodos"] if nodo["id"] == 1)
    nodo2 = next(nodo for nodo in bst["nodos"] if nodo["id"] == 2)
    nodo3 = next(nodo for nodo in bst["nodos"] if nodo["id"] == 3)
    nodo4 = next(nodo for nodo in bst["nodos"] if nodo["id"] == 4)

    assert bst["raiz"] == 1

    assert nodo1["evento"]["magnitud"] == 1.0
    assert nodo1["derecha"] == 2

    assert nodo2["evento"]["magnitud"] == 2.0
    assert nodo2["derecha"] == 3

    assert nodo3["evento"]["magnitud"] == 3.0
    assert nodo3["derecha"] == 4

    assert nodo4["evento"]["magnitud"] == 4.0
    assert nodo4["derecha"] is None

    assert bst["altura"] == 3

    print("altura AVL:", avl["altura"])
    print("altura BST:", bst["altura"])
test_cargar_inserciones_balancea_avl()
print("test cargar_inserciones_balancea_avl: OK\n\n")


def test_cargar_inserciones_id_duplicado():

    print("-------------------------- test_cargar_inserciones_id_duplicado --------------------------\n")

    escenario = crear_escenario_con_zonas()
    persistencia = Persistencia()

    try:

        persistencia.cargarInserciones(
            obtenerDict("data/prueba_insercion_duplicado.json"),
            escenario.zonas
        )

        assert False, "Se esperaba ValueError por ID duplicado."

    except ValueError as e:

        assert "identificador" in str(e).lower()
        print("Error detectado correctamente:", e)
test_cargar_inserciones_id_duplicado()
print("test cargar_inserciones_id_duplicado: OK\n\n")


def test_indicadores_carga_inserciones():
    print("-------------------------- test_indicadores_carga_inserciones --------------------------\n")

    escenario = crear_escenario_con_zonas()
    persistencia = Persistencia()

    resultado = persistencia.cargarInserciones(
        obtenerDict("data/prueba_insercion_orden.json"),
        escenario.zonas
    )

    avl = resultado["avl"]
    bst = resultado["bst"]

    # Ambos tienen los mismos eventos.
    assert len(avl["nodos"]) == 4
    assert len(bst["nodos"]) == 4

    # Ambos tienen raíz.
    assert avl["raiz"] is not None
    assert bst["raiz"] is not None

    # El BST recibe 1 -> 2 -> 3 -> 4 sin balancear.
    nodo_raiz_bst = next(
        nodo for nodo in bst["nodos"]
        if nodo["id"] == bst["raiz"]
    )

    assert nodo_raiz_bst["evento"]["magnitud"] == 1.0

    # Indicadores del AVL.
    assert avl["altura"] >= 0
    assert avl["hojas"] >= 1

    profundidad_maxima_avl = max(
        nodo["profundidad"]
        for nodo in avl["nodos"]
    )

    # Indicadores del BST.
    assert bst["altura"] == 3
    assert bst["hojas"] == 1

    profundidad_maxima_bst = max(
        nodo["profundidad"]
        for nodo in bst["nodos"]
    )

    assert profundidad_maxima_bst == 3

    # El AVL, al estar balanceado, debe tener menor profundidad máxima
    # que este BST degenerado.
    assert profundidad_maxima_avl < profundidad_maxima_bst

    print("AVL")
    print("  raíz:", avl["raiz"])
    print("  altura:", avl["altura"])
    print("  profundidad máxima:", profundidad_maxima_avl)
    print("  hojas:", avl["hojas"])

    print("\nBST")
    print("  raíz:", bst["raiz"])
    print("  altura:", bst["altura"])
    print("  profundidad máxima:", profundidad_maxima_bst)
    print("  hojas:", bst["hojas"])
test_indicadores_carga_inserciones()
print("\ntest indicadores_carga_inserciones: OK\n\n")