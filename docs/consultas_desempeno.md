# Consultas y análisis del desempeño

Todas las consultas devuelven `nodos_avl_examinados`. El contador suma cada nodo visitado en los recorridos y búsquedas AVL que forman esa consulta. El escaneo de eventos históricos se informa como estado en asociaciones, pero no se suma a ese contador porque no visita nodos AVL.

## Consultas

- `consultarPrimerosPendientes(k)` valida que `k` sea positivo y recorre las claves en orden inverso (derecha, nodo, izquierda). Se detiene al encontrar `k` pendientes. Como el estado no forma parte de la clave, no se puede descartar un subárbol solo porque sus claves sean menores; se descarta el resto una vez reunidos los `k` resultados. Peor caso: `O(n)`, con hasta `O(h + k)` espacio para pila y resultados.
- `consultarPorMagnitud(minimo, maximo)` usa límites inclusivos. La magnitud no es el primer componente de `Key` (prioridad lo es), así que no se puede podar con seguridad por magnitud: peor caso `O(n)` y `O(n)` para resultados.
- `consultarPorProfundidadYFechas(limite, inicio, fin)` aplica límites inclusivos. Profundidad y fecha no pertenecen a la clave, por lo que examina todo el AVL: peor caso `O(n)` y `O(n)` para resultados.
- `consultarAsociaciones(id)` devuelve candidatos, referencia elegida y eventos que tienen ese evento como referencia, incluyendo el estado activo/archivado. La búsqueda de referencias inversas compara cada evento con los candidatos, por lo que su peor caso es `O(n(n + a))`, donde `n` es el número activo y `a` el histórico; usa `O(n + a)` espacio auxiliar. El contador incluye las pasadas que recorren el AVL.
- `consultarEventosCostosos()` busca eventos de prioridad 3 a profundidad mayor que `L`, y reporta profundidad, límite y visitas de la búsqueda por clave. El recorrido inicial cuesta `O(n)`; cada búsqueda cuesta `O(h)`, por lo que el peor caso es `O(nh)` y `O(n)` de espacio para resultados.

## Comparación AVL/BST

`compararOrdenesInsercion()` reconstruye ambos árboles con el mismo conjunto activo en órdenes ascendente y descendente de clave. Reporta altura, hojas y comparaciones acumuladas al buscar las mismas claves. Un BST puede tener altura y búsquedas `O(n)` con inserción ordenada; un AVL mantiene altura `O(log n)`. Las métricas son estructurales y no dependen de tiempos de reloj.

El AVL ordena por `(prioridad, magnitud, id)`. Solo se descartan ramas cuando esa ordenación demuestra que no pueden contener el resultado; atributos ajenos a la clave requieren recorrido completo.