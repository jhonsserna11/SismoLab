# SismoLab — HTML + CSS + JavaScript

Versión independiente del prototipo visual de SismoLab para trabajar directamente desde VS Code.

## Archivos

- `index.html` — estructura y navegación de la interfaz.
- `styles.css` — estilos, layout, temas claro/oscuro y componentes visuales.
- `script.js` — navegación, renderizado de pantallas y comportamiento del prototipo.

## Cómo ejecutarlo

1. Abre esta carpeta en VS Code.
2. Abre `index.html` con Live Server (recomendado) o ábrelo directamente en el navegador.
3. No necesitas React, TypeScript, Vite, Tailwind ni `npm` para esta versión.

## Importante para el proyecto real

El prototipo conserva datos simulados para demostrar la interfaz. La lógica real de SismoLab debe conectarse después al backend/`Escenario`: creación y corrección de eventos, AVL/BST, cola FIFO de reportes, histórico y deshacer. La interfaz no debería volver a calcular esas reglas por su cuenta.
