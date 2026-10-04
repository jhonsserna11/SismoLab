from src.logic.Escenario import Escenario
from datetime import datetime, timezone
from src.domain.Zona import Zona

import json
from copy import deepcopy
from decimal import Decimal
from src.domain.Estacion import Estacion

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
    for estacion in [Estacion("EST-1", "manizales"), Estacion("EST-2", "Medellin"), Estacion("EST-3", "Bogota"), Estacion("EST-4", "Armenia")]: escenario.estaciones.append(estacion)
    print(f"\n\n ----- estaciones : {escenario.estaciones}\n\n ----")

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

    assert nodo1["key"]["prioridad"] == 3
    assert nodo2["key"]["prioridad"] == 1
    assert nodo3["key"]["prioridad"] == 3

    # Insertion loading replaces the active catalog.
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

    # The AVL remains balanced.
    for nodo in avl["nodos"]:
        assert abs(nodo["factor"]) <= 1

    # The BST receives the same insertion order without rebalancing.
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

    # A rejected load must leave the scenario unchanged.
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

    assert len(avl["nodos"]) == 4
    assert len(bst["nodos"]) == 4

    assert avl["raiz"] is not None
    assert bst["raiz"] is not None

    # The BST receives the sorted keys without rebalancing.
    nodo_raiz_bst = next(
        nodo for nodo in bst["nodos"]
        if nodo["id"] == bst["raiz"]
    )

    assert nodo_raiz_bst["evento"]["magnitud"] == 1.0

    assert avl["altura"] >= 0
    assert avl["hojas"] >= 1

    profundidad_maxima_avl = avl["profundidad_maxima"]

    assert bst["altura"] == 3
    assert bst["hojas"] == 1

    profundidad_maxima_bst = bst["profundidad_maxima"]

    assert profundidad_maxima_bst == 3

    # The balanced AVL is shallower than this degenerate BST.
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

    # Deletion records the ID separately from archived events.
    nodo = escenario.avl.encontrarNodo(100)
    escenario.eliminacionIndividual(nodo.key)

    # Archiving preserves the full event in history.
    nodo = escenario.avl.encontrarNodo(90)
    escenario.archivarRama(nodo)

    assert 100 in escenario.eliminados
    assert len(escenario.historico) == 1

    escenario.cargarInserciones(obtenerDict("data/prueba_insercion.json"))

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


def test_cargar_topologia():
    print("-------------------------- test_cargar_topologia --------------------------\n")

    escenario = crear_escenario_con_zonas()

    resultado = escenario.cargarTopologia(
        obtenerDict("data/prueba_topologia.json")
    )

    avl = resultado["avl"]

    assert resultado["tipo"] == "topologia"
    assert avl["raiz"] == 2
    assert len(avl["nodos"]) == 3

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

    assert nodo2["izquierda"] == 1
    assert nodo2["derecha"] == 3

    assert nodo1["izquierda"] is None
    assert nodo1["derecha"] is None

    assert nodo3["izquierda"] is None
    assert nodo3["derecha"] is None

    assert nodo2["altura"] == 1
    assert nodo2["factor"] == 0

    assert escenario.avl.raiz is not None
    assert escenario.avl.raiz.key.id_key == 2

    assert escenario.avl.raiz.izq.key.id_key == 1
    assert escenario.avl.raiz.der.key.id_key == 3

    print("Topología cargada correctamente.")
    print("Raíz:", avl["raiz"])
    print("Altura:", avl["altura"])
test_cargar_topologia()
print("test cargar_topologia: OK")

