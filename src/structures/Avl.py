from .Nodo import Nodo
from .Nodo import Key
from typing import Optional

class Avl:
    def __init__(self):
        self.raiz = None

    def insertar(self, key:Key)-> None:
        self.raiz = self._insertar(self.raiz, key)

    def _insertar(self, nodo:Optional["Nodo"], key:Key) -> Nodo:
        if nodo is None:
            return Nodo(key)

        if key < nodo.key:
            nodo.izq = self._insertar(nodo.izq, key)
        elif key == nodo.key:
            print("keys iguales")
            #clave duplicada (validar el flujo en este escenario)
        else:
            nodo.der = self._insertar(nodo.der, key)
        return nodo

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