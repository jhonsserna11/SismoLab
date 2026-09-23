from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Nodo, Key

from src.domain.Evento import Evento

from collections import deque

class Escenario:
    def __init__(self):
        self.avl = Avl()
        self.bst = Bst()

        self.estaciones = []
        self.zonas = []

        self.historico: list[Evento] = []
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
        return True

    def _buscarCandidatos(self, eventoB):
        candidatos = []

        if self.avl.raiz is None:
            return candidatos

        cola = deque([self.avl.raiz])

        while cola:
            nodo = cola.popleft()

            eventoA = nodo.evento

            if eventoA.esCandidato(eventoB, self.W, self.R):
                candidatos.append(eventoA)

            if nodo.izq is not None:
                cola.append(nodo.izq)

            if nodo.der is not None:
                cola.append(nodo.der)

        return candidatos
    def _agregarCandidatosArchivados(self, eventoB, candidatos):
        for eventoA in self.historico:
            if eventoA.esCandidato(eventoB, self.W, self.R):
                candidatos.append(eventoA)

    def _seleccionarCandidato(self, candidatos, eventoB):
        if not candidatos:
            return None

        mejor = candidatos[0]

        for candidato in candidatos[1:]:
            if candidato.magnitud > mejor.magnitud:
                mejor = candidato

            elif candidato.magnitud == mejor.magnitud:
                diferencia_candidato = (
                    eventoB.fechaHora - candidato.fechaHora
                ).total_seconds()

                diferencia_mejor = (
                    eventoB.fechaHora - mejor.fechaHora
                ).total_seconds()

                if diferencia_candidato < diferencia_mejor:
                    mejor = candidato

                elif diferencia_candidato == diferencia_mejor:
                    if candidato.id < mejor.id:
                        mejor = candidato

        return mejor

    def _obtenerAsociaciones(self, eventoB):
        candidatos = self._buscarCandidatos(eventoB)

        self._agregarCandidatosArchivados(
            eventoB,
            candidatos
        )

        asociado = self._seleccionarCandidato(
            candidatos,
            eventoB
        )

        return {
            "candidatos": candidatos,
            "asociado": asociado
        }

    def consultarEvento(self, idEvento:int):
        for evento in self.historico:
            if evento.id == idEvento:
                return {"status": "archivado"}
        if idEvento in self.eliminados:
            return {"status": "eliminado"}

        nodo = self.avl.encontrarNodo(idEvento)
        if nodo is None:
            raise ValueError("el id ingresado no existe")
        return self._consultarEvento(nodo)

    def _consultarEvento(self, nodo:Nodo):
        evento = nodo.evento
        prioridad = nodo.key.prioridad
        profundidad = self.avl.nivel_de_un_nodo(nodo.key)
        datos = self.avl.obtenerDatosNodo(nodo)

        poblada = self._esPoblada(evento.zonax, evento.zonay)
        asociaciones = self._obtenerAsociaciones(evento)
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
            "altura": datos["altura"],
            "factor_balance": datos["factor"],
            "asociaciones": {
                "candidatos": [candidato.id for candidato in asociaciones["candidatos"]],
                "asociado": asociaciones["asociado"].id if asociaciones["asociado"] is not None else None
            }
        }
