import json
from datetime import datetime, timezone

from src.logic.Escenario import Escenario
from src.logic.Persistencia import Persistencia
from src.domain.Reporte import Reporte


def cargar_escenario_inicial():

    with open(
        "data/estado_inicial.json",
        "r",
        encoding="utf-8"
    ) as archivo:
        datos = json.load(archivo)

    config = datos["configuracion"]

    reloj = datetime.fromisoformat(
        config["reloj"].replace("Z", "+00:00")
    )

    escenario = Escenario(
        config["W"],
        config["R"],
        config["L"],
        config["T"],
        reloj
    )

    escenario.cargarEscenario(datos)

    escenario.pila_deshacer.clear()

    return escenario


def main():

    escenario = cargar_escenario_inicial()

    # =====================================================
    # EVENTOS ADICIONALES
    # =====================================================

    escenario.crearEvento(
        400,
        5.5,
        25,
        150,
        150,
        datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
        ["EST-1"]
    )

    escenario.crearEvento(
        500,
        4.5,
        20,
        600,
        600,
        datetime(2026, 10, 1, 9, 40, tzinfo=timezone.utc),
        ["EST-2"]
    )

    escenario.crearEvento(
        600,
        6.2,
        35,
        100,
        100,
        datetime(2026, 10, 1, 9, 50, tzinfo=timezone.utc),
        ["EST-3"]
    )

    escenario.crearEvento(
        700,
        4.8,
        60,
        700,
        200,
        datetime(2026, 10, 1, 10, 0, tzinfo=timezone.utc),
        ["EST-4"]
    )

    escenario.crearEvento(
        800,
        3.5,
        70,
        300,
        700,
        datetime(2026, 10, 1, 10, 10, tzinfo=timezone.utc),
        ["EST-3"]
    )

    # =====================================================
    # REPORTES PARA LA COLA
    # =====================================================

    escenario.encolarReporte(
        Reporte(
            200,
            1,
            6.0,
            30,
            600,
            600,
            datetime(2026, 10, 1, 9, 10, tzinfo=timezone.utc),
            "EST-2"
        )
    )

    escenario.encolarReporte(
        Reporte(
            100,
            1,
            5.0,
            20,
            100,
            100,
            datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
            "EST-1"
        )
    )

    escenario.encolarReporte(
        Reporte(
            300,
            2,
            4.2,
            50,
            200,
            700,
            datetime(2026, 10, 1, 9, 20, tzinfo=timezone.utc),
            "EST-3"
        )
    )

    escenario.encolarReporte(
        Reporte(
            400,
            1,
            5.5,
            25,
            150,
            150,
            datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
            "EST-1"
        )
    )

    escenario.encolarReporte(
        Reporte(
            800,
            1,
            3.5,
            70,
            300,
            700,
            datetime(2026, 10, 1, 10, 10, tzinfo=timezone.utc),
            "EST-3"
        )
    )

    # Mismo evento/revisión, pero datos diferentes.
    # Debe producir conflicto.
    escenario.encolarReporte(
        Reporte(
            500,
            1,
            4.9,
            20,
            600,
            600,
            datetime(2026, 10, 1, 9, 40, tzinfo=timezone.utc),
            "EST-2"
        )
    )

    # Reporte con revisión antigua.
    escenario.encolarReporte(
        Reporte(
            600,
            1,
            6.2,
            35,
            100,
            100,
            datetime(2026, 10, 1, 9, 50, tzinfo=timezone.utc),
            "EST-3"
        )
    )

    # =====================================================
    # GUARDAR ESCENARIO
    # =====================================================

    persistencia = Persistencia()

    datos = persistencia.guardarEscenario(
        escenario
    )

    with open(
        "data/escenario_pruebas.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    print("Escenario de pruebas generado correctamente.")
    print("Archivo: data/escenario_pruebas.json")


if __name__ == "__main__":
    main()