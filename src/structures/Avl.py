from .Nodo import Nodo
from .Nodo import Key
from src.domain.Evento import Evento

from collections import deque
from typing import Optional

class Avl:
    def __init__(self):
        self.raiz = None

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
                return self._rotacion_derecha(nodo)
            if balance < -1 and key > nodo.der.key:
                return self._rotacion_izquierda(nodo)
            if balance > 1 and key > nodo.izq.key:
                nodo.izq = self._rotacion_izquierda(nodo.izq)
                return self._rotacion_derecha(nodo)
            if balance < -1 and key < nodo.der.key:
                nodo.der = self._rotacion_derecha(nodo.der)
                return self._rotacion_izquierda(nodo)
        return nodo

    #Método inOrder: imprime el arbol de menor a mayor keys
    def inOrder(self):
        if self.raiz is None:
            print("Árbol vacío")
        self._inOrder(self.raiz)
    def _inOrder(self, nodo:Nodo):
        if nodo is None:
            return
        else:
            self._inOrder(nodo.izq)
            print(nodo.key.mostrarValores(), end=" ")
            self._inOrder(nodo.der)

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

    def obtenerDatosNodo(self, nodo:Nodo):
        altura = self._obtenerAltura(nodo)
        factor = self._factor_balance(nodo)

        return {"altura": altura, "factor": factor}

    def _rotacion_derecha(self, y: Nodo) -> Nodo:
        x = y.izq
        temporal = x.der

        x.der = y
        y.izq = temporal

        self._actualizarAltura(y)
        self._actualizarAltura(x)

        return x

    def _rotacion_izquierda(self, x: Nodo) -> Nodo:
        y = x.der
        temporal = y.izq

        y.izq = x
        x.der = temporal

        self._actualizarAltura(x)
        self._actualizarAltura(y)

        return y

    """ -------------------------------------------------------------------------------------- """
    def pre_order(self) -> None:
        if self.raiz is None:
            print("", end="")
        else:
            self._pre_order(self.raiz)
    def _pre_order(self, raiz: Optional[Nodo]) -> None:

        if raiz is None:
            return

        raiz.key.mostrarValores()

        self._pre_order(raiz.izq)
        self._pre_order(raiz.der)


    def post_order(self) -> None:

        if self.raiz is None:
            print("", end="")
        else:
            self._post_order(self.raiz)

    def _post_order(self, raiz: Optional[Nodo]) -> None:

        if raiz is None:
            return

        self._post_order(raiz.izq)
        self._post_order(raiz.der)

        raiz.key.mostrarValores()


    def anchura(self) -> None:
        if self.raiz is None:
            print("", end="")
        else:
            self._anchura(self.raiz)

    def _anchura(self, raiz: Nodo) -> None:
        cola = deque([raiz])
        while cola:
            nodo = cola.popleft()
            print(nodo.key.mostrarValores(), end=" ")

            if nodo.izq is not None:
                cola.append(nodo.izq)
            if nodo.der is not None:
                cola.append(nodo.der)

    def encontrarNodo(self, id:int)->Nodo:
        if self.raiz is None:
            return None
        else:
            return self._encontrarNodo(self.raiz, id)
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


    # *** Pendiente: verificar el parametro de busqueda para la eliminación del nodo (key completa o solo id_key)?
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
            balance = self._factor_balance(raiz)


            if (balance > 1 and self._factor_balance(raiz.izq) >= 0):
                return self._rotacion_derecha(raiz)
            if (balance > 1 and self._factor_balance(raiz.izq) < 0):
                raiz.izq = self._rotacion_izquierda(raiz.izq)
                return self._rotacion_derecha(raiz)
            if (balance < -1 and self._factor_balance(raiz.der) <= 0):
                return self._rotacion_izquierda(raiz)
            if (balance < -1 and self._factor_balance(raiz.der) > 0):
                raiz.der = self._rotacion_derecha(raiz.der)
                return self._rotacion_izquierda(raiz)
        return raiz


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