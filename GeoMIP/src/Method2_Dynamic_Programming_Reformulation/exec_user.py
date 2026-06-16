import argparse

from src.controllers.manager import Manager

# 👇 Importación de estrategias 👇 #
from src.controllers.strategies.k_geometric import KGeoMIPStrategy





def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--estado")
    parser.add_argument("--condiciones")
    parser.add_argument("--alcance")
    parser.add_argument("--mecanismo")
    parser.add_argument("--k", type=int)
    parser.add_argument("--tamano", type=int)

    args = parser.parse_args()

    print(args.estado)
    print(args.condiciones)
    print(args.alcance)
    print(args.mecanismo)
    print(args.k)
    print(args.tamano)
    
    gestor_redes = Manager(args.estado)
    gestor_redes.generar_red(args.tamano)
    tpm = gestor_redes.cargar_red()
    

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_bf : KGeoMIPStrategy = KGeoMIPStrategy(gestor_redes)

    sia_cero = analizador_bf.aplicar_estrategia(
        args.condiciones,
        args.alcance,
        args.mecanismo,
        tpm,
        args.k
    )
    print(sia_cero)


if __name__ == "__main__":
    main()
    