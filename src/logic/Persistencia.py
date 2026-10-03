from datetime import datetime, timezone

from src.domain.Evento import Evento

from src.structures.Avl import Avl
from src.structures.Bst import Bst

from src.structures.Nodo import Key, Nodo

from decimal import Decimal

class Persistencia:

    def cargarInserciones(self, datos, zonas):
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
                raise ValueError(
                    f"Faltan campos obligatorios: {sorted(faltantes)}"
                )

            id_evento = datos_evento.get("id")

            if id_evento in ids:
                raise ValueError(
                    f"El identificador {id_evento} está repetido."
                )

            ids.add(id_evento)

            fecha = self._fechaDesdeJson(
                datos_evento.get("fechaHora")
            )

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
            raise ValueError(
                "La fecha debe ser una cadena."
            )

        try:
            if valor.endswith("Z"):
                valor = valor[:-1] + "+00:00"

            fecha = datetime.fromisoformat(valor)

        except ValueError:
            raise ValueError(
                "La fecha no tiene un formato ISO 8601 válido."
            )

        if fecha.tzinfo is None:
            raise ValueError(
                "La fecha debe incluir zona horaria."
            )

        return fecha.astimezone(timezone.utc)



    def cargarTopologia(self, datos, zonas):
        if not isinstance(datos, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")

        if datos.get("tipo_carga") != "topologia":
            raise ValueError("El archivo no corresponde a una carga por topología.")

        nodos_datos = datos.get("nodos")

        if not isinstance(nodos_datos, list):
            raise ValueError("El campo 'nodos' debe ser una lista.")

        raiz_id = datos.get("raiz")
        nodos = {}
        ids = set()

        for datos_nodo in nodos_datos:
            self._validarNodo(datos_nodo, ids, nodos, zonas)

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


    def _validarNodo(self, datos_nodo, ids: set, nodos: dict, zonas):
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