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

    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return (self.prioridad, self.magnitud, self.id_key) == (other.prioridad, other.magnitud, other.id_key)
    def mostrarValores(self):
        return (str(self.prioridad) + ", "+ str(self.magnitud) + ", "+ str(self.id_key))

@dataclass
class Nodo:
    key: Key

    izq: Optional["Nodo"] = None
    der: Optional["Nodo"] = None
    altura: int = 0