def test_cargar_topologia_prioridad_incorrecta():
    print("-------------------------- test_cargar_topologia_prioridad_incorrecta --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["nodos"][0]["key"]["prioridad"] = 1

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por prioridad incorrecta."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_prioridad_incorrecta()
print("test cargar_topologia_prioridad_incorrecta: OK")


def test_cargar_topologia_referencia_inexistente():
    print("-------------------------- test_cargar_topologia_referencia_inexistente --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["nodos"][0]["izquierda"] = 99

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por referencia inexistente."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_referencia_inexistente()
print("test cargar_topologia_referencia_inexistente: OK")

def test_cargar_topologia_dos_padres():
    print("-------------------------- test_cargar_topologia_dos_padres --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["nodos"][2]["derecha"] = 1

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6
        
        assert False, "Se esperaba ValueError por nodo con dos padres."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_dos_padres()
print("test cargar_topologia_dos_padres: OK")

def test_cargar_topologia_nodo_desconectado():
    print("-------------------------- test_cargar_topologia_nodo_desconectado --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    nodo = deepcopy(datos["nodos"][1])

    nodo["id"] = 4
    nodo["key"]["id_key"] = 4
    nodo["evento"]["id"] = 4

    datos["nodos"].append(nodo)

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por nodo desconectado."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_nodo_desconectado()
print("test cargar_topologia_nodo_desconectado: OK")

def test_cargar_topologia_altura_incorrecta():
    print("-------------------------- test_cargar_topologia_altura_incorrecta --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["nodos"][0]["altura"] = 99

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por altura incorrecta."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_altura_incorrecta()
print("test cargar_topologia_altura_incorrecta: OK")

def test_cargar_topologia_factor_incorrecto():
    print("-------------------------- test_cargar_topologia_factor_incorrecto --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["nodos"][0]["factor"] = 99

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por factor incorrecto."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_factor_incorrecto()
print("test cargar_topologia_factor_incorrecto: OK")

def test_cargar_topologia_raiz_incorrecta():
    print("-------------------------- test_cargar_topologia_raiz_incorrecta --------------------------\n")

    escenario = crear_escenario_con_zonas()

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    escenario.crearEvento(1, 3.0, 100.0, 100.0, 304.6, datetime(2026, 9, 21, 11, 45, 32, tzinfo=timezone.utc), ["EST-4"])

    datos["raiz"] = 1

    try:
        escenario.cargarTopologia(datos)
        # A failed load must preserve the existing scenario.
        assert escenario.avl.raiz.key == 1
        assert escenario.avl.raiz.evento.zonax == 100.0
        assert escenario.avl.raiz.evento.zonay == 304.6

        assert False, "Se esperaba ValueError por raíz incorrecta."
    except ValueError as e:
        print("Error detectado correctamente:", e)
test_cargar_topologia_raiz_incorrecta()
print("test argar_topologia_raiz_incorrecta: OK")

def test_cargar_topologia_invalida_conserva_escenario():
    print("-------------------------- test_cargar_topologia_invalida_conserva_escenario --------------------------\n")

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

    datos = obtenerDict("data/prueba_topologia.json")
    datos = deepcopy(datos)

    datos["nodos"][0]["altura"] = 99

    try:
        escenario.cargarTopologia(datos)
        assert False, "Se esperaba ValueError."
    except ValueError:
        pass

    assert escenario.avl.raiz is raiz_antes
    assert escenario.avl.raiz is not None
test_cargar_topologia_invalida_conserva_escenario()
print("test cargar_topologia_invalida_conserva_escenario: OK")


def inicializarZonasyEstaciones(escenario:Escenario):
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
    for estacion in [Estacion("EST-1", "manizales"), Estacion("EST-2", "Medellin"), Estacion("EST-3", "Bogota"), Estacion("EST-4", "Armenia")]: escenario.estaciones.append(estacion)

def test_guardar_escenario():
    origenW = 24
    origenR = 80
    origenL = 5
    origenT = 120
    origenmodo_estres = True

    reloj = datetime(2026, 10, 1, 10, 54, 55, tzinfo=timezone.utc)

    escenario_origen = Escenario(origenW, origenR, origenL, origenT, reloj)
    escenario_origen.modo_estres = origenmodo_estres

    inicializarZonasyEstaciones(escenario_origen)

    datos = escenario_origen.guardarEscenario()

    assert datos["configuracion"]["W"] == 24
    assert datos["configuracion"]["R"] == 80
    assert datos["configuracion"]["L"] == 5
    assert datos["configuracion"]["T"] == 120
    assert datos["configuracion"]["modo_estres"] is True
    assert datos["configuracion"]["reloj"] == datetime(2026, 10, 1, 10, 54, 55, tzinfo=timezone.utc).isoformat()

    assert datos["avl"]["raiz"] == None
test_guardar_escenario()
print("test guardar_escenario: OK")

def test_cargar_escenario():
    escenario_origen = Escenario(
        24,
        80,
        5,
        120,
        datetime(2026, 10, 1, 10, 54, 55, tzinfo=timezone.utc)
    )
    escenario_origen.modo_estres = True
    inicializarZonasyEstaciones(escenario_origen)

    datos = escenario_origen.guardarEscenario()

    escenario_destino = Escenario(
        48,
        40,
        3,
        72,
        datetime(2026, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    )

    escenario_destino.cargarEscenario(datos)

    estado_cargado = escenario_destino.guardarEscenario()

    assert estado_cargado == datos
test_cargar_escenario()
print("test cargar_escenario: OK")


def test_cargar_escenario_invalido_conserva_escenario():
    escenario = Escenario(
        24,
        80,
        5,
        120,
        datetime(2026, 10, 1, 10, 54, 55, tzinfo=timezone.utc)
    )
    escenario.modo_estres = True
    inicializarZonasyEstaciones(escenario)

    estado_original = escenario.guardarEscenario()

    datos_invalidos = estado_original.copy()
    datos_invalidos["configuracion"] = datos_invalidos["configuracion"].copy()
    datos_invalidos["configuracion"]["W"] = -10

    try:
        escenario.cargarEscenario(datos_invalidos)
        assert False
    except ValueError:
        pass

    assert escenario.guardarEscenario() == estado_original
    assert len(escenario.pila_deshacer) == 0
test_cargar_escenario_invalido_conserva_escenario()
print("test cargar_escenario_invalido_conserva_escenario: OK")


def test_cargar_escenario_se_puede_deshacer():
    # Save the current state as A.
    escenario = Escenario(
        24,
        80,
        5,
        120,
        datetime(2026, 10, 1, 10, 54, 55, tzinfo=timezone.utc)
    )
    escenario.modo_estres = True
    inicializarZonasyEstaciones(escenario)

    estado_original = escenario.guardarEscenario()

    # Prepare a different state B to load.
    otro = Escenario(
        48,
        40,
        3,
        72,
        datetime(2026, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    )
    otro.modo_estres = False
    inicializarZonasyEstaciones(otro)

    datos_nuevo_estado = otro.guardarEscenario()

    print(datos_nuevo_estado)

    escenario.cargarEscenario(datos_nuevo_estado)

    assert escenario.guardarEscenario() == datos_nuevo_estado

    # Undo must restore state A exactly.
    assert escenario.deshacer() is True

    assert escenario.guardarEscenario() == estado_original
test_cargar_escenario_se_puede_deshacer()
print("test cargar_escenario_se_puede_deshacer: OK")


def crear_escenario_con_arboles():
    reloj = datetime(
        2026, 10, 1, 10, 0, 0,
        tzinfo=timezone.utc
    )

    escenario = Escenario(
        48,
        40,
        3,
        72,
        reloj
    )

    inicializarZonasyEstaciones(escenario)

    escenario.crearEvento(
        100,
        Decimal("5.0"),
        Decimal("20.0"),
        Decimal("100.0"),
        Decimal("100.0"),
        datetime(2026, 10, 1, 9, 0, 0, tzinfo=timezone.utc),
        ["EST-1"]
    )

    escenario.crearEvento(
        200,
        Decimal("6.0"),
        Decimal("30.0"),
        Decimal("600.0"),
        Decimal("600.0"),
        datetime(2026, 10, 1, 9, 10, 0, tzinfo=timezone.utc),
        ["EST-2"]
    )

    escenario.crearEvento(
        300,
        Decimal("4.0"),
        Decimal("50.0"),
        Decimal("200.0"),
        Decimal("700.0"),
        datetime(2026, 10, 1, 9, 20, 0, tzinfo=timezone.utc),
        ["EST-3"]
    )
    return escenario

def test_cargar_escenario_con_arboles():
    print("-------------------------- test_cargar_escenario_con_arboles --------------------------\n")

    escenario_origen = crear_escenario_con_arboles()

    datos = escenario_origen.guardarEscenario()

    escenario_destino = Escenario(
        10,
        10,
        1,
        10,
        datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    )

    escenario_destino.cargarEscenario(datos)

    assert escenario_destino.guardarEscenario() == datos
test_cargar_escenario_con_arboles()
print("test cargar_escenario_con_arboles: OK")


def test_cargar_escenario_estacion_inexistente():
    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    datos["avl"]["nodos"][0]["evento"]["estaciones"] = ["EST-999"]

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass

    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_estacion_inexistente()
print("test cargar_escenario_estacion_inexistente: OK")


def test_cargar_escenario_id_evento_inexistente():
    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    nodo = datos["avl"]["nodos"][0]
    nodo["izquierda"] = 999999

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass

    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_id_evento_inexistente()
print("test cargar_escenario_id_evento_inexistente: OK")


def test_cargar_escenario_altura_incorrecta():

    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    nodo = datos["avl"]["nodos"][0]
    nodo["altura"] += 1

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass

    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_altura_incorrecta()
print("test cargar_escenario_altura_incorrecta: OK")


def test_cargar_escenario_factor_incorrecto():

    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    nodo = datos["avl"]["nodos"][0]
    nodo["factor"] = 99

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass

    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_factor_incorrecto()
print("test cargar_escenario_factor_incorrecto: OK")


def test_cargar_escenario_clave_inconsistente():

    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    nodo = datos["avl"]["nodos"][0]
    nodo["key"]["id_key"] = 999999

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass

    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_clave_inconsistente()

print("test cargar_escenario_clave_inconsistente: OK")


def test_cargar_escenario_ciclo():

    escenario_origen = crear_escenario_con_arboles()
    datos = escenario_origen.guardarEscenario()

    raiz = datos["avl"]["raiz"]

    nodo_raiz = None

    for nodo in datos["avl"]["nodos"]:
        if nodo["id"] == raiz:
            nodo_raiz = nodo
            break

    assert nodo_raiz is not None

    nodo_raiz["izquierda"] = raiz

    escenario_destino = crear_escenario_con_arboles()
    estado_original = escenario_destino.guardarEscenario()

    try:
        escenario_destino.cargarEscenario(datos)
        assert False
    except ValueError:
        pass
    assert escenario_destino.guardarEscenario() == estado_original
test_cargar_escenario_ciclo()
print("test cargar_escenario_ciclo: OK")