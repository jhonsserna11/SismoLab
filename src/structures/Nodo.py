from dataclasses import dataclass
from typing import Optional

@dataclass
class Key:
    prioridad: int
    magnitud: float
    id_key: int

    def __lt__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return (self.prioridad, self.magnitud, self.id_key) < (other.prioridad, other.magnitud, other.id_key)
    def __gt__(self, other):
            if not isinstance(other, Key):
                return NotImplemented
            return (self.prioridad, self.magnitud, self.id_key) > (other.prioridad, other.magnitud, other.id_key)
    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return (self.prioridad, self.magnitud, self.id_key) == (other.prioridad, other.magnitud, other.id_key)
    
    def mostrarValores(self):
        return ("["+ str(self.prioridad) + ", "+ str(self.magnitud) + ", "+ str(self.id_key)+" ]")

@dataclass
class Nodo:
    key: Key

    izq: Optional["Nodo"] = None
    der: Optional["Nodo"] = None
    altura: int = 0

    #Método esHoja: retorna el valor de verdad de la sentencia -> ambos hijos son None? (no hay hijos ni izq ni der)
    def esHoja(self)->bool:
        return self._esHoja(self)
    def _esHoja(self)->bool:
        return self.izq is None and self.der is None