from src.structures.Avl import Avl
from src.structures.Bst import Bst

class Escenario:
    def __init__(self):
        self.avl = Avl()
        self.bst = Bst()

        self.estaciones = []
        self.zonas = []

        self.historico = []
        self.eliminados = set()

        self.cola_reportes = ...

        self.reloj = ...

        self.W = 48
        self.R = 40
        self.L = 3
        self.T = 72

        self.modo_estres = False

        self.asociaciones = ...

        self.metricas = ...

        self.historial = ...