from structures.Avl import Avl
from structures.Nodo import Nodo
from structures.Nodo import Key 
from structures.Bst import Bst

def main():
    K1 = Key(3, 5.0, 1)
    K2 = Key(3, 5.0, 2)
    K3 = Key(2, 8.0, 3)

    bst1 = Bst()

    bst1.insertar(K1)
    bst1.insertar(K2)
    bst1.insertar(K3)

    bst1.inorden()
    bst1.preorden()
    bst1.posorden()
    
    
    bst1.buscar(K2)
    

if __name__ == "__main__":
    main()
