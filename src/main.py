from structures.Avl import Avl
from structures.Nodo import Nodo
from structures.Nodo import Key 

def main():
    K1 = Key(3, 5.0, 1)
    K2 = Key(3, 5.0, 2)
    K3 = Key(2, 8.0, 3)
    K4 = Key(2, 10.0, 4)
    K5 = Key(1, 6.1, 5)
    K6 = Key(1, 6.2, 6)

    avl1 = Avl()

    avl1.insertar(K1)
    avl1.insertar(K2)
    avl1.insertar(K3)

    avl1.inOrder()
    print("\n")

    avl1.insertar(K4)
    avl1.insertar(K5)
    avl1.insertar(K6)

    avl1.inOrder()

if __name__ == "__main__":
    main()
