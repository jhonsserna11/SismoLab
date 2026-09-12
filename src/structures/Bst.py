from .Nodo import Nodo
from .Nodo import Key
from typing import Optional

class Bst:
    def __init__(self):
        self.raiz = None
        
    def insertar(self, dato: Key) -> None:
        
        if self.raiz is None:
            self.raiz = Nodo(key=dato)
            print(f"El valor {dato.mostrarValores()} se ha insertado como raíz del árbol")
        else:
            self._insertar(self.raiz, dato)
    
    def _insertar(self, nodo: Nodo, dato: Key) -> None:
        if dato < nodo.key:
            # Insertar en el subárbol izquierdo
            if nodo.izq is None:
                nodo.izq = Nodo(key=dato)
                print(f"El valor {dato.mostrarValores()} se ha insertado a la izquierda de {nodo.key.mostrarValores()}")
            else:
                self._insertar(nodo.izq, dato)
        elif dato > nodo.key:
            # Insertar en el subárbol derecho
            if nodo.der is None:
                nodo.der = Nodo(key=dato)
                print(f"El valor {dato.mostrarValores()} se ha insertado a la derecha de {nodo.key.mostrarValores()}")
            else:
                self._insertar(nodo.der, dato)
        else:
            # El valor ya existe en el árbol
            print(f"El valor {dato.mostrarValores()} ya existe en el árbol")
    
    def buscar(self, dato: Key) -> Optional[Nodo]:
    
        if self.raiz is None:
            print("El árbol está vacío")
            return None
        else:
            return self._buscar(self.raiz, dato)
    
    def _buscar(self, nodo: Optional[Nodo], dato: Key) -> Optional[Nodo]:
        if nodo is None:
            return None
        
        if dato < nodo.key:
            # Buscar en el subárbol izquierdo
            return self._buscar(nodo.izq, dato)
        elif dato > nodo.key:
            # Buscar en el subárbol derecho
            return self._buscar(nodo.der, dato)
        else:
            # Nodo encontrado
            print(f"El valor {dato.mostrarValores()} ha sido encontrado")
            return nodo
    
    def eliminar(self, dato: Key) -> None:
        if self.raiz is None:
            print("El árbol está vacío")
        else:
            self.raiz = self._eliminar(self.raiz, dato)
    
    def _eliminar(self, nodo: Optional[Nodo], dato: Key) -> Optional[Nodo]:
        if nodo is None:
            return None
        
        if dato < nodo.key:
            nodo.izq = self._eliminar(nodo.izq, dato)
        elif dato > nodo.key:
            nodo.der = self._eliminar(nodo.der, dato)
        else:
            # Nodo encontrado
            # Caso 1: Nodo hoja
            if nodo.izq is None and nodo.der is None:
                print(f"El valor {dato.mostrarValores()} ha sido eliminado")
                return None
            
            # Caso 2: Nodo con solo hijo derecho
            if nodo.izq is None:
                print(f"El valor {dato.mostrarValores()} ha sido eliminado")
                return nodo.der
            
            # Caso 3: Nodo con solo hijo izquierdo
            if nodo.der is None:
                print(f"El valor {dato.mostrarValores()} ha sido eliminado")
                return nodo.izq
            
            # Caso 4: Nodo con dos hijos
            # Buscar el mínimo en el subárbol derecho (sucesor inorden)
            nodo_minimo = self._encontrar_minimo(nodo.der)
            nodo.key = nodo_minimo.key
            nodo.der = self._eliminar(nodo.der, nodo_minimo.key)
        
        return nodo
    
    def _encontrar_minimo(self, nodo: Nodo) -> Nodo:
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual
        
    def preorden(self) -> None:
        if self.raiz is None:
            print("El árbol está vacío")
        else:
            self._preorden(self.raiz)
    
    def _preorden(self, nodo: Optional[Nodo]) -> None:
        if nodo is None:
            return
        
        print(nodo.key.mostrarValores())
        self._preorden(nodo.izq)
        self._preorden(nodo.der)
        
    def inorden(self) -> None:
        if self.raiz is None:
            print("El árbol está vacío")
        else:
            self._inorden(self.raiz)
    
    def _inorden(self, nodo: Optional[Nodo]) -> None:
        if nodo is None:
            return
        
        self._inorden(nodo.izq)
        print(nodo.key.mostrarValores())
        self._inorden(nodo.der)
        
    def posorden(self) -> None:
        if self.raiz is None:
            print("El árbol está vacío")
        else:
            self._posorden(self.raiz)
    
    def _posorden(self, nodo: Optional[Nodo]) -> None:
        if nodo is None:
            return
        
        self._posorden(nodo.izq)
        self._posorden(nodo.der)
        print(nodo.key.mostrarValores())           