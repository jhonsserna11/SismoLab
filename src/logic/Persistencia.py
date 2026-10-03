from datetime import datetime, timezone

from src.domain.Evento import Evento
from src.domain.Zona import Zona
from src.domain.Estacion import Estacion
from src.domain.Reporte import Reporte

from src.structures.Avl import Avl
from src.structures.Bst import Bst

from src.structures.Nodo import Key, Nodo

from decimal import Decimal
from collections import deque

import json
from pathlib import Path

class Persistencia:

    def cargarInserciones(self, datos, zonas, estaciones):
        if not isinstance(datos, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")

        if datos.get("tipo_carga") != "inserciones":
            raise ValueError(
                "El archivo no corresponde a una carga por inserciones."
            )

        eventos = datos.get("eventos")

        if not isinstance(eventos, list):
            raise ValueError(
                "El campo 'eventos' debe ser una lista."
            )

        avl = Avl()
        bst = Bst()
        ids = set()
        ids_estaciones = {estacion.id_estacion for estacion in estaciones}

        for datos_evento in eventos:

            if not isinstance(datos_evento, dict):
                raise ValueError(
                    "Cada elemento de 'eventos' debe ser un objeto."
                )
            campos_obligatorios = {
                "id",
                "magnitud",
                "profundidad",
                "zonax",
                "zonay",
                "fechaHora",
                "revision",
                "estaciones"
            }

            faltantes = campos_obligatorios - datos_evento.keys()

            if faltantes:
                raise ValueError(f"Faltan campos obligatorios: {sorted(faltantes)}")

            id_evento = datos_evento.get("id")

            if id_evento in ids:
                raise ValueError(f"El identificador {id_evento} está repetido.")

            ids.add(id_evento)

            fecha = self._fechaDesdeJson(datos_evento.get("fechaHora"))

            estaciones_evento = datos_evento.get("estaciones")

            if not isinstance(estaciones_evento, list):
                raise ValueError(f"Las estaciones del evento {id_evento} deben ser una lista.")

            for id_estacion in estaciones_evento:
                if type(id_estacion) is not str or not id_estacion.strip():
                    raise ValueError(f"La referencia de estación del evento {id_evento} no es válida.")
                if id_estacion not in ids_estaciones:
                    raise ValueError(f"La estación {id_estacion} asociada al evento {id_evento} no existe.")

            evento = Evento(
                id_evento,
                datos_evento.get("magnitud"),
                datos_evento.get("profundidad"),
                datos_evento.get("zonax"),
                datos_evento.get("zonay"),
                fecha,
                datos_evento.get("revision"),
                datos_evento.get("estaciones")
            )

            poblada = self._esPoblada(
                zonas,
                evento.zonax,
                evento.zonay
            )

            prioridad = evento.calcularPrioridad(poblada)

            key = Key(
                prioridad,
                evento.magnitud,
                evento.id
            )

            # La carga por inserciones exige AVL balanceado.
            avl.insertar(key, evento, False)

            # BST sin balanceo.
            bst.insertar(key, evento)

        return {
            "tipo": "inserciones",
            "avl": avl,
            "bst": bst
        }

    def _esPoblada(self, zonas, zonax, zonay):
        for zona in zonas:
            if zona.contiene(zonax, zonay) and zona.es_poblada():
                return True

        return False

    def _serializarArbol(self, arbol):
        arbol.altura()
        nodos = []
        profundidad_maxima = -1

        def recorrer(nodo, profundidad):
            if nodo is None:
                return

            nonlocal profundidad_maxima
            profundidad_maxima = max(profundidad_maxima, profundidad)

            datos = {
                "id": nodo.key.id_key,
                "key": {
                    "prioridad": nodo.key.prioridad,
                    "magnitud": float(nodo.evento.magnitud),
                    "id_key": nodo.key.id_key
                },
                "evento": {
                    "id": nodo.evento.id,
                    "magnitud": float(nodo.evento.magnitud),
                    "profundidad": float(nodo.evento.profundidad),
                    "zonax": float(nodo.evento.zonax),
                    "zonay": float(nodo.evento.zonay),
                    "fechaHora": nodo.evento.fechaHora.isoformat(),
                    "revision": nodo.evento.revision,
                    "estaciones": nodo.evento.estaciones,
                    "estado": nodo.evento.estado
                },
                "altura": nodo.altura,
                "izquierda": (
                    nodo.izq.key.id_key
                    if nodo.izq is not None
                    else None
                ),
                "derecha": (
                    nodo.der.key.id_key
                    if nodo.der is not None
                    else None
                )
            }

            if type(arbol) is Avl:
                datos["factor"] = ((nodo.izq.altura if nodo.izq is not None else -1) - (nodo.der.altura if nodo.der is not None else -1))

            nodos.append(datos)

            recorrer(nodo.izq, profundidad + 1)
            recorrer(nodo.der, profundidad + 1)

        recorrer(arbol.raiz, 0)

        return {
            "raiz": (
                arbol.raiz.key.id_key
                if arbol.raiz is not None
                else None
            ),
            "altura": arbol.altura(),
            "profundidad_maxima": profundidad_maxima,
            "hojas": arbol.hojas(),
            "nodos": nodos
        }
    
    def _fechaDesdeJson(self, valor):
        if not isinstance(valor, str):
            raise ValueError("La fecha debe ser una cadena.")

        try:
            if valor.endswith("Z"):
                valor = valor[:-1] + "+00:00"

            fecha = datetime.fromisoformat(valor)

        except ValueError:
            raise ValueError("La fecha no tiene un formato ISO 8601 válido.")

        if fecha.tzinfo is None:
            raise ValueError("La fecha debe incluir zona horaria.")

        return fecha.astimezone(timezone.utc)

    def _fechaDesdeJsonReloj(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El parametro reloj no es valido.")

        try:
            if valor.endswith("Z"):
                valor = valor[:-1] + "+00:00"

            fecha = datetime.fromisoformat(valor)

        except ValueError:
            raise ValueError("El parametro reloj no tiene un formato ISO 8601 válido.")

        if fecha.tzinfo is None:
            raise ValueError("El parametro reloj debe incluir zona horaria.")

        return fecha.astimezone(timezone.utc)



    def cargarTopologia(self, datos, zonas, estaciones):
        if not isinstance(datos, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")
        campos_datos = {"tipo_carga", "raiz", "nodos"}
        if set(datos.keys()) != campos_datos:
            raise ValueError("El archivo debe tener las claves 'raiz' y 'nodos'.")
        if datos.get("tipo_carga") != "topologia":
            raise ValueError("El archivo no corresponde a una carga por topología.")
        
        nodos_datos = datos.get("nodos")

        if not isinstance(nodos_datos, list):
            raise ValueError("El campo 'nodos' debe ser una lista.")

        raiz_id = datos.get("raiz")
        if raiz_id is not None:
            if type(raiz_id) is not int or raiz_id <= 0:
                raise ValueError("El parametro raiz debe ser entero positivo")
        nodos = {}
        ids = set()

        ids_estaciones = {estacion.id_estacion for estacion in estaciones}
        for datos_nodo in nodos_datos:   
            self._validarNodo(datos_nodo, ids, nodos, zonas, ids_estaciones)

        self._conectarNodos(nodos_datos, nodos)
        self._validarConectividad(nodos, raiz_id)
        self._validarOrdenGlobal(nodos, raiz_id)
        balanceado = self._validarAlturasYFactores(nodos, nodos_datos, raiz_id)
        nuevo_avl = Avl()

        if raiz_id is not None:
            nuevo_avl.raiz = nodos[raiz_id]
        return {
            "tipo": "topologia",
            "balanceado": balanceado,
            "avl": nuevo_avl
        }


    def _validarNodo(self, datos_nodo, ids: set, nodos: dict, zonas, ids_estaciones=None):
        if not isinstance(datos_nodo, dict):
            raise ValueError("Cada elemento de 'nodos' debe ser un objeto.")

        datos_key = datos_nodo.get("key")

        if not isinstance(datos_key, dict):
            raise ValueError("El nodo debe contener una key válida.")

        campos_key = {"prioridad", "magnitud", "id_key"}

        faltantes = campos_key - datos_key.keys()

        if faltantes:
            raise ValueError(f"Faltan campos de la key: {sorted(faltantes)}")

        id_nodo = datos_key.get("id_key")

        if id_nodo in ids:
            raise ValueError(f"El identificador {id_nodo} está repetido.")

        ids.add(id_nodo)

        datos_evento = datos_nodo.get("evento")
        if not isinstance(datos_evento, dict):
            raise ValueError(f"El nodo {id_nodo} debe contener un evento válido.")

        campos_evento = {
            "id",
            "magnitud",
            "profundidad",
            "zonax",
            "zonay",
            "fechaHora",
            "revision",
            "estaciones",
            "estado"
        }

        faltantes = campos_evento - datos_evento.keys()

        if faltantes:
            raise ValueError(f"Faltan campos del evento {id_nodo}: {sorted(faltantes)}")

        if datos_evento.get("id") != datos_key.get("id_key"):
            raise ValueError(f"El id_key {datos_key.get('id_key')} no coincide con el ID del evento.")

        estaciones_evento = datos_evento.get("estaciones")
        if not isinstance(estaciones_evento, list):
            raise ValueError(f"Las estaciones del evento {id_nodo} deben ser una lista.")

        for id_estacion in estaciones_evento:
            if type(id_estacion) is not str or not id_estacion.strip():
                raise ValueError(f"La referencia de estación del evento {id_nodo} no es válida.")

            if ids_estaciones is not None and id_estacion not in ids_estaciones:
                raise ValueError(f"La estación {id_estacion} asociada al evento {id_nodo} no existe.")

        fecha = self._fechaDesdeJson(
            datos_evento.get("fechaHora")
        )

        evento = Evento(
            datos_evento.get("id"),
            datos_evento.get("magnitud"),
            datos_evento.get("profundidad"),
            datos_evento.get("zonax"),
            datos_evento.get("zonay"),
            fecha,
            datos_evento.get("revision"),
            datos_evento.get("estaciones")
        )

        evento.estado = datos_evento.get("estado")

        poblada = self._esPoblada(
            zonas,
            evento.zonax,
            evento.zonay
        )

        prioridad_calculada = evento.calcularPrioridad(poblada)

        prioridad_guardada = datos_key.get("prioridad")

        if prioridad_guardada != prioridad_calculada:
            raise ValueError(f"La prioridad del nodo {id_nodo} no coincide con la prioridad calculada.")

        magnitud_guardada = Decimal(str(datos_key.get("magnitud")))

        if magnitud_guardada != evento.magnitud:
            raise ValueError(f"La magnitud de la key del nodo {id_nodo} no coincide con la del evento.")

        key = Key(
            prioridad_guardada,
            magnitud_guardada,
            datos_key.get("id_key")
        )

        nodo = Nodo(key, evento)
        nodos[id_nodo] = nodo

    def _conectarNodos(self, nodos_datos: list, nodos: dict):
        nodos_con_padre = set()

        for datos_nodo in nodos_datos:

            id_nodo = datos_nodo["key"]["id_key"]
            nodo = nodos[id_nodo]

            id_izquierda = datos_nodo.get("izquierda")
            id_derecha = datos_nodo.get("derecha")

            if id_izquierda is not None:

                if id_izquierda not in nodos:
                    raise ValueError(f"El hijo izquierdo del nodo {id_nodo} referencia un nodo inexistente: {id_izquierda}.")

                if id_izquierda in nodos_con_padre:
                    raise ValueError(f"El nodo {id_izquierda} tiene más de un padre.")

                nodos_con_padre.add(id_izquierda)
                nodo.izq = nodos[id_izquierda]

            if id_derecha is not None:

                if id_derecha not in nodos:
                    raise ValueError(f"El hijo derecho del nodo {id_nodo} referencia un nodo inexistente: {id_derecha}.")

                if id_derecha in nodos_con_padre:
                    raise ValueError(f"El nodo {id_derecha} tiene más de un padre.")

                nodos_con_padre.add(id_derecha)
                nodo.der = nodos[id_derecha]

    def _validarConectividad(self, nodos: dict, raiz_id):

        if not nodos:
            if raiz_id is not None:
                raise ValueError("Se indicó una raíz para un árbol sin nodos.")
            return

        if raiz_id not in nodos:
            raise ValueError(f"La raíz {raiz_id} no existe entre los nodos.")

        hijos = set()

        for nodo in nodos.values():

            if nodo.izq is not None:
                hijos.add(nodo.izq.key.id_key)

            if nodo.der is not None:
                hijos.add(nodo.der.key.id_key)

        raices = set(nodos.keys()) - hijos

        if len(raices) != 1:
            raise ValueError(f"La topología debe tener una única raíz. Raíces encontradas: {sorted(raices)}.")

        raiz_real = next(iter(raices))

        if raiz_real != raiz_id:
            raise ValueError(f"La raíz indicada ({raiz_id}) no coincide con la raíz real ({raiz_real}).")

        visitados = set()
        pendientes = [nodos[raiz_id]]

        while pendientes:

            nodo = pendientes.pop()

            id_nodo = nodo.key.id_key

            if id_nodo in visitados:
                raise ValueError(f"La topología contiene un ciclo que involucra al nodo {id_nodo}.")

            visitados.add(id_nodo)

            if nodo.izq is not None:
                pendientes.append(nodo.izq)

            if nodo.der is not None:
                pendientes.append(nodo.der)

        if visitados != set(nodos.keys()):
            desconectados = set(nodos.keys()) - visitados
            raise ValueError(f"Existen nodos desconectados de la raíz: {sorted(desconectados)}.")

    def _validarOrdenGlobal(self, nodos: dict, raiz_id):
        def _validar(nodo, limite_inferior, limite_superior):

            if nodo is None:
                return

            clave = nodo.key

            if limite_inferior is not None and not limite_inferior < clave:
                raise ValueError(f"La clave del nodo {clave.id_key} no cumple el límite inferior global.")

            if limite_superior is not None and not clave < limite_superior:
                raise ValueError(f"La clave del nodo {clave.id_key} no cumple el límite superior global.")

            _validar(nodo.izq, limite_inferior, clave)

            _validar(nodo.der, clave, limite_superior)

        if raiz_id is not None:
            _validar(nodos[raiz_id], None, None)

    def _validarAlturasYFactores( self, nodos: dict, nodos_datos: list, raiz_id):
        datos_por_id = {}

        for datos_nodo in nodos_datos:

            id_nodo = datos_nodo["key"]["id_key"]

            if "altura" not in datos_nodo:
                raise ValueError(f"El nodo {id_nodo} no contiene altura.")

            if "factor" not in datos_nodo:
                raise ValueError(f"El nodo {id_nodo} no contiene factor.")

            datos_por_id[id_nodo] = {
                "altura": datos_nodo["altura"],
                "factor": datos_nodo["factor"]
            }
        balanceado = True
        def _calcular(nodo):

            if nodo is None:
                # entrega -1 porque es hoja y sus hijos none le retornan -1, para que la altura calculada de la hoja sea 0 (-1 -(-1) = 0)
                # entrega True porque si esta vacio esta balanceado y si es una hoja supone que desde la hoja es balanceado y se manda el True al escenario superior de la pila de recursion
                return -1, True

            altura_izquierda, balanceado_izquierda = _calcular(nodo.izq)
            altura_derecha, balanceado_derecha = _calcular(nodo.der)

            altura_calculada = 1 + max(
                altura_izquierda,
                altura_derecha
            )

            factor_calculado = (altura_izquierda - altura_derecha)

            id_nodo = nodo.key.id_key
            datos_nodo = datos_por_id[id_nodo]

            if datos_nodo["altura"] != altura_calculada:
                raise ValueError(
                    f"La altura del nodo {id_nodo} no coincide. "
                    f"Guardada: {datos_nodo['altura']}, "
                    f"calculada: {altura_calculada}."
                )
            nodo.altura = altura_calculada

            if datos_nodo["factor"] != factor_calculado:
                raise ValueError(
                    f"El factor del nodo {id_nodo} no coincide. "
                    f"Guardado: {datos_nodo['factor']}, "
                    f"calculado: {factor_calculado}."
                )

            balanceado = (balanceado_izquierda and balanceado_derecha and -1 <= factor_calculado <= 1)

            return altura_calculada, balanceado

        if raiz_id is not None:
            altura_calculada, balanceado = _calcular(nodos[raiz_id])  
            return balanceado
        return True


    def _serializarEvento(self, evento):
        return {
            "id": evento.id,
            "magnitud": float(evento.magnitud),
            "profundidad": float(evento.profundidad),
            "zonax": float(evento.zonax),
            "zonay": float(evento.zonay),
            "fechaHora": evento.fechaHora.isoformat(),
            "revision": evento.revision,
            "estaciones": evento.estaciones,
            "estado": evento.estado
        }

    def _serializarEstacion(self, estacion):
        return {
            "id_estacion": estacion.id_estacion,
            "nombre": estacion.nombre
        }

    def _serializarReporte(self, reporte):
        return {
            "id_evento": reporte.id_evento,
            "nRevision": reporte.nRevision,
            "magnitud": float(reporte.magnitud),
            "profundidad": float(reporte.profundidad),
            "zonax": float(reporte.zonax),
            "zonay": float(reporte.zonay),
            "fecha": reporte.fecha.isoformat(),
            "estacion": reporte.estacion
        }

    def _serializarColaReportes(self, cola):
        return [
            self._serializarReporte(reporte)
            for reporte in cola
        ]
    
    def guardarEscenario(self, escenario):
        return {
            "tipo_carga": "escenario",
            "configuracion": {
                "W": escenario.W,
                "R": escenario.R,
                "L": escenario.L,
                "T": escenario.T,
                "modo_estres": escenario.modo_estres,
                "reloj": escenario.reloj.isoformat()
            },
            "avl": self._serializarArbol(escenario.avl),
            "bst": self._serializarArbol(escenario.bst),
            "historico": [
                self._serializarEvento(evento)
                for evento in escenario.historico
            ],
            "eliminados": list(escenario.eliminados),
            "estaciones": [
                self._serializarEstacion(estacion)
                for estacion in escenario.estaciones
            ],
            "zonas": [
                zona.obtener_datos()
                for zona in escenario.zonas
            ],
            "cola_reportes": self._serializarColaReportes(
                escenario.cola_reportes
            ),
            "metricas": {
                "escenario": escenario.metricas.copy(),
                "avl": escenario.avl.metricas.copy()
            }
        }

    def cargarEscenario(self, datos):
        # Validacion general JSON
        if not isinstance(datos, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")

        if datos.get("tipo_carga") != "escenario":
            raise ValueError("El archivo no corresponde a una carga por topología.")
        resultado = self._cargarEscenario(datos)
        return resultado

    def _cargarEscenario(self, datos):
        # Validacion clave Configuracion
        configuracion = datos.get("configuracion")

        if not isinstance(configuracion, dict):
            raise ValueError("El archivo debe contener los parametros de configuración (W - R - L - T - (modo_estres)bool - reloj")

        campos_configuracion = {"W", "R", "L", "T", "modo_estres", "reloj"}

        if set(configuracion.keys()) != campos_configuracion:
            raise ValueError("El archivo no contiene todos los parametros de configuración necesarios")

        w = configuracion["W"]
        r = configuracion["R"]
        l = configuracion["L"]
        t = configuracion["T"]
        modo_estres = configuracion["modo_estres"]
        reloj = configuracion["reloj"]
        
        if not type(w) is int or w <= 0:
            raise ValueError("El parametro W no es válido - debe ser entero positivo.")
        if not type(r) is int or r <= 0:
            raise ValueError("El parametro R no es válido - debe ser entero positivo.")
        if not type(l) is int or l <= 0:
            raise ValueError("El parametro L no es válido - debe ser entero positivo.")
        if not type(t) is int or t <= 0:
            raise ValueError("El parametro T no es válido - debe ser entero positivo.")
        if not type(modo_estres) is bool:
            raise ValueError("El parametro modo_estres no es válido - debe ser booleano ( True -> modo_estres activado - False -> modo_estres desactivado (modo normal) )")
        reloj = self._fechaDesdeJsonReloj(reloj)

        # Validacion inicial arboles
        datos_avl = datos.get("avl")
        datos_bst = datos.get("bst")

        if not isinstance(datos_avl, dict):
            raise ValueError("El campo 'avl' debe ser un objeto.")
        if not isinstance(datos_bst, dict):
            raise ValueError("El campo 'bst' debe ser un objeto.")

        campos_arbol = {"raiz", "altura", "profundidad_maxima", "hojas", "nodos"}
        if set(datos_avl.keys()) != campos_arbol:
            raise ValueError("El arbol AVL deben tener todos sus datos: id de la raiz, altura del arbol, profundidad maxima, cantidad hojas, lista de nodos")
        
        if set(datos_bst.keys()) != campos_arbol:
            raise ValueError("El arbol BST deben tener todos sus datos: id de la raiz, altura del arbol, profundidad maxima, cantidad de hojas y lista de nodos")
            
        # Validacion de clave Zonas
        zonas_datos = datos.get("zonas")
        if not isinstance(zonas_datos, list):
            raise ValueError("El campo 'zonas' debe ser una lista.")

        zonas_temporales = []
        for datos_zona in zonas_datos:
            if not isinstance(datos_zona, dict):
                raise ValueError("Cada elemento de 'zonas' debe ser un objeto.")

            campos_zona = {"id_zona", "nombre", "x_min", "x_max", "y_min", "y_max", "poblada"}
            if set(datos_zona.keys()) != campos_zona:
                raise ValueError("Las zonas deben tener todos sus datos: id, nombre, sus limites en X y en Y, señal poblada en True o false dependiendo el caso")

            id_zona = datos_zona["id_zona"]
            nombre_zona = datos_zona["nombre"]
            x_min = datos_zona["x_min"]
            x_max = datos_zona["x_max"]
            y_min = datos_zona["y_min"]
            y_max = datos_zona["y_max"]
            
            poblada = datos_zona["poblada"]
            if not isinstance(poblada, bool):
                raise ValueError(f"La propiedad 'poblada' de la zona {id_zona} debe ser booleana.")

            zona = Zona(id_zona, nombre_zona, x_min, x_max, y_min, y_max, poblada)
            zonas_temporales.append(zona)

        raiz_avl = datos_avl.get("raiz")
        if raiz_avl is not None:
            if type(raiz_avl) is not int or raiz_avl <= 0:
                    raise ValueError("El parametro 'raiz' del AVL debe ser entero positivo.")
        nodosAvl = {}
        ids_avl = set()

        raiz_bst = datos_bst.get("raiz")
        if raiz_bst is not None:
            if type(raiz_bst) is not int or raiz_bst <= 0:
                raise ValueError("El parametro 'raiz' del BST debe ser entero positivo.")
        nodosBst = {}
        ids_bst = set()

        nodos_datos_avl = datos_avl["nodos"]
        if not isinstance(nodos_datos_avl, list):
            raise ValueError("El campo 'nodos' del árbol AVL debe ser una lista de nodos.")

        for nodo_avl in nodos_datos_avl:
            # Validar cada nodo
            self._validarNodo(nodo_avl, ids_avl, nodosAvl, zonas_temporales)

        # realizar conexiones entre los nodos
        self._conectarNodos(nodos_datos_avl, nodosAvl)
        # validar conexiones del arbol
        self._validarConectividad(nodosAvl, raiz_avl)
        # validar topologia y orden del arbol
        self._validarOrdenGlobal(nodosAvl, raiz_avl)
        # Valida alturas y factores - dice si el arbol está balanceado o no
        balanceado_avl = self._validarAlturasYFactores(nodosAvl, nodos_datos_avl, raiz_avl)

        # crea objeto Avl y referencia la raiz
        nuevo_avl = Avl()
        if raiz_avl is not None:
            nuevo_avl.raiz = nodosAvl[raiz_avl]

        # valida parametros generales calculados del AVL con los ingresados en JSON
        if datos_avl["altura"] != nuevo_avl.altura():
            raise ValueError("La altura del AVL no coincide con la altura calculada.")

        if datos_avl["profundidad_maxima"] != self._profundidadMaxima(nuevo_avl):
            raise ValueError("La profundidad máxima del AVL no coincide con la calculada.")

        if datos_avl["hojas"] != nuevo_avl.hojas():
            raise ValueError("La cantidad de hojas del AVL no coincide con la calculada.")


        nodos_datos_bst = datos_bst["nodos"]
        if not isinstance(nodos_datos_bst, list):
            raise ValueError("El campo 'nodos' del árbol BST debe ser una lista de nodos.")

        for nodo_bst in nodos_datos_bst:
            #valida cada nodo
            self._validarNodo(nodo_bst, ids_bst, nodosBst, zonas_temporales)

        # realiza conexiones entre nodos
        self._conectarNodos(nodos_datos_bst, nodosBst)
        # validar conexiones del arbol
        self._validarConectividad(nodosBst, raiz_bst)
        # validar topologia y orden del arbol
        self._validarOrdenGlobal(nodosBst, raiz_bst)

        #validar alturas de los nodos del arbol BST
        self._validarAlturasBST(nodosBst, nodos_datos_bst, raiz_bst)

        #crea objeto Bst y añade la raiz
        nuevo_bst = Bst()
        if raiz_bst is not None:
            nuevo_bst.raiz = nodosBst[raiz_bst]

        # valida parametros generales calculados del BST con los ingresados en JSON
        if datos_bst["altura"] != nuevo_bst.altura():
            raise ValueError(
                "La altura del BST no coincide con la altura calculada."
            )

        if datos_bst["profundidad_maxima"] != self._profundidadMaxima(nuevo_bst):
            raise ValueError(
                "La profundidad máxima del BST no coincide con la calculada."
            )

        if datos_bst["hojas"] != nuevo_bst.hojas():
            raise ValueError(
                "La cantidad de hojas del BST no coincide con la calculada."
            )

        eliminados_datos = datos.get("eliminados")
        if not isinstance(eliminados_datos, list):
            raise ValueError("El campo 'eliminados' debe ser una lista.")
        eliminados = set()
        self._validarEliminados(eliminados_datos, eliminados)

        estaciones_datos = datos.get("estaciones")

        if not isinstance(estaciones_datos, list):
            raise ValueError("El campo 'estaciones' debe ser una lista.")
        estaciones = []
        ids_estaciones = set()
        self._validarEstaciones(estaciones_datos, estaciones, ids_estaciones)

        historico_datos = datos.get("historico")
        if not isinstance(historico_datos, list):
            raise ValueError("El historico debe ser una lista")
        historico = []
        ids_historico = set()
        self._validarHistorico(historico_datos, historico, ids_historico)

        cola_datos = datos.get("cola_reportes")
        if not isinstance(cola_datos, list):
            raise ValueError("El campo 'cola_reportes' debe ser una lista.")
        cola_reportes = deque()
        self._validarReportes(cola_datos, cola_reportes, ids_estaciones)

        metricas_datos = datos.get("metricas")
        if not isinstance(metricas_datos, dict):
            raise ValueError("El campo 'metricas' debe ser un objeto.")
        campos_metricas = {"escenario", "avl"}
        if set(metricas_datos.keys()) != campos_metricas:
            raise ValueError("El campo 'metricas' debe contener las métricas del escenario y del AVL.")
        
        metricas_escenario_datos = metricas_datos["escenario"]
        metricas_escenario = self._validarMetricasEscenario(metricas_escenario_datos)

        metricas_avl_datos = metricas_datos["avl"]
        metricas_avl = self._verificarMetricasAvl(metricas_avl_datos)
        nuevo_avl.metricas = metricas_avl


        ids_activos_avl = set(nodosAvl.keys())
        ids_activos_bst = set(nodosBst.keys())

        if ids_activos_avl != ids_activos_bst:
            raise ValueError("El AVL y el BST no contienen los mismos eventos activos.")

        self._validarMismosEventosyMismaKey(ids_activos_avl, nodosAvl, nodosBst)

        ids_historicos = {evento.id for evento in historico}

        if ids_activos_avl & ids_historicos:
            raise ValueError("Existen eventos que aparecen simultáneamente como activos y en el histórico.")
        if ids_activos_avl & eliminados:
            raise ValueError("Existen eventos que aparecen simultáneamente como activos y eliminados.")
        if ids_historicos & eliminados:
            raise ValueError("Existen eventos que aparecen simultáneamente como históricos y eliminados.")

        ids_estaciones = { estacion.id_estacion for estacion in estaciones }
        self._verificarExistenciaDeEstaciones(ids_estaciones, ids_activos_avl, nodosAvl, historico)

        estado = {
            "avl": nuevo_avl,
            "bst": nuevo_bst,
            "estaciones": estaciones,
            "zonas": zonas_temporales,
            "historico": historico,
            "eliminados": eliminados,
            "W": w,
            "R": r,
            "L": l,
            "T": t,
            "modo_estres": modo_estres,
            "reloj": reloj,
            "metricas": metricas_escenario,
            "cola_reportes": cola_reportes
        }

        return estado
        


    def _validarHistorico(self, historico_datos, historico, ids_historico):
        for datos_evento in historico_datos:
            if not isinstance(datos_evento, dict):
                raise ValueError("Cada elemento de 'historico' debe ser un objeto.")

            campos_evento = {
                "id",
                "magnitud",
                "profundidad",
                "zonax",
                "zonay",
                "fechaHora",
                "revision",
                "estaciones",
                "estado"
            }

            if set(datos_evento.keys()) != campos_evento:
                raise ValueError("Cada evento del histórico debe contener todos sus campos.")

            id_evento = datos_evento["id"]

            if type(id_evento) is not int or id_evento <= 0:
                raise ValueError(f"El ID del evento histórico {id_evento} no es válido.")

            if id_evento in ids_historico:
                raise ValueError(f"El evento histórico {id_evento} está repetido.")
            ids_historico.add(id_evento)

            revision = datos_evento["revision"]
            if type(revision) is not int or revision <= 0:
                raise ValueError(f"La revisión del evento histórico {id_evento} debe ser un entero positivo.")
            
            estaciones = datos_evento["estaciones"]
            if not isinstance(estaciones, list):
                raise ValueError(f"Las estaciones del evento histórico {id_evento} deben ser una lista.")
            for id_estacion in estaciones:
                if type(id_estacion) is not str or not id_estacion.strip():
                    raise ValueError(f"La referencia de estación del evento histórico {id_evento} no es válida.")
            
            estado = datos_evento["estado"]
            estados_validos = {"Pendiente", "Revisado"}
            if estado not in estados_validos:
                raise ValueError(f"El estado del evento histórico {id_evento} no es válido.")

            magnitud = datos_evento["magnitud"]
            if isinstance(magnitud, bool) or not isinstance(magnitud, (int, float, Decimal)):
                raise ValueError(f"La magnitud del evento histórico {id_evento} debe ser numérica.")
            if magnitud < 0:
                raise ValueError(f"La magnitud del evento histórico {id_evento} no puede ser negativa.")

            profundidad = datos_evento["profundidad"]
            if isinstance(profundidad, bool) or not isinstance(profundidad, (int, float, Decimal)):
                raise ValueError(f"La profundidad del evento histórico {id_evento} debe ser numérica.")
            if profundidad < 0:
                raise ValueError(f"La profundidad del evento histórico {id_evento} no puede ser negativa.")

            zonax = datos_evento["zonax"]
            if isinstance(zonax, bool) or not isinstance(zonax, (int, float, Decimal)):
                raise ValueError(f"La coordenada zonax del evento histórico {id_evento} debe ser numérica.")
            if not 0 <= zonax <= 1000:
                raise ValueError(f"La coordenada zonax del evento histórico {id_evento} debe estar entre 0 y 1000.")
            
            zonay = datos_evento["zonay"]
            if isinstance(zonay, bool) or not isinstance(zonay, (int, float, Decimal)):
                raise ValueError(f"La coordenada zonay del evento histórico {id_evento} debe ser numérica.")
            if not 0 <= zonay <= 1000:
                raise ValueError(f"La coordenada zonay del evento histórico {id_evento} debe estar entre 0 y 1000.")
            
            fecha = self._fechaDesdeJson(datos_evento["fechaHora"])

            evento = Evento(
                datos_evento["id"],
                datos_evento["magnitud"],
                datos_evento["profundidad"],
                datos_evento["zonax"],
                datos_evento["zonay"],
                fecha,
                datos_evento["revision"],
                datos_evento["estaciones"]
            )

            evento.estado = datos_evento["estado"]

            historico.append(evento)

    def _validarEliminados(self, eliminados_datos, eliminados):
        for id_evento in eliminados_datos:
            if type(id_evento) is not int or id_evento <= 0:
                raise ValueError(f"El identificador eliminado {id_evento} no es válido.")

            if id_evento in eliminados:
                raise ValueError(f"El identificador eliminado {id_evento} está repetido.")

            eliminados.add(id_evento)

    def _validarEstaciones(self, estaciones_datos, estaciones, ids_estaciones):
        for datos_estacion in estaciones_datos:
            if not isinstance(datos_estacion, dict):
                raise ValueError("Cada elemento de 'estaciones' debe ser un objeto.")

            campos_estacion = {"id_estacion", "nombre"}

            if set(datos_estacion.keys()) != campos_estacion:
                raise ValueError("Cada estación debe contener id_estacion y nombre.")

            id_estacion = datos_estacion["id_estacion"]
            nombre = datos_estacion["nombre"]

            if isinstance(id_estacion, bool) or not isinstance(id_estacion, str) or not id_estacion.strip():
                raise ValueError(f"El identificador de la estación {id_estacion} no es válido.")

            if id_estacion in ids_estaciones:
                raise ValueError(f"La estación {id_estacion} está repetida.")

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError(f"El nombre de la estación {id_estacion} no es válido.")

            ids_estaciones.add(id_estacion)

            estacion = Estacion(id_estacion, nombre)

            estaciones.append(estacion)

    def _validarReportes(self, cola_datos, cola_reportes, ids_estaciones):
        for datos_reporte in cola_datos:
            if not isinstance(datos_reporte, dict):
                raise ValueError("Cada elemento de 'cola_reportes' debe ser un objeto.")
            
            campos_reporte = {
                "id_evento",
                "nRevision",
                "magnitud",
                "profundidad",
                "zonax",
                "zonay",
                "fecha",
                "estacion"
            }

            if set(datos_reporte.keys()) != campos_reporte:
                raise ValueError("Cada reporte debe contener todos sus campos.")

            id_eventoReporte = datos_reporte["id_evento"]
            if type(id_eventoReporte) is not int or id_eventoReporte <= 0:
                raise ValueError(f"El ID del evento del reporte {id_eventoReporte} no es válido.")
            
            n_revision = datos_reporte["nRevision"]
            if type(n_revision) is not int or n_revision <= 0:
                raise ValueError(f"La revisión del reporte con evento {id_eventoReporte} debe ser un entero positivo.")
            magnitud = datos_reporte["magnitud"]
            profundidad = datos_reporte["profundidad"]
            zonax = datos_reporte["zonax"]
            zonay = datos_reporte["zonay"]

            for valor, nombre in [(magnitud, "magnitud"), (profundidad, "profundidad"), (zonax, "zonax"), (zonay, "zonay")]:
                if isinstance(valor, bool) or not isinstance(valor, (int, float, Decimal)):
                    raise ValueError(f"La {nombre} del reporte del evento {id_eventoReporte} debe ser numérica.")

            if magnitud < 0 or profundidad < 0:
                raise ValueError(f"La magnitud y profundidad del reporte del evento {id_eventoReporte} no pueden ser negativas.")

            fecha = self._fechaDesdeJson(datos_reporte["fecha"])

            estacion = datos_reporte["estacion"]

            if isinstance(estacion, bool) or not isinstance(estacion, str):
                raise ValueError(f"La estación del reporte del evento {id_eventoReporte} no es válida.")
            if estacion not in ids_estaciones:
                raise ValueError(f"La estación {estacion} del reporte del evento {id_eventoReporte} no existe.")

            reporte = Reporte(
                id_eventoReporte,
                n_revision,
                magnitud,
                profundidad,
                zonax,
                zonay,
                fecha,
                estacion
            )

            cola_reportes.append(reporte)

    def _validarMetricasEscenario(self, metricas_escenario_datos):
        if not isinstance(metricas_escenario_datos, dict):
            raise ValueError("Las métricas del escenario deben ser un objeto.")

        campos_metricas_escenario = {
            "correcciones_aceptadas",
            "reportes_descartados",
            "conflictos",
            "archivos_masivos",
            "eventos_archivados"
        }

        if set(metricas_escenario_datos.keys()) != campos_metricas_escenario:
            raise ValueError("Las métricas del escenario no contienen todos los campos requeridos.")

        metricas_escenario = {}

        for nombre, valor in metricas_escenario_datos.items():
            if type(valor) is not int or valor < 0:
                raise ValueError(f"La métrica '{nombre}' del escenario debe ser un entero no negativo.")
            metricas_escenario[nombre] = valor
        return metricas_escenario

    def _verificarMetricasAvl(self, metricas_avl_datos):
        if not isinstance(metricas_avl_datos, dict):
            raise ValueError("Las métricas del AVL deben ser un objeto.")

        campos_metricas_avl = {
            "casos_LL",
            "casos_RR",
            "casos_LR",
            "casos_RL",
            "giros_izquierda",
            "giros_derecha"
        }

        if set(metricas_avl_datos.keys()) != campos_metricas_avl:
            raise ValueError("Las métricas del AVL no contienen todos los campos requeridos.")

        metricas_avl = {}

        for nombre, valor in metricas_avl_datos.items():
            if type(valor) is not int or valor < 0:
                raise ValueError(f"La métrica '{nombre}' del AVL debe ser un entero no negativo.")
            metricas_avl[nombre] = valor
        return metricas_avl

    def _validarMismosEventosyMismaKey(self, ids_activos_avl, nodosAvl, nodosBst):
        for id_evento in ids_activos_avl:
            evento_avl = nodosAvl[id_evento].evento
            evento_bst = nodosBst[id_evento].evento

            if (
                evento_avl.id != evento_bst.id
                or evento_avl.magnitud != evento_bst.magnitud
                or evento_avl.profundidad != evento_bst.profundidad
                or evento_avl.zonax != evento_bst.zonax
                or evento_avl.zonay != evento_bst.zonay
                or evento_avl.fechaHora != evento_bst.fechaHora
                or evento_avl.revision != evento_bst.revision
                or evento_avl.estaciones != evento_bst.estaciones
                or evento_avl.estado != evento_bst.estado
            ):
                raise ValueError(f"El evento {id_evento} no coincide entre el AVL y el BST.")
            
            key_avl = nodosAvl[id_evento].key
            key_bst = nodosBst[id_evento].key

            if key_avl != key_bst:
                raise ValueError(f"La key del evento {id_evento} no coincide entre el AVL y el BST.")

    def _verificarExistenciaDeEstaciones(self, ids_estaciones, ids_activos_avl, nodosAvl, historico):
        for id_evento in ids_activos_avl:
            estaciones_evento = nodosAvl[id_evento].evento.estaciones
            for id_estacion in estaciones_evento:
                if id_estacion not in ids_estaciones:
                    raise ValueError(f"La estación {id_estacion} asociada al evento {id_evento} no existe.")
        
        for evento in historico:
            for id_estacion in evento.estaciones:
                if id_estacion not in ids_estaciones:
                    raise ValueError(f"La estación {id_estacion} asociada al evento {evento.id} no existe.")

    def _validarAlturasBST(self, nodos, nodos_datos, raiz_id):
        datos_por_id = {}

        for datos_nodo in nodos_datos:
            id_nodo = datos_nodo["key"]["id_key"]

            if "altura" not in datos_nodo:
                raise ValueError(f"El nodo {id_nodo} no contiene altura.")

            datos_por_id[id_nodo] = datos_nodo["altura"]

        def _calcular(nodo):
            if nodo is None:
                return -1

            altura_izquierda = _calcular(nodo.izq)
            altura_derecha = _calcular(nodo.der)

            altura_calculada = 1 + max(altura_izquierda, altura_derecha)

            id_nodo = nodo.key.id_key
            altura_guardada = datos_por_id[id_nodo]

            if altura_guardada != altura_calculada:
                raise ValueError(
                    f"La altura del nodo {id_nodo} no coincide. "
                    f"Guardada: {altura_guardada}, "
                    f"calculada: {altura_calculada}."
                )

            nodo.altura = altura_calculada

            return altura_calculada

        if raiz_id is not None:
            return _calcular(nodos[raiz_id])

        return -1

    def _profundidadMaxima(self, arbol):
        def recorrer(nodo, profundidad):
            if nodo is None:
                return -1

            return max(
                profundidad,
                recorrer(nodo.izq, profundidad + 1),
                recorrer(nodo.der, profundidad + 1)
            )

        return recorrer(arbol.raiz, 0)
    

    def guardarVersion(self, escenario, nombre):
        import json
        import re
        from pathlib import Path

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la versión es obligatorio.")

        nombre = nombre.strip()

        if not re.fullmatch(r"[A-Za-z0-9_-]+", nombre):
            raise ValueError(
                "El nombre de la versión solo puede contener letras, números, guion y guion bajo."
            )

        carpeta = Path(__file__).resolve().parent.parent.parent / "data" / "versiones"
        carpeta.mkdir(parents=True, exist_ok=True)

        nombre_archivo = nombre
        contador = 1

        while (carpeta / f"{nombre_archivo}.json").exists():
            nombre_archivo = f"{nombre}_{contador}"
            contador += 1

        datos = self.guardarEscenario(escenario)

        ruta = carpeta / f"{nombre_archivo}.json"

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        return {
            "nombre": nombre_archivo
        }

    def listarVersiones(self):
        from pathlib import Path

        carpeta = Path(__file__).resolve().parent.parent.parent / "data" / "versiones"
        carpeta.mkdir(parents=True, exist_ok=True)

        versiones = []

        for archivo in carpeta.glob("*.json"):
            versiones.append(archivo.stem)

        versiones.sort()

        return versiones

    def cargarVersion(self, nombre):
        import json
        import re
        from pathlib import Path

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la versión es obligatorio.")

        nombre = nombre.strip()

        if not re.fullmatch(r"[A-Za-z0-9_-]+", nombre):
            raise ValueError("Nombre de versión no válido.")

        carpeta = Path(__file__).resolve().parent.parent.parent / "data" / "versiones"
        ruta = carpeta / f"{nombre}.json"

        if not ruta.exists():
            raise ValueError(f"La versión '{nombre}' no existe.")

        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        return datos