from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Nodo, Key

from src.domain.Evento import Evento

class Escenario:
    def __init__(self):
        self.avl = Avl()
        self.bst = Bst()

        self.estaciones = []
        self.zonas = []

        self.historico = []
        self.eliminados = set()

        self.W = 48
        self.R = 40
        self.L = 3
        self.T = 72

        self.modo_estres = False

    def crearEvento(self, idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion):
        try:
            if idEvento in self.eventos_ids:
                raise ValueError("El identificador ingresado ya existe.")

            evento = Evento(idEvento, magnitud, profundidad, zonax, zonay, fecha, 1, estacion)
            self._crearEvento(evento)
        except ValueError as e:
            print("error: ", e)
    def _crearEvento(self, evento:Evento):
        prioridad = evento.calcularPrioridad(self._esPoblada(evento.zonax, evento.zonay))
        key = Key(prioridad, evento.magnitud, evento.id)
        self.avl.insertar(key, evento)


    def _esPoblada(self, zonax, zonay)->bool:
        pass

    def consultarEvento(self, idEvento:int):
        if idEvento in self.historico:
            return {"status": "archivado"}
        elif idEvento in self.eliminados:
            return {"status": "eliminado"}

        if idEvento not in self.eventos_por_id:
            raise ValueError("el id ingresado no existe")
        else:
            nodo = self.avl.encontrarNodo(idEvento)
            evento = nodo.evento
            prioridad = nodo.key.prioridad
            profundidad = self.avl.nivel_de_un_nodo(nodo)

            poblada = self._esPoblada(evento.zonax, evento.zonay)

            return {
                "status": "activo",
                "magnitud": evento.magnitud,
                "profundidad": evento.profundidad,
                "zonax": evento.zonax,
                "zonay": evento.zonay,
                "fecha": evento.fechaHora,
                "revision": evento.revision,
                "estaciones": evento.estaciones,
                "poblada": poblada,
                "prioridad": prioridad,
                "clave": nodo.key.mostrarValores(),
                "estado": evento.estado,
                "profundidadNodo": profundidad
            }

        



