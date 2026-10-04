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
            if nodo.izq is None:
                nodo.izq = Nodo(key=dato, evento=evento)
            else:
                self._insertar(nodo.izq, dato, evento)
        elif dato > nodo.key:
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
            return self._buscar(nodo.izq, dato)
        elif dato > nodo.key:
            return self._buscar(nodo.der, dato)
        else:
            return nodo

    def buscarConConteo(self, dato: Key):
        nodo = self.raiz
        comparaciones = 0

        while nodo is not None:
            comparaciones += 1
            if dato == nodo.key:
                return nodo, comparaciones
            if dato < nodo.key:
                nodo = nodo.izq
            else:
                nodo = nodo.der

        return None, comparaciones
    
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
            if nodo.izq is None and nodo.der is None:
                return None
            
            if nodo.izq is None:
                return nodo.der
            
            if nodo.der is None:
                return nodo.izq
            
            # Replace a node with two children by its in-order successor.
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

    def hojas(self) -> int:
        return self._hojas(self.raiz)

    def _hojas(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 0
        if nodo.esHoja():
            return 1
        return self._hojas(nodo.izq) + self._hojas(nodo.der)
    
    def _altura(self, nodo: Optional[Nodo]) -> int:
        
        if nodo is None:
            return -1
        
        altura_izq = self._altura(nodo.izq)
        
        altura_der = self._altura(nodo.der)
        
        altura_nodo = 1 + max(altura_izq, altura_der)
        
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
        
        if dato == nodo.key:
            return nivel
        
        resultado_izq = self._profundidad(nodo.izq, dato, nivel + 1)
        if resultado_izq != -1:
            return resultado_izq
        
        resultado_der = self._profundidad(nodo.der, dato, nivel + 1)
        return resultado_der

    def hojas(self):
        def contar_hojas(nodo):
            if nodo is None:
                return 0

            if nodo.izq is None and nodo.der is None:
                return 1

            return contar_hojas(nodo.izq) + contar_hojas(nodo.der)

        return contar_hojas(self.raiz)

    def profundidad_maxima(self):
        def calcular(nodo, profundidad):
            if nodo is None:
                return -1

            if nodo.izq is None and nodo.der is None:
                return profundidad

            profundidad_izq = calcular(nodo.izq, profundidad + 1)
            profundidad_der = calcular(nodo.der, profundidad + 1)

            return max(profundidad_izq, profundidad_der)

        if self.raiz is None:
            return -1

        return calcular(self.raiz, 0)