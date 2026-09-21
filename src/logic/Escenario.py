from src.structures.Avl import Avl
from src.structures.Bst import Bst

class Escenario:
    def __init__(self):
        self.avl = Avl()
        self.bst = Bst()

        self.estaciones = []
        self.zonas = []

        self.eventos_ids = {}

        self.historico = []
        self.eliminados = set()

        self.W = 48
        self.R = 40
        self.L = 3
        self.T = 72

        self.modo_estres = False

    def crearEvento(self, idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion):
        if idEvento in self.eventos_ids:
            ValueError("El identificador ingresado ya existe.")

        evento = Evento()
