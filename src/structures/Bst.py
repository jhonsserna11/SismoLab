from .Nodo import Nodo
from .Nodo import Key
from src.domain.Evento import Evento
from typing import Optional

class Bst:
    def __init__(self):
        self.raiz = None
        
    def insertar(self, dato: Key, evento:Evento) -> None:
        
        if self.raiz is None:
            self.raiz = Nodo(key=dato, evento=evento)
        else:
            self._insertar(self.raiz, dato, evento)
    
    def _insertar(self, nodo: Nodo, dato: Key, evento:Evento) -> None:
        if dato < nodo.key:
            # Insertar en el subárbol izquierdo
            if nodo.izq is None:
                nodo.izq = Nodo(key=dato, evento=evento)
            else:
                self._insertar(nodo.izq, dato, evento)
        elif dato > nodo.key:
            # Insertar en el subárbol derecho
            if nodo.der is None:
                nodo.der = Nodo(key=dato, evento=evento)
            else:
                self._insertar(nodo.der, dato, evento)
        
    def buscar(self, dato: Key) -> Optional[Nodo]:
    
        if self.raiz is None:
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
            return nodo
    
    def eliminar(self, dato: Key) -> None:
        if self.raiz is None:
            return
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
                return None
            
            # Caso 2: Nodo con solo hijo derecho
            if nodo.izq is None:
                return nodo.der
            
            # Caso 3: Nodo con solo hijo izquierdo
            if nodo.der is None:
                return nodo.izq
            
            # Caso 4: Nodo con dos hijos
            # Buscar el mínimo en el subárbol derecho (sucesor inorden)
            nodo_minimo = self._encontrar_minimo(nodo.der)
            nodo.key = nodo_minimo.key
            nodo.evento = nodo_minimo.evento
            nodo.der = self._eliminar(nodo.der, nodo_minimo.key)
        
        return nodo
    
    def _encontrar_minimo(self, nodo: Nodo) -> Nodo:
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual
        
    def preorden(self):
        if self.raiz is None:
            return []
        return self._preorden(self.raiz)

    def _preorden(self, nodo: Optional[Nodo]):
        if nodo is None:
            return []

        resultado = [nodo.key]
        resultado.extend(self._preorden(nodo.izq))
        resultado.extend(self._preorden(nodo.der))
        return resultado

    def inorden(self):
        if self.raiz is None:
            return []
        return self._inorden(self.raiz)

    def _inorden(self, nodo: Optional[Nodo]):
        if nodo is None:
            return []

        resultado = []
        resultado.extend(self._inorden(nodo.izq))
        resultado.append(nodo.key)
        resultado.extend(self._inorden(nodo.der))
        return resultado

    def posorden(self):
        if self.raiz is None:
            return []
        return self._posorden(self.raiz)

    def _posorden(self, nodo: Optional[Nodo]):
        if nodo is None:
            return []

        resultado = []
        resultado.extend(self._posorden(nodo.izq))
        resultado.extend(self._posorden(nodo.der))
        resultado.append(nodo.key)
        return resultado
        
    def altura(self) -> int:
    
        if self.raiz is None:
            return -1
        else:
            altura_resultado = self._altura(self.raiz)
            return altura_resultado
    
    def _altura(self, nodo: Optional[Nodo]) -> int:
        
        if nodo is None:
            return -1
        
        # Calcular la altura del subárbol izquierdo
        altura_izq = self._altura(nodo.izq)
        
        # Calcular la altura del subárbol derecho
        altura_der = self._altura(nodo.der)
        
        # La altura del nodo es 1 + el máximo de las alturas de sus subárboles
        altura_nodo = 1 + max(altura_izq, altura_der)
        
        # Actualizar la altura del nodo
        nodo.altura = altura_nodo
        
        return altura_nodo
    
    def cantidad_nodos(self) -> int:
    
        if self.raiz is None:
            return 0
        else:
            cantidad_resultado = self._cantidad_nodos(self.raiz)
            return cantidad_resultado
    
    def _cantidad_nodos(self, nodo: Optional[Nodo]) -> int:
        
        if nodo is None:
            return 0
        
        # Contar el nodo actual + cantidad de nodos en subárbol izquierdo + cantidad de nodos en subárbol derecho
        cantidad_izq = self._cantidad_nodos(nodo.izq)
        cantidad_der = self._cantidad_nodos(nodo.der)
        
        return 1 + cantidad_izq + cantidad_der
    
    def profundidad(self, dato: Key) -> int:
        
        if self.raiz is None:
            return -1
        
        profundidad_resultado = self._profundidad(self.raiz, dato, 0)
        if profundidad_resultado != -1:
            return profundidad_resultado
        else:
            return -1
    
    def _profundidad(self, nodo: Optional[Nodo], dato: Key, nivel: int) -> int:
        
        if nodo is None:
            return -1
        
        # Si encontramos el nodo, retornamos su profundidad
        if dato == nodo.key:
            return nivel
        
        # Buscar en el subárbol izquierdo
        resultado_izq = self._profundidad(nodo.izq, dato, nivel + 1)
        if resultado_izq != -1:
            return resultado_izq
        
        # Buscar en el subárbol derecho
        resultado_der = self._profundidad(nodo.der, dato, nivel + 1)
        return resultado_der