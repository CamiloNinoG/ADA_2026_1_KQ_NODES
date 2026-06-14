import os
import time
import pandas as pd
from datetime import datetime
import openpyxl
from src.controllers.manager import Manager
from src.strategies.kqnodes.kqnodes import KQNodes
from src.strategies.q_nodes import QNodes
from src.strategies.force import BruteForce
from src.strategies.kqnodes.profilter import KQNodesProfiler


def obtener_timestamp():
    """Devuelve la hora actual formateada para los prints."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def texto_a_binario(texto, universo):
    """Convierte una cadena de letras a su binario adaptado al tamaño del universo."""
    if pd.isna(texto):
        return "0" * len(universo)
    resultado = "".join(
        ["1" if letra in str(texto).upper() else "0" for letra in universo]
    )
    return resultado


def menu_configuracion():
    """Despliega el menú interactivo corregido en consola."""
    print("=" * 60)
    print(" 🛠️  PANEL DE CONFIGURACIÓN DE ESTRATEGIAS (IIT) ")
    print("=" * 60)

    # 1. Longitud del Universo
    while True:
        try:
            longitud = int(
                input("🔹 Ingrese la longitud del universo (10, 15, 20, 22, 25): ")
            )
            if longitud in [10, 15, 20, 22, 25]:
                break
            print("❌ Tamaño no estándar. Intente de nuevo.")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")

    # 2. Selección del Método (Primero el método, para máxima flexibilidad)
    print("\n🔹 Seleccione el método a utilizar:")
    print("  [1] QNodes (Solo K=2)")
    print("  [2] BruteForce (Solo K=2)")
    print("  [3] KQNodes (Soporta K=2 hasta K=5)")
    opc_metodo = input("👉 Opción: ").strip()

    if opc_metodo == "1":
        metodo = "QNodes"
        k_seleccionado = 2
        print("📌 Método QNodes seleccionado automáticamente con K=2 (Bipartición).")
    elif opc_metodo == "2":
        metodo = "BruteForce"
        k_seleccionado = 2
        print("📌 Método BruteForce seleccionado automáticamente con K=2 (Bipartición).")
    else:
        metodo = "KQNodes"
        # Si es KQNodes, el usuario decide libremente si quiere K=2, 3, 4 o 5
        while True:
            try:
                k_seleccionado = int(
                    input("\n🔹 Elija el valor de K partición para KQNodes (2 - 5): ")
                )
                if 2 <= k_seleccionado <= 5:
                    break
                print("❌ K debe estar entre 2 y 5.")
            except ValueError:
                print("❌ Ingrese un número válido.")

    return longitud, k_seleccionado, metodo


def iniciar():
    # Cargar configuraciones desde el menú dinámico
    LONGITUD_ELEMENTOS, K_PARTICIONES, METODO_USADO = menu_configuracion()

    nombre_hoja = f"{LONGITUD_ELEMENTOS}A-Elementos"
    universo_letras = "".join([chr(65 + i) for i in range(LONGITUD_ELEMENTOS)])

    # Configuración de bits moleculares
    estado_inicial = "1" + "0" * (LONGITUD_ELEMENTOS - 1)
    condiciones = "1" * LONGITUD_ELEMENTOS

    print(
        f"\n[{obtener_timestamp()}] 🌐 Inicializando Red con {LONGITUD_ELEMENTOS} bits..."
    )
    gestor_redes = Manager(estado_inicial)
    mpt = gestor_redes.cargar_red()

    # Instanciación exacta según la selección
    if METODO_USADO == "QNodes":
        print("🟢 Instanciando: QNODES")
        analizador_bf = QNodes(mpt)
    elif METODO_USADO == "BruteForce":
        print("🟢 Instanciando: BRUTE FORCE")
        analizador_bf = BruteForce(mpt)
    else:
        print("🟢 Instanciando: KQNODES")
        analizador_bf = KQNodes(mpt)

    ruta_excel_origen = os.path.join("src", "results", "pruebas.xlsx")
    ruta_salida = os.path.join("src", "results", "pruebas_con_resultados.xlsx")

    if not os.path.exists(ruta_excel_origen):
        print(
            f"[{obtener_timestamp()}] ❌ ERROR: No se encontró el archivo de origen en '{ruta_excel_origen}'"
        )
        return

    print(
        f"[{obtener_timestamp()}] 📊 Cargando datos crudos de origen con Pandas..."
    )
    df_origen = pd.read_excel(
        ruta_excel_origen, sheet_name=nombre_hoja, skiprows=4
    )
    df_origen.columns = df_origen.columns.str.strip().str.replace("\n", " ")

    # 🏗️ CONSTRUCCIÓN DEL NUEVO EXCEL DESDE CERO
    print(
        f"[{obtener_timestamp()}] 📄 Creando nueva estructura de reporte formateada..."
    )
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = nombre_hoja

    # Inyección de metadatos solicitados en el encabezado
    sheet["A1"] = f"K = {K_PARTICIONES}"
    sheet["A2"] = "Estado inicial:"
    sheet["B2"] = estado_inicial
    sheet["A3"] = "Sistema:"
    sheet["B3"] = universo_letras
    sheet["A4"] = "Sistema Candidato:"
    sheet["B4"] = universo_letras

    etiqueta_seccion = (
        "PRUEBAS BIPARTICIONES" if K_PARTICIONES == 2 else "PRUEBAS MULTIPARTICIONES"
    )
    sheet["D4"] = f"{etiqueta_seccion} ({METODO_USADO})"

    sheet["A5"] = "Subsistema"

    # Encabezados de las columnas de datos
    sheet["A6"] = "#Prueba"
    sheet["B6"] = "Alcance o Purview (t+1)"
    sheet["C6"] = "Mecanismo(t)"
    sheet["D6"] = "Partición"
    sheet["E6"] = "Pérdida"
    sheet["F6"] = "Tiempo"

    KQNodesProfiler.wrap(analizador_bf)

    print(f"\n[{obtener_timestamp()}] 🔍 Procesando datos e inyectando...")
    print("=" * 80)

    pruebas_procesadas = 0

    # Procesar filas mapeadas desde Pandas hacia el nuevo Libro de Trabajo
    for index, fila in df_origen.iterrows():
        id_prueba = fila.get("#Prueba")
        alcance_txt = fila.get("Alcance o Purview (t+1)")
        mecanismo_txt = fila.get("Mecanismo(t)")

        if pd.isna(alcance_txt) or pd.isna(mecanismo_txt):
            continue

        pruebas_procesadas += 1
        num_prueba = int(id_prueba) if not pd.isna(id_prueba) else (index + 1)
        fila_excel = index + 7

        alcance_bin = texto_a_binario(alcance_txt, universo_letras)
        mecanismo_bin = texto_a_binario(mecanismo_txt, universo_letras)

        print(
            f"[{obtener_timestamp()}] 🕒 [Prueba #{num_prueba}] (Fila Destino: {fila_excel})"
        )

        sheet[f"A{fila_excel}"] = num_prueba
        sheet[f"B{fila_excel}"] = alcance_txt
        sheet[f"C{fila_excel}"] = mecanismo_txt

        tiempo_inicio = time.time()
        try:
            # 🧠 Control Lógico de Reseteos y Métodos
            if K_PARTICIONES == 2:
                # Si es K=2 pero estás usando KQNodes, sí requiere reset_estado y aplicar_estrategia_k
                if METODO_USADO == "KQNodes":
                    if hasattr(analizador_bf, "reset_estado"):
                        analizador_bf.reset_estado()
                        print("      🔄 Estado reseteado (KQNodes ejecutando K=2).")
                    
                    sia_cero = analizador_bf.aplicar_estrategia_k(
                        estado_inicial, condiciones, alcance_bin, mecanismo_bin, 2
                    )
                else:
                    # QNodes o BruteForce para K=2: No se resetean y usan aplicar_estrategia estándar
                    print(f"      🚫 Salteando reset_estado para {METODO_USADO} (K=2)")
                    sia_cero = analizador_bf.aplicar_estrategia(
                        estado_inicial, condiciones, alcance_bin, mecanismo_bin
                    )
            else:
                # Para K > 2 (Siempre será KQNodes)
                if hasattr(analizador_bf, "reset_estado"):
                    analizador_bf.reset_estado()
                    print("      🔄 Estado reseteado para estrategia K > 2.")

                sia_cero = analizador_bf.aplicar_estrategia_k(
                    estado_inicial,
                    condiciones,
                    alcance_bin,
                    mecanismo_bin,
                    K_PARTICIONES,
                )

            tiempo_fin = time.time() - tiempo_inicio
            particion_val = getattr(sia_cero, "particion", "N/A")
            perdida_val = getattr(
                sia_cero, "phi", getattr(sia_cero, "perdida", sia_cero)
            )
            tiempo_str = f"{tiempo_fin:.4f}s"

            print(
                f"      ✨ [OK {METODO_USADO} K={K_PARTICIONES}] {tiempo_str} | Partición: {particion_val} | Pérdida: {perdida_val}"
            )

        except Exception as e:
            tiempo_fin = time.time() - tiempo_inicio
            particion_val = "ERROR"
            perdida_val = str(e)
            tiempo_str = f"{tiempo_fin:.4f}s"
            print(f"      ❌ ERROR en ejecución: {e}")

        # Inyectar resultados calculados en el bloque de salida
        sheet[f"D{fila_excel}"] = str(particion_val)
        sheet[f"E{fila_excel}"] = str(perdida_val)
        sheet[f"F{fila_excel}"] = tiempo_str

    print("\n" + "=" * 80)
    if pruebas_procesadas > 0:
        print(f"[{obtener_timestamp()}] 💾 Guardando resultados en: {ruta_salida}")
        wb.save(ruta_salida)
    else:
        print(
            f"[{obtener_timestamp()}] ⚠️ No se procesaron filas. Archivo no generado."
        )

    wb.close()
    KQNodesProfiler.report()


if __name__ == "__main__":
    iniciar()