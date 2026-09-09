from structures.Avl import Avl
from structures.Nodo import Nodo
from structures.Nodo import Key 

def main():
    K1 = Key(3, 5.0, 1)
    K2 = Key(3, 5.0, 2)
    K3 = Key(2, 8.0, 3)

    avl1 = Avl()

    avl1.insertar(K1)
    avl1.insertar(K2)
    avl1.insertar(K3)

    avl1.inOrder()

if __name__ == "__main__":
    main()
