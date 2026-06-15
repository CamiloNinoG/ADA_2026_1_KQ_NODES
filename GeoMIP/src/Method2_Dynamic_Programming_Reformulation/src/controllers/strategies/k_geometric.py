import time
import numpy as np

from src.controllers.manager import Manager
from src.controllers.strategies.geometric import GeometricSIA
from src.models.core.solution import Solution
from src.constants.models import  KGEOMIP_LABEL
from src.funcs.format import fmt_kparte_q


class KGeoMIPStrategy(GeometricSIA):

    def __init__(self, manager: Manager):
        super().__init__(manager)

    def aplicar_estrategia(self, condicion: str, alcance: str, mecanismo: str, tpm: np.ndarray, k: int = 3):
        super().calcular_tabla_transiciones(condicion, alcance, mecanismo, tpm)

        self.min_emd = float("inf")
        self.mejor_particion = None
        self.mejor_dist = None
        
        # Generamos los arreglos de índices iniciales de forma directa y compacta
        presentes_init = np.arange(len(self.sia_subsistema.dims_ncubos), dtype=np.int8)
        futuros_init = np.arange(len(self.sia_subsistema.indices_ncubos), dtype=np.int8)
        self.aplicar_estrategia_k_geometric(k, presentes_init, futuros_init)
        
        if self.mejor_particion is None:
            raise ValueError("No se encontró ninguna partición válida")
        return Solution(
            estrategia=KGEOMIP_LABEL,
            perdida=self.min_emd,
            distribucion_subsistema=self.sia_dists_marginales,
            distribucion_particion=self.mejor_dist,
            tiempo_total=time.time() - self.sia_tiempo_inicio,
            particion=fmt_kparte_q(self.key_a_particion_global(self.mejor_particion))
        )

    def aplicar_estrategia_k_geometric(self, k: int, presentes_local, futuros_local):
        frontera = []
        particiones_iniciales = self.calcular_costos(presentes_local, futuros_local, [])
        for particion, valor in particiones_iniciales.items():
            frontera.append((particion, valor[0], valor[1]))

        while frontera:
            particion_actual, emd_actual, dist_actual = min(frontera, key=lambda x: x[1])
            frontera.remove((particion_actual, emd_actual, dist_actual))

            while True:
                if emd_actual >= self.min_emd:
                    break
                
                particion_actual_np = self.key_a_particion(particion_actual)

                if len(particion_actual_np) >= k:
                    self.min_emd = emd_actual
                    self.mejor_particion = particion_actual
                    self.mejor_dist = dist_actual
                    break

                hijos_totales = []

                for idx_bloque, (presentes, futuros) in enumerate(particion_actual_np):
                    if len(presentes) <= 1 or len(futuros) <= 1:
                        continue

                    partes_restantes = particion_actual_np.copy()
                    partes_restantes.pop(idx_bloque)

                    hijos = self.calcular_costos(presentes, futuros, partes_restantes)

                    for nueva_particion, valor in hijos.items():
                        emd_hijo = valor[0]
                        if emd_hijo >= self.min_emd:
                            continue
                        hijos_totales.append((nueva_particion, emd_hijo, valor[1]))

                if not hijos_totales:
                    break

                hijos_totales.sort(key=lambda x: x[1])
                mejor_hijo = hijos_totales[0]

                if len(hijos_totales) > 1:
                    frontera.extend(hijos_totales[1:])

                particion_actual = mejor_hijo[0]
                emd_actual = mejor_hijo[1]
                dist_actual = mejor_hijo[2]

    def key_a_particion(self, key):
        return [
            [
                np.array(presentes, dtype=np.int8),
                np.array(futuros, dtype=np.int8)
            ]
            for presentes, futuros in key
        ]
    def key_a_particion_global(self, key):

        return [
            [
                np.array(
                    [self.sia_subsistema.dims_ncubos[i] for i in presentes],
                    dtype=np.int8
                ),
                np.array(
                    [self.sia_subsistema.indices_ncubos[i] for i in futuros],
                    dtype=np.int8
                )
            ]
            for presentes, futuros in key
        ]