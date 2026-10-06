# SISMOLAB AVL

Sistema de gestión y análisis de eventos sísmicos desarrollado en Python como proyecto de Estructuras de Datos.

El sistema utiliza un árbol AVL como estructura principal para almacenar los eventos sísmicos activos y un árbol BST como estructura de comparación. También incluye persistencia mediante archivos JSON, gestión de reportes, historial, versiones, modo de estrés y recuperación de la estructura.

## REQUISITOS

* Python 3.x
* Tkinter, incluido normalmente con la instalación de Python.

El proyecto utiliza únicamente módulos de la biblioteca estándar de Python y módulos propios del proyecto. No requiere la instalación de paquetes externos mediante pip.

## EJECUCIÓN

Para ejecutar el sistema se debe abrir una terminal y ubicarse en la carpeta raíz del proyecto:

```
SismoLab
```

Desde esta carpeta se ejecuta:

```
python -m src.main
```

Al ejecutar el comando se iniciará la aplicación.

## ESTRUCTURA GENERAL

El proyecto se encuentra organizado principalmente en:

* src/domain: clases correspondientes al modelo del dominio.
* src/structures: estructuras de datos implementadas para el proyecto.
* src/logic: lógica principal del sistema y persistencia.
* src/frontend: interfaz gráfica.
* src/data: datos y archivos utilizados por el sistema.
* tests: pruebas utilizadas durante el desarrollo.

## NOTA

El comando de ejecución debe realizarse desde la carpeta raíz SismoLab. Ejecutarlo desde otra ubicación puede impedir que Python encuentre correctamente el paquete src y sus módulos.
