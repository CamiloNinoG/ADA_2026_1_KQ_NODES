from pathlib import Path
import subprocess
import questionary


ROOT = Path(__file__).resolve().parent


def solicitar_estado_inicial(tamano_tpm: int) -> str:

    opcion = questionary.select(
        "Seleccione el estado inicial:",
        choices=[
            "Todo en 0",
            "1 seguido de ceros",
            "Ingresar manualmente"
        ]
    ).ask()

    if opcion == "Todo en 0":
        return "0" * tamano_tpm

    if opcion == "1 seguido de ceros":
        return "1" + ("0" * (tamano_tpm - 1))

    while True:

        estado = questionary.text(
            f"Ingrese un estado inicial de {tamano_tpm} bits:"
        ).ask()

        if len(estado) != tamano_tpm:
            print(f"Debe tener {tamano_tpm} bits.")
            continue

        if not all(c in "01" for c in estado):
            print("Solo se permiten 0 y 1.")
            continue

        return estado


def solicitar_vector(nombre: str, tamano_tpm: int) -> str:

    opcion = questionary.select(
        f"Seleccione {nombre}:",
        choices=[
            "Todo en 1",
            "Ingresar manualmente"
        ]
    ).ask()

    if opcion == "Todo en 1":
        return "1" * tamano_tpm

    while True:

        valor = questionary.text(
            f"Ingrese {nombre} ({tamano_tpm} bits):"
        ).ask()

        if len(valor) != tamano_tpm:
            print(f"Debe tener {tamano_tpm} bits.")
            continue

        if not all(c in "01" for c in valor):
            print("Solo se permiten 0 y 1.")
            continue

        return valor


def main():

    algoritmo = questionary.select(
        "Seleccione el algoritmo:",
        choices=[
            "KGeoMIP",
            "QNodes"
        ]
    ).ask()

    tamano_tpm = int(questionary.select(
            "Seleccione el tamaño de la TPM:",
            choices=[
                "10",
                "15",
                "20",
                "22",
                "25"
            ]
        ).ask()
    )

    k= int (questionary.select(
        "Seleccione k:",
        choices=[
            "2",
            "3",
            "4",
            "5"
        ] ).ask())
    estado =solicitar_estado_inicial(tamano_tpm)
    condiciones = solicitar_vector("las condiciones",tamano_tpm)
    alcance = solicitar_vector("el alcance",tamano_tpm)
    mecanismo =solicitar_vector("el mecanismo",tamano_tpm)

    if algoritmo == "KGeoMIP":

        subprocess.run(
            [
                "uv",
                "run",
                "exec_user.py",
                "--estado",
                estado,
                "--condiciones",
                condiciones,
                "--alcance",
                alcance,
                "--mecanismo",
                mecanismo,
                "--k",
                str(k),
                "--tamano",
                str(tamano_tpm),
            ],
            cwd=ROOT / "GeoMIP" / "src" / "Method2_Dynamic_Programming_Reformulation"
        )
    else:
        subprocess.run(
            [
                "uv",
                "run",
                "exec_user.py",
                "--estado",
                estado,
                "--condiciones",
                condiciones,
                "--alcance",
                alcance,
                "--mecanismo",
                mecanismo,
                "--k",
                str(k),
                "--tamano",
                str(tamano_tpm),
            ],
            cwd=ROOT / "QNodes" 
        )

if __name__ == "__main__":
    main()