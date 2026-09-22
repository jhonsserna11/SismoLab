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
            if not self._IdUnica(idEvento):
                raise ValueError("El identificador ingresado ya existe.")

            evento = Evento(idEvento, magnitud, profundidad, zonax, zonay, fecha, 1, estacion)
            self._crearEvento(evento)
        except ValueError as e:
            print("error: ", e)
    def _crearEvento(self, evento:Evento):
        prioridad = evento.calcularPrioridad(self._esPoblada(evento.zonax, evento.zonay))
        key = Key(prioridad, evento.magnitud, evento.id)
        self.avl.insertar(key, evento)

    def _IdUnica(self, id)->bool:
        if type(id) is not int:
            raise ValueError("el id ingresado debe ser numero entero")
        if type(self.avl.encontrarNodo(id)) is Nodo:
            return False
        for e in self.historico:
            if e.id == id:
                return False
        if id in self.eliminados:
            return False

        return True

                
    def _esPoblada(self, zonax, zonay)->bool:
        pass

    def consultarEvento(self, idEvento:int):
        if idEvento in self.historico:
            return {"status": "archivado"}
        elif idEvento in self.eliminados:
            return {"status": "eliminado"}

        nodo = self.avl.encontrarNodo(idEvento)
        if nodo is None:
            raise ValueError("el id ingresado no existe")
        else:
            self._consultarEvento(self, nodo)

    def _consultarEvento(self, nodo:Nodo):
        evento = nodo.evento
        prioridad = nodo.key.prioridad
        profundidad = self.avl.nivel_de_un_nodo(nodo)
        datos = self.avl.obtenerDatosNodo(nodo)

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
            "profundidadNodo": profundidad,
            "altura": datos.altura,
            "factor_balance": datos.factor
        }

        



