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

    resultado = escenario.cargarInserciones(obtenerDict("data/prueba_insercion.json"))

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

    # La carga por inserciones reemplaza el catálogo activo.
    assert escenario.avl.raiz is not None
    assert escenario.bst.raiz is not None

    assert escenario.avl.raiz.key.id_key == avl["raiz"]
    assert escenario.bst.raiz.key.id_key == bst["raiz"]

    assert escenario.avl.peso() == 3
    assert escenario.bst.cantidad_nodos() == 3

    print("AVL cargado:", len(avl["nodos"]), "eventos")
    print("BST cargado:", len(bst["nodos"]), "eventos")
test_cargar_inserciones()
print("test cargar_inserciones: OK\n\n")


def test_cargar_inserciones_balancea_avl():

    print("-------------------------- test_cargar_inserciones_balancea_avl --------------------------\n")

    escenario = crear_escenario_con_zonas()

    resultado = escenario.cargarInserciones(obtenerDict("data/prueba_insercion_orden.json"))

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

    assert escenario.avl.raiz is not None
    assert escenario.bst.raiz is not None

    print("altura AVL:", avl["altura"])
    print("altura BST:", bst["altura"])
test_cargar_inserciones_balancea_avl()
print("test cargar_inserciones_balancea_avl: OK\n\n")


def test_cargar_inserciones_id_duplicado():

    print("-------------------------- test_cargar_inserciones_id_duplicado --------------------------\n")

    escenario = crear_escenario_con_zonas()
    escenario.crearEvento(
        99,
        5.0,
        20.0,
        100.0,
        300.0,
        datetime(2026, 9, 23, 10, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )
    raiz_antes = escenario.avl.raiz

    try:

        escenario.cargarInserciones(obtenerDict("data/prueba_insercion_duplicado.json"))

        assert False, "Se esperaba ValueError por ID duplicado."

    except ValueError as e:

        assert "identificador" in str(e).lower()
        print("Error detectado correctamente:", e)

    # La carga inválida no modifica el escenario.
    assert escenario.avl.raiz is raiz_antes
    assert escenario.avl.raiz is not None
test_cargar_inserciones_id_duplicado()
print("test cargar_inserciones_id_duplicado: OK\n\n")


def test_indicadores_carga_inserciones():
    print("-------------------------- test_indicadores_carga_inserciones --------------------------\n")

    escenario = crear_escenario_con_zonas()

    resultado = escenario.cargarInserciones(obtenerDict("data/prueba_insercion_orden.json"))

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

    assert escenario.avl.raiz is not None
    assert escenario.bst.raiz is not None

    assert avl["raiz"] is not None
    assert bst["raiz"] is not None

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


def test_deshacer_carga_inserciones():
    print("-------------------------- test_deshacer_carga_inserciones --------------------------\n")

    escenario = crear_escenario_con_zonas()

    escenario.crearEvento(
        99,
        5.0,
        20.0,
        100.0,
        300.0,
        datetime(2026, 9, 23, 10, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )
    escenario.crearEvento(
        100,
        5.0,
        20.0,
        100.0,
        300.0,
        datetime(2026, 9, 23, 10, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )
    escenario.crearEvento(
        90,
        5.0,
        20.0,
        100.0,
        300.0,
        datetime(2026, 9, 23, 10, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )

    raiz_antes = escenario.avl.raiz.key.id_key

    # Eliminar un evento: su ID queda en eliminados.
    nodo = escenario.avl.encontrarNodo(100)
    escenario.eliminacionIndividual(nodo.key)

    # Archivar el otro evento: pasa a historico.
    nodo = escenario.avl.encontrarNodo(90)
    escenario.archivarRama(nodo)

    assert 100 in escenario.eliminados
    assert len(escenario.historico) == 1
    escenario.cargarInserciones(
        obtenerDict("data/prueba_insercion.json")
    )

    assert escenario.avl.raiz.key.id_key != raiz_antes
    assert escenario.avl.raiz.key.id_key == 1

    assert escenario.historico == []
    assert escenario.eliminados == set()

    resultado = escenario.deshacer()

    assert resultado is True
    assert escenario.avl.raiz.key.id_key == raiz_antes
    assert 100 in escenario.eliminados
    assert len(escenario.historico) == 1
    print("Catálogo anterior restaurado correctamente.")
test_deshacer_carga_inserciones()
print("test deshacer_carga_inserciones: OK")