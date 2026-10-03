from .Nodo import Nodo
from .Nodo import Key
from src.domain.Evento import Evento

from collections import deque
from typing import Optional

class Avl:
    def __init__(self):
        self.raiz = None
        self.metricas = {
            "casos_LL": 0,
            "casos_RR": 0,
            "casos_LR": 0,
            "casos_RL": 0,
            "giros_izquierda": 0,
            "giros_derecha": 0
        }

    #Metodo insertar: agrega un nuevo nodo al árbol
    def insertar(self, key:Key, evento:Evento, modo_estres:bool)-> None:
        self.raiz = self._insertar(self.raiz, key, evento, modo_estres)
    def _insertar(self, nodo: Optional[Nodo], key: Key, evento:Evento, modo_estres:bool) -> Nodo:
        if nodo is None:
            return Nodo(key, evento)
        if key < nodo.key:
            nodo.izq = self._insertar(nodo.izq, key, evento, modo_estres)
        elif key > nodo.key:
            nodo.der = self._insertar(nodo.der, key, evento, modo_estres)
        else:
            return nodo

        self._actualizarAltura(nodo)

        if not modo_estres:
            balance = self._factor_balance(nodo)

            if balance > 1 and key < nodo.izq.key:
                self.metricas["casos_LL"] += 1
                return self._rotacion_derecha(nodo)
            if balance < -1 and key > nodo.der.key:
                self.metricas["casos_RR"] += 1
                return self._rotacion_izquierda(nodo)
            if balance > 1 and key > nodo.izq.key:
                self.metricas["casos_LR"] += 1
                nodo.izq = self._rotacion_izquierda(nodo.izq)
                return self._rotacion_derecha(nodo)
            if balance < -1 and key < nodo.der.key:
                self.metricas["casos_RL"] += 1
                nodo.der = self._rotacion_derecha(nodo.der)
                return self._rotacion_izquierda(nodo)
        return nodo


    def _obtenerAltura(self, nodo: Optional["Nodo"])->int:
        if nodo is None:
            return -1
        return nodo.altura

    def _actualizarAltura(self, nodo:Nodo)->None:
        nodo.altura = 1 + max(self._obtenerAltura(nodo.izq), self._obtenerAltura(nodo.der))

    def _factor_balance(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 0
        return (self._obtenerAltura(nodo.izq) - self._obtenerAltura(nodo.der))
    #dfbl<sdfhdsbfjh
    def verificarEstructura(self, modo_estres: bool = False) -> dict:
        registros = []
        visitados = {}
        ids_eventos = {}
        equilibrado = True

        def auditar(nodo, limite_inferior, limite_superior):
            nonlocal equilibrado
            if nodo is None:
                return -1, True

            referencia = id(nodo)
            if referencia in visitados:
                registros.append({
                    "referencia": referencia,
                    "repetido_de": visitados[referencia],
                    "id": getattr(getattr(nodo, "evento", None), "id", None),
                    "errores": ["Nodo repetido o ciclo en los enlaces"],
                    "advertencias": [],
                    "altura_recalculada": None,
                    "factor_balance_recalculado": None
                })
                return None, False
            visitados[referencia] = len(registros)

            evento = getattr(nodo, "evento", None)
            clave = getattr(nodo, "key", None)
            identificador = getattr(evento, "id", getattr(clave, "id_key", None))
            registro = {
                "referencia": referencia,
                "id": identificador,
                "errores": [],
                "advertencias": []
            }
            registros.append(registro)

            if not isinstance(clave, Key):
                registro["errores"].append("Clave ausente o inválida")
            else:
                if clave.prioridad not in {1, 2, 3}:
                    registro["errores"].append(
                        f"Prioridad inválida en la clave: {clave.prioridad}"
                    )
                try:
                    if limite_inferior is not None and not limite_inferior < clave:
                        registro["errores"].append("Clave fuera del límite inferior global")
                    if limite_superior is not None and not clave < limite_superior:
                        registro["errores"].append("Clave fuera del límite superior global")
                except (AttributeError, TypeError):
                    registro["errores"].append("Clave no comparable")

            if evento is None or not hasattr(evento, "id"):
                registro["errores"].append("Evento ausente o inválido")
            else:
                try:
                    ids_eventos.setdefault(evento.id, []).append(registro)
                except TypeError:
                    registro["errores"].append("Identificador de evento inválido")
                if isinstance(clave, Key):
                    if clave.id_key != evento.id:
                        registro["errores"].append("El identificador de la clave no coincide con el evento")
                    if clave.magnitud != evento.magnitud:
                        registro["errores"].append("La magnitud de la clave no coincide con el evento")

            altura_izquierda, izquierda_valida = auditar(
                getattr(nodo, "izq", None), limite_inferior,
                clave if isinstance(clave, Key) else limite_superior
            )
            altura_derecha, derecha_valida = auditar(
                getattr(nodo, "der", None),
                clave if isinstance(clave, Key) else limite_inferior, limite_superior
            )
            subarbol_valido = izquierda_valida and derecha_valida
            altura_calculada = (
                1 + max(altura_izquierda, altura_derecha)
                if subarbol_valido else None
            )
            factor_calculado = (
                altura_izquierda - altura_derecha
                if subarbol_valido else None
            )
            registro["altura_recalculada"] = altura_calculada
            registro["factor_balance_recalculado"] = factor_calculado

            if subarbol_valido and getattr(nodo, "altura", None) != altura_calculada:
                registro["errores"].append(
                    f"Altura almacenada {getattr(nodo, 'altura', None)}; recalculada {altura_calculada}"
                )

            if subarbol_valido and abs(factor_calculado) > 1:
                equilibrado = False
                mensaje = f"Factor de balance recalculado fuera de [-1, 1]: {factor_calculado}"
                if modo_estres:
                    registro["advertencias"].append("Desbalance esperado en modo estrés: " + mensaje)
                else:
                    registro["errores"].append(mensaje)

            return altura_calculada, subarbol_valido

        auditar(self.raiz, None, None)

        for identificador, eventos in ids_eventos.items():
            if len(eventos) > 1:
                for registro in eventos:
                    registro["errores"].append(f"Identificador duplicado: {identificador}")

        inconsistentes = [
            {clave: valor for clave, valor in registro.items() if clave != "referencia"}
            for registro in registros
            if registro["errores"] or registro["advertencias"]
        ]
        return {
            "valido": not any(registro["errores"] for registro in registros),
            "equilibrado": equilibrado,
            "modo": "estres" if modo_estres else "normal",
            "nodos_visitados": len(visitados),
            "eventos_inconsistentes": inconsistentes
        }
    #akfbkadhfkbhaj
    def obtenerDatosNodo(self, nodo:Nodo):
        altura = self._obtenerAltura(nodo)
        factor = self._factor_balance(nodo)

        return {"altura": altura, "factor": factor}

    def _rotacion_derecha(self, y: Nodo) -> Nodo:
        self.metricas["giros_derecha"] += 1
        x = y.izq
        temporal = x.der

        x.der = y
        y.izq = temporal

        self._actualizarAltura(y)
        self._actualizarAltura(x)

        return x

    def _rotacion_izquierda(self, x: Nodo) -> Nodo:
        self.metricas["giros_izquierda"] += 1
        y = x.der
        temporal = y.izq

        y.izq = x
        x.der = temporal

        self._actualizarAltura(x)
        self._actualizarAltura(y)

        return y

     #Método inOrder: imprime el arbol de menor a mayor keys
    def inOrder(self):
       recorrido = []
       self._inOrder(self.raiz, recorrido)
       return recorrido
    def _inOrder(self, nodo: Optional[Nodo], recorrido: list):
       if nodo is None:
           return
       self._inOrder(nodo.izq, recorrido)
       recorrido.append(nodo.key)
       self._inOrder(nodo.der, recorrido)

    def pre_order(self):
        recorrido = []
        self._pre_order(self.raiz, recorrido)
        return recorrido
    def _pre_order(self, nodo: Optional[Nodo], recorrido: list):
        if nodo is None:
            return
        recorrido.append(nodo.key)
        self._pre_order(nodo.izq, recorrido)
        self._pre_order(nodo.der, recorrido)

    def post_order(self):
        recorrido = []
        self._post_order(self.raiz, recorrido)
        return recorrido
    def _post_order(self, nodo: Optional[Nodo], recorrido: list):
        if nodo is None:
            return
        self._post_order(nodo.izq, recorrido)
        self._post_order(nodo.der, recorrido)
        recorrido.append(nodo.key)


    def anchura(self) -> None:
        if self.raiz is None:
            return []
        else:
            return self._anchura(self.raiz)

    def _anchura(self, raiz: Nodo) -> None:
        recorrido = []
        cola = deque([raiz])

        while cola:
            nodo = cola.popleft()
            recorrido.append(nodo.key)

            if nodo.izq is not None:
                cola.append(nodo.izq)

            if nodo.der is not None:
                cola.append(nodo.der)

        return recorrido

    def encontrarNodo(self, id:int)->Nodo:
        if self.raiz is None:
            return None
        else:
            return self._encontrarNodo(self.raiz, id)

    def encontrarNodoConConteo(self, id: int):
        if self.raiz is None:
            return None, 0

        cola = deque([self.raiz])
        nodos_examinados = 0
        while cola:
            nodo = cola.popleft()
            nodos_examinados += 1
            if nodo.key.id_key == id:
                return nodo, nodos_examinados
            if nodo.izq is not None:
                cola.append(nodo.izq)
            if nodo.der is not None:
                cola.append(nodo.der)

        return None, nodos_examinados

    def buscarConConteo(self, key: Key):
        nodo = self.raiz
        nodos_examinados = 0

        while nodo is not None:
            nodos_examinados += 1
            if key == nodo.key:
                return nodo, nodos_examinados
            if key < nodo.key:
                nodo = nodo.izq
            else:
                nodo = nodo.der

        return None, nodos_examinados

    def nodosConConteo(self):
        nodos = []
        if self.raiz is None:
            return nodos, 0

        pila = [self.raiz]
        while pila:
            nodo = pila.pop()
            nodos.append(nodo)
            if nodo.der is not None:
                pila.append(nodo.der)
            if nodo.izq is not None:
                pila.append(nodo.izq)

        return nodos, len(nodos)

    def primerosPendientesDescendente(self, k: int):
        pendientes = []
        if self.raiz is None:
            return pendientes, 0

        pila = []
        nodo = self.raiz
        nodos_examinados = 0

        while (nodo is not None or pila) and len(pendientes) < k:
            while nodo is not None:
                pila.append(nodo)
                nodo = nodo.der

            nodo = pila.pop()
            nodos_examinados += 1
            if nodo.evento.estado == "Pendiente":
                pendientes.append(nodo)
            nodo = nodo.izq

        return pendientes, nodos_examinados

    def nodosConProfundidadYConteo(self):
        nodos = []
        if self.raiz is None:
            return nodos, 0

        pila = [(self.raiz, 0)]
        while pila:
            nodo, profundidad = pila.pop()
            nodos.append((nodo, profundidad))
            if nodo.der is not None:
                pila.append((nodo.der, profundidad + 1))
            if nodo.izq is not None:
                pila.append((nodo.izq, profundidad + 1))

        return nodos, len(nodos)

    def _encontrarNodo(self, raiz:Nodo, id:int):
        cola = deque([raiz])
        while cola:
            nodo = cola.popleft()
            if nodo.key.id_key == id:
                return nodo
            if nodo.izq is not None:
                cola.append(nodo.izq)
            if nodo.der is not None:
                cola.append(nodo.der)
        return None


    def _buscar_minimo(self, raiz: Nodo) -> Nodo:
        actual = raiz
        while actual.izq is not None:
            actual = actual.izq
        return actual


    def eliminar(self, key: Key, modo_estres:bool) -> None:
        self.raiz = self._eliminar(self.raiz, key, modo_estres)

    def _eliminar( self, raiz: Optional[Nodo], key: Key, modo_estres:bool) -> Optional[Nodo]:
        if raiz is None:
            return None
        
        if key < raiz.key:
            raiz.izq = self._eliminar(raiz.izq, key, modo_estres)

        elif key > raiz.key:
            raiz.der = self._eliminar(raiz.der, key, modo_estres)

        else:
            # Nodo hoja
            if raiz.esHoja():
                return None

            # Solo tiene hijo derecho
            if raiz.izq is None:
                return raiz.der

            # Solo tiene hijo izquierdo
            if raiz.der is None:
                return raiz.izq

            # Tiene dos hijos
            sucesor = self._buscar_minimo(
                raiz.der
            )

            raiz.key = sucesor.key
            raiz.evento = sucesor.evento

            raiz.der = self._eliminar(raiz.der, sucesor.key, modo_estres)

        self._actualizarAltura(raiz)

        if not modo_estres:
            return self._balancear(raiz)
        return raiz

    def _balancear(self, raiz):
        balance = self._factor_balance(raiz)
        
        if (balance > 1 and self._factor_balance(raiz.izq) >= 0):
            self.metricas["casos_LL"] += 1
            return self._rotacion_derecha(raiz)
        if (balance > 1 and self._factor_balance(raiz.izq) < 0):
            self.metricas["casos_LR"] += 1
            raiz.izq = self._rotacion_izquierda(raiz.izq)
            return self._rotacion_derecha(raiz)
        if (balance < -1 and self._factor_balance(raiz.der) <= 0):
            self.metricas["casos_RR"] += 1
            return self._rotacion_izquierda(raiz)
        if (balance < -1 and self._factor_balance(raiz.der) > 0):
            self.metricas["casos_RL"] += 1
            raiz.der = self._rotacion_derecha(raiz.der)
            return self._rotacion_izquierda(raiz)
        return raiz

    def recuperar(self):
        self.raiz = self._recuperar(self.raiz)
    def _recuperar(self, subraiz:Nodo):
        if subraiz is None:
            return None

        subraiz.izq = self._recuperar(subraiz.izq)
        subraiz.der = self._recuperar(subraiz.der)

        self._actualizarAltura(subraiz)

        subraiz = self._balancear(subraiz)
        return subraiz

    def altura(self) -> int:

        if self.raiz is None:
            return -1

        return self._altura(self.raiz)

    def _altura(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return -1

        return 1 + max(
            self._altura(nodo.izq),
            self._altura(nodo.der)
        )

    def peso(self) -> int:
        if self.raiz is None:
            return 0
        return self._peso(self.raiz)
    def _peso(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 0

        return (1 + self._peso(nodo.izq) + self._peso(nodo.der))


    def recorrido_por_ramas(self) -> None:
        if self.raiz is None:
            print("El árbol está vacío.")
            return

        print("Caminos por ramas:")

        self._recorrido_por_ramas(
            self.raiz,
            []
        )
    def _recorrido_por_ramas(self, nodo: Nodo, camino: list) -> None:
        camino.append(nodo.key)

        if nodo.esHoja():
            print(
                " -> ".join(
                    map(str, camino)
                )
            )
        else:
            if nodo.izq is not None:
                self._recorrido_por_ramas(
                    nodo.izq,
                    camino.copy()
                )
            if nodo.der is not None:
                self._recorrido_por_ramas(
                    nodo.der,
                    camino.copy()
                )


    def nivel_de_un_nodo(self, key: Key) -> int:
        if self.raiz is None:
            return -1

        return self._nivel_de_un_nodo(self.raiz,key,0)

    def nivel_de_un_nodoConConteo(self, key: Key):
        nodo = self.raiz
        nivel = 0
        nodos_examinados = 0

        while nodo is not None:
            nodos_examinados += 1
            if nodo.key == key:
                return nivel, nodos_examinados
            if key < nodo.key:
                nodo = nodo.izq
            else:
                nodo = nodo.der
            nivel += 1

        return -1, nodos_examinados

    def _nivel_de_un_nodo(self, nodo: Optional[Nodo], key: Key, nivel_actual: int) -> int:
        if nodo is None:
            return -1

        if nodo.key == key:
            return nivel_actual

        if key < nodo.key:
            return self._nivel_de_un_nodo(
                nodo.izq,
                key,
                nivel_actual + 1
            )
        else:
            return self._nivel_de_un_nodo(
                nodo.der,
                key,
                nivel_actual + 1
            )

    def nodos_con_profundidad(self):
        nodos = []
        self._nodos_con_profundidad(self.raiz, 0, nodos)
        return nodos

    def _nodos_con_profundidad(self, nodo, profundidad, nodos):
        if nodo is None:
            return

        nodos.append((nodo, profundidad))

        self._nodos_con_profundidad(
            nodo.izq,
            profundidad + 1,
            nodos
        )

        self._nodos_con_profundidad(
            nodo.der,
            profundidad + 1,
            nodos
        )

    def cantidad_de_nodos_por_nivel(self) -> dict:
        if self.raiz is None:
            return {}
        conteo = {}
        self._cantidad_de_nodos_por_nivel(
            self.raiz,
            0,
            conteo
        )
        return conteo
    def _cantidad_de_nodos_por_nivel(
        self,
        nodo: Optional[Nodo],
        nivel: int,
        conteo: dict
    ) -> None:

        if nodo is None:
            return

        conteo[nivel] = (
            conteo.get(nivel, 0) + 1
        )

        self._cantidad_de_nodos_por_nivel(
            nodo.izq,
            nivel + 1,
            conteo
        )

        self._cantidad_de_nodos_por_nivel(
            nodo.der,
            nivel + 1,
            conteo
        )

    def hojas(self) -> int:
        return self._hojas(self.raiz)
    def _hojas(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 0

        if nodo.esHoja():
            return 1

        return self._hojas(nodo.izq) + self._hojas(nodo.der)

    def eventos_por_prioridad(self):
        eventos = {
            1: [],
            2: [],
            3: []
        }
        self._eventos_por_prioridad(self.raiz, eventos)
        return eventos
    def _eventos_por_prioridad(self, nodo, eventos):
        if nodo is None:
            return

        prioridad = nodo.key.prioridad
        eventos[prioridad].append(nodo)

        self._eventos_por_prioridad(nodo.izq, eventos)
        self._eventos_por_prioridad(nodo.der, eventos)

    def eventos_pendientes(self):
        pendientes = []
        self._eventos_pendientes(self.raiz, pendientes)
        return pendientes
    def _eventos_pendientes(self, nodo:Nodo, pendientes):
        if nodo is None:
            return

        if nodo.evento.estado == "Pendiente":
            pendientes.append(nodo)

        self._eventos_pendientes(nodo.izq, pendientes)
        self._eventos_pendientes(nodo.der, pendientes)