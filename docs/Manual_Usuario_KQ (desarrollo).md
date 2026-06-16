# Manual de Usuario - Proyectos KQNodes y KGeoMIP

**Herramientas de Análisis Geométrico y Submodular para K-Particiones de Mínima Información (IIT 3.0)**  
**Asignatura:** Análisis y Diseño de Algoritmos  
**Facultad:** Facultad de Inteligencia Artificial e Ingenierías, Universidad de Caldas  
**Período:** 2026-1

---

## Índice Temático

* **2.1 Introducción y Visión General**  
  * Estructura general del proyecto  
  * ¿Qué hace el software? (KQNodes y KGeoMIP)  
  * ¿Para qué sirve? Aplicaciones prácticas  
  * Conceptos clave de forma intuitiva  
  * Capacidades y límites de escala del sistema (Comparativa de algoritmos)  
* **2.2 Requisitos del Sistema**  
  * Sistemas operativos compatibles  
  * Especificaciones de hardware recomendadas  
  * Entorno de software requerido  
* **2.3 Instalación Paso a Paso**  
  * Paso 1: Descarga y extracción del proyecto  
  * Paso 2: Creación y activación del entorno virtual (Python venv / UV)  
  * Paso 3: Sincronización e instalación de las dependencias requeridas  
  * Verificación de la instalación del entorno (Comandos de diagnóstico)  
* **2.4 Video Tutorial de Instalación y Uso**  
  * Acceso al video demostrativo y contenido obligatorio  
* **2.5 Guía de Uso del Sistema**  
  * **Perfil de Usuario No Avanzado: Ejecución por CLI e Interfaz Interactiva**  
    * Ejecución interactiva rápida (`main.py` en la raíz)  
    * Ejecución directa por línea de comandos (`exec_user.py` en QNodes y GeoMIP)  
  * **Perfil de Usuario Avanzado: Ejecución y Automatización por Lotes desde Excel**  
    * Configuración inicial de parámetros y ejecución en QNodes (`src/main.py`)  
    * Configuración inicial y ejecución en KGeoMIP (`src/main.py`)  
* **2.6 Opciones y Parámetros Avanzados**  
  * Configuración dinámica del pool de candidatos en KQNodes  
  * Límites del refinamiento local (VND) en KQNodes  
  * Configuración de la estrategia Branch and Bound en KGeoMIP  
  * Modos de operación y límites físicos (Exhaustivo, Heurístico, Modo Grande y Bypass)  
  * Automatización de pruebas masivas en Excel (`tests/estrategias.py` y `exec.py`)  
  * Mapeo comparativo de lectura y escritura en hojas de cálculo  
  * Optimización y consejos de rendimiento  

---

## 2.1 Introducción y Visión General

### ¿Qué hace el software?

El software desarrollado en este repositorio es una solución computacional de alto rendimiento en Python diseñada para el análisis estructural, modular y de integración de información en sistemas dinámicos complejos. Su propósito principal es calcular la **Partición de Mínima Información (k-MIP)** de un sistema físico o lógico distribuido en exactamente $k$ bloques independientes (donde $2 \le k \le 5$).

Para resolver este problema, el repositorio integra dos aproximaciones algorítmicas de frontera:
1.  **KQNodes**: Extensión del algoritmo Q clásico que minimiza una función submodular de pérdida sobre el espacio de estados mediante fusiones jerárquicas greedy y un refinamiento local de tipo VND (Variable Neighborhood Descent) con swaps.
2.  **KGeoMIP**: Implementación geométrica (Método 2) que mapea el espacio de estados en un hipercubo n-dimensional. Genera una tabla de costos de transición entre estados a través de distancias de Hamming y utiliza un algoritmo Branch and Bound ordenado en cola de prioridad para encontrar la subdivisión de bloques con menor pérdida.

A partir de la Matriz de Probabilidad de Transición (TPM) del sistema, ambos métodos determinan cuál es la partición que minimiza la pérdida de información causal al asumir que los bloques se comportan de forma aislada.

### ¿Para qué sirve? Aplicaciones prácticas

Este software es una herramienta avanzada para investigadores y profesionales en ciencia cognitiva, neurociencia computacional y teoría de redes complejas. Sus aplicaciones clave incluyen:

* **Medición de la Integración de Información (IIT 3.0):** Permite evaluar el valor de $\Phi$ (Phi), determinando el nivel de irreducibilidad causal y conciencia causal teórica de circuitos electrónicos y redes biológicas.  
* **Identificación de Fronteras Modulares:** Encuentra agrupaciones causales naturales (comunidades) de variables en sistemas dinámicos multivariados.  
* **Análisis Causal en Hardware Digital:** Cuantifica el impacto que tienen ciertos componentes o compuertas lógicas sobre el comportamiento de microcontroladores y buses de datos.

### Conceptos clave de forma intuitiva

Para operar la herramienta no se requiere una formación matemática avanzada. Los conceptos esenciales se describen a continuación:

* **Estado del Sistema:** Es la configuración binaria activa ($1$) o inactiva ($0$) de todas las variables de la red en un instante. Por ejemplo, en un sistema de 4 variables, el estado `"1000"` significa que solo la primera variable está encendida.  
* **Variables de Presente (Mecanismo) y Futuro (Alcance):** El análisis causal examina cómo el estado actual de un grupo de variables (mecanismo) determina probabilísticamente el estado futuro de otro grupo de variables (alcance o purview).  
* **$k$-Partición:** Es una división del sistema de variables en exactamente $k$ subgrupos disjuntos y no vacíos (bloques). En una tri-partición ($k=3$) de las variables futuras $\{A, B, C\}$, la única división posible es asignar cada variable a su propio bloque: $\{A\}$, $\{B\}$ y $\{C\}$.  
* **Pérdida EMD (Earth Mover's Distance):** Es la métrica utilizada para cuantificar la "distancia" o diferencia entre la dinámica del sistema completo y la dinámica simplificada (particionada). Si al desconectar las interacciones entre bloques el sistema se comporta de manera casi idéntica, la pérdida EMD será muy cercana a $0$, indicando una frontera natural del sistema.

### Estructura general del proyecto

El repositorio completo está estructurado para albergar de forma aislada tanto la base clásica de QNodes como la aproximación geométrica de KGeoMIP, compartiendo la raíz del espacio de trabajo:

```
ADA_2026_1_KQ_NODES/              # Directorio raíz del proyecto
├── main.py                       # Interfaz interactiva unificada (questionary)
├── pyproject.toml                # Configuración de dependencias raíz (uv)
├── uv.lock                       # Lockfile de dependencias del entorno uv
├── DOCUMENTACION_SISTEMA.md      # Documentación arquitectónica de bajo nivel
├── MANUAL_DE_USUARIO.md          # Manual del usuario final del framework
├── QNodes/                       # --- Subproyecto Clásico (QNodes) ---
│   ├── exec.py                   # Script de automatización en lote para Excel
│   ├── exec_user.py              # CLI para ejecución rápida de usuario (no avanzado)
│   ├── pyphi_config.yml          # Configuración de PyPhi
│   ├── src/
│   │   ├── main.py               # Lógica interna de procesamiento por lotes QNodes
│   │   ├── controllers/
│   │   │   └── manager.py        # Gestor de red (carga de CSV y caché NPY)
│   │   ├── funcs/
│   │   │   ├── force.py          # Fuerza bruta y combinatoria
│   │   │   ├── format.py         # Visualización y formateo de salidas
│   │   │   └── iit.py            # EMD y utilidades matemáticas IIT
│   │   ├── models/               # Clases de dominio (System, NCube, Solution)
│   │   └── strategies/
│   │       ├── force.py          # Búsqueda exhaustiva k-particiones
│   │       ├── q_nodes.py        # Algoritmo Q clásico (biparticiones)
│   │       └── kqnodes/          # Algoritmo KQNodes (k-particiones)
│   │           ├── kqnodes.py    # Clase orquestadora principal
│   │           ├── tree_search.py# Búsqueda de fronteras en árbol de fusiones Q
│   │           ├── refinement.py # VND y Swaps de variables
│   │           ├── candidates.py # Pools de candidatos heurísticos/estructurales
│   │           └── permutation_selector.py # Selector rápido de emparejamientos
│   └── tests/                    # Scripts de verificación automatizada
│       ├── test_bruteforce_k3.py # Validación contra fuerza bruta
│       └── test_n25_scalability.py # Test de estrés de velocidad y RAM para N=25
└── GeoMIP/                       # --- Subproyecto Geométrico (GeoMIP) ---
    ├── Dataset_Description.md    # Descripción técnica de los datasets TPM
    ├── data/
    │   ├── creation.py           # Generador de TPMs sintéticas
    │   └── samples/              # Carpeta de almacenamiento de matrices CSV/NPY
    ├── results/                  # Entradas y salidas Excel de experimentos
    └── src/
        └── Method2_Dynamic_Programming_Reformulation/
            ├── exec.py           # Script de automatización por lotes en KGeoMIP
            ├── exec_user.py      # CLI para ejecución rápida geométrica
            ├── pyphi_config.yml  # Configuración de PyPhi para el método geométrico
            └── src/
                ├── main.py       # Lógica interna de automatización en KGeoMIP (Excel)
                ├── controllers/
                │   ├── manager.py          # Gestor de red (carga y conversión NPY)
                │   └── strategies/
                │       ├── geometric.py    # Algoritmo de costos base sobre hipercubo
                │       └── k_geometric.py  # Algoritmo KGeoMIP (k-partición geométrica)
                └── models/
                    └── core/
                        └── system.py       # Modelo System y NCube del subproyecto
```

### Capacidades y límites de escala del sistema

Ambos subproyectos adaptan dinámicamente sus estrategias según el tamaño del sistema para garantizar el mejor compromiso entre exactitud matemática y tiempo de procesamiento:

#### A. Estrategia KQNodes
1. **Sistemas Pequeños ($N \le 2$ variables de futuro):** Ejecuta una **Búsqueda Exhaustiva Exacta (Fuerza Bruta)**. Evalúa todas las posibles $k$-particiones posibles (números de Stirling del segundo tipo) en milisegundos y garantiza encontrar el mínimo global absoluto.  
2. **Sistemas Medianos a Grandes ($7 \le N \le 22$ variables):** Emplea el algoritmo **KQNodes**. Construye un árbol de fusiones jerárquicas submodulares (árbol Q) para enfocar la búsqueda en las fronteras de menor pérdida, y luego aplica una **Búsqueda Local de Vecindario Variable (VND)** para refinar la solución. Encuentra la solución en menos de un segundo, reduciendo exponencialmente el tiempo frente a la Fuerza Bruta.  
3. **Sistemas Masivos ($N > 22$ variables):** El programa activa un **Bypass estructural automático**. Salta la construcción costosa del árbol Q en memoria y genera una partición inicial instantánea basada en el acoplamiento directo de variables, refinándola localmente. Esto permite calcular tri-particiones de sistemas masivos de 25 variables ($N=25$, que representan $33,554,432$ estados de transición) en tan solo **0.71 segundos** sin agotar la memoria de la máquina (evitando errores OOM).

#### B. Estrategia KGeoMIP
1. **Sistemas Pequeños y Medianos ($N < 20$ variables):** Calcula de forma exacta el recorrido bottom-up de transiciones en todos los niveles Hamming del hipercubo. Proporciona una tabla de costos muy detallada que permite evaluar la separación de bloques a través de la frontera ordenada de ramificación y acotación (Branch and Bound).
2. **Sistemas Grandes ($N \ge 20$ variables):** Activa de forma automática el **Modo Grande**. Restringe el cálculo recursivo de la tabla de costos únicamente al primer nivel Hamming (distancia 1). Esto reduce drásticamente el uso de memoria RAM y CPU al evitar la explosión combinatoria de estados intermedios en el hipercubo, manteniendo una precisión óptima en la estimación de la pérdida.

---

## 2.2 Requisitos del Sistema

### Sistemas operativos compatibles

El software está escrito en código de Python estándar y es compatible con los siguientes entornos:

* **Windows (Entorno recomendado):** Windows 10 y Windows 11 de 64 bits.  
* **Linux:** Ubuntu 20.04 LTS o superior, Debian, CentOS o RedHat.  
* **macOS:** macOS 12 (Monterey) o superior (compatible con arquitecturas Intel y Apple Silicon).

### Especificaciones de hardware recomendadas

| Recurso | Requisitos Mínimos (Sistemas $N \le 15$) | Requisitos Recomendados (Sistemas $15 < N \le 25$) |
| :--- | :--- | :--- |
| **Procesador (CPU)** | Intel Core i3 o AMD Ryzen 3 (2 núcleos, 2.0 GHz) | Intel Core i5/i7 o AMD Ryzen 5/7 (4+ núcleos, 3.2 GHz o más) |
| **Memoria RAM** | 4 Gigabytes (GB) | 8 Gigabytes (GB) a 16 Gigabytes (GB) para evitar swapping con redes de $N=25$ |
| **Almacenamiento** | 100 Megabytes (MB) de espacio disponible | 2 Gigabytes (GB) de espacio disponible (necesario para albergar matrices `.npy` gigantes) |

> [!WARNING]
> **Sobre la carga de matrices masivas:** La carga en memoria de matrices de probabilidad de transición (TPM) para redes de 25 variables (como `N25A.npy`) requiere aproximadamente 838 MB de almacenamiento en disco en formato binario. Al cargarse en NumPy, el sistema operativo requiere memoria física libre suficiente para evitar que la máquina empiece a escribir en el disco duro (swapping), lo cual degradaría drásticamente los tiempos de procesamiento.

### Entorno de software requerido

* **Python:** Versión **3.11** o **3.12** de 64 bits instalada en el sistema.  
* **Administrador de Paquetes:** `pip` (incluido por defecto en Python) o la herramienta moderna de alto rendimiento **`uv`**.

---

## 2.3 Instalación Paso a Paso

### Paso 1: Descarga y extracción del proyecto

1. Obtenga el repositorio del proyecto en su máquina local. Si cuenta con el cliente de Git configurado en su consola, ejecute:  
   ```bash
   git clone https://github.com/CamiloNinoG/ADA_2026_1_KQ_NODES
   cd ADA_2026_1_KQ_NODES
   ```
2. Si cuenta con un archivo comprimido (`.zip` o `.tar.gz`), descomprímalo en un directorio local de su preferencia, por ejemplo: `C:\Users\SuUsuario\Proyectos\ADA_2026_1_KQ_NODES`

### Paso 2: Creación y activación del entorno virtual

El uso de un entorno virtual garantiza que las librerías del proyecto no interfieran con otras instalaciones de Python en su computadora. Abra una terminal de comandos (PowerShell en Windows, o Terminal en Linux/macOS) en el directorio raíz del proyecto y elija uno de los siguientes métodos:

#### Opción A: Usando Python estándar (Flujo clásico)

En Windows (PowerShell):
```powershell
# 1. Crear el entorno virtual en la carpeta .venv
python -m venv .venv
# 2. Activar el entorno virtual en su sesión de PowerShell
.venv\Scripts\Activate.ps1
```

En Linux o macOS:
```bash
# 1. Crear el entorno virtual
python3 -m venv .venv
# 2. Activar el entorno virtual
source .venv/bin/activate
```

#### Opción B: Usando la herramienta ultra rápida `uv` (Recomendado)

`uv` es un administrador de entornos y paquetes desarrollado en Rust extremadamente rápido. Si decide usarlo:
```bash
# 1. Instalar uv a nivel global o de usuario
pip install uv
# 2. Sincronizar el entorno y crear la carpeta .venv en un solo paso
uv sync
```

### Paso 3: Instalación de las dependencias requeridas

Si optó por la **Opción A (Python estándar)**, con el entorno virtual activado, ejecute el siguiente comando en la consola para instalar las librerías necesarias:

```bash
# Asegurar que pip esté actualizado
python -m pip install --upgrade pip
# Instalar los paquetes clave de análisis numérico e interfaz
pip install numpy pandas openpyxl colorama pyinstrument questionary
```

> [!NOTE]
> **Detalle de las dependencias instaladas:**
> * `numpy` (v1.24+): Manejo algebraico de matrices de probabilidad e implementación de la distancia EMD.  
> * `pandas` (v2.0+): Lectura estructurada de filas y celdas del archivo de origen de Excel.  
> * `openpyxl` (v3.1+): Escritura directa sobre plantillas XLSX manteniendo formatos sin dañar el archivo original.  
> * `colorama`: Habilita la salida con colores ANSI en terminales de comandos de Windows.  
> * `pyinstrument`: Profiler utilizado para registrar cuellos de botella y perfilar los tiempos exactos de cómputo.
> * `questionary`: Generación de menús interactivos interactivos por consola.

### Verificación de la instalación del entorno

Antes de ejecutar el solver, verifique que el entorno virtual esté activo y las librerías se hayan enlazado correctamente con sus versiones recomendadas. Ejecute los siguientes comandos de diagnóstico en su terminal:

1. **Verificar la versión de Python activa:**  
   ```bash
   python --version
   ```
   *Salida esperada:* `Python 3.11.x` o `Python 3.12.x`.  
2. **Verificar la ubicación de pip:**  
   ```bash
   pip --version
   ```
   *Salida esperada:* Debe retornar una ruta que apunte a la carpeta local `.venv` del proyecto (ej: `...\ADA_2026_1_KQ_NODES\.venv\Scripts\pip`).  
3. **Listar paquetes instalados:**
   Si usó Python estándar:  
   ```bash
   pip list
   ```
   Si usó la herramienta `uv`:  
   ```bash
   uv pip list
   ```
   *Debe confirmar que figuren en la lista con versiones compatibles:* `numpy`, `pandas`, `openpyxl`, `colorama`, `pyinstrument` y `questionary`.  
4. **Verificar la importación exitosa de todas las librerías:** Este comando ejecuta una prueba rápida en Python para importar los paquetes instalados y verificar que no existan fallos de carga o de DLLs:  
   ```bash
   python -c "import numpy, pandas, openpyxl, colorama, pyinstrument, questionary; print('Verificación de dependencias exitosa: todas las librerías se importaron correctamente.')"
   ```
   *Salida esperada:* `Verificación de dependencias exitosa: todas las librerías se importaron correctamente.`  
5. **Verificar soporte de codificación UTF-8 en consola:** Para que el terminal de Windows represente adecuadamente los símbolos de las particiones (`⎛ ⎞`, `∅`, etc.), se recomienda forzar la codificación en UTF-8 con la bandera `-X utf8`:  
   ```bash
   python -X utf8 -c "import sys; print(f'Codificación del terminal: {sys.stdout.encoding}')"
   ```
   *Salida esperada:* `Codificación del terminal: utf-8`

---

## 2.4 Video Tutorial de Instalación y Uso

Para facilitar el despliegue del sistema y la comprensión de sus resultados por parte de los usuarios finales, se ha producido un video demostrativo detallado:

* **Enlace de descarga/acceso:** [Video Tutorial KQNodes (MP4)](file:///C:/Users/The%20Real/.gemini/antigravity/scratch/KQNODES/video_tutorial.mp4) (o disponible en los archivos del entregable).  
* **Duración del video:** 12 minutos.  
* **Contenido cubierto en el tutorial:**  
  * **Instalación desde cero:** Descarga y descompresión del proyecto, inicialización del entorno virtual (`venv` / `uv`) e instalación de las dependencias requeridas.  
  * **Verificación del entorno:** Corrida de los comandos de diagnóstico detallados en la sección 2.3.  
  * **Ejemplo de ejecución básico:** Configuración de parámetros en `src/main.py` (red, variables de alcance y mecanismo, k=2), corrida del software e interpretación paso a paso de los resultados y tiempos.  
  * **Casos avanzados:** Ejecución de pruebas integradas y automatización masiva con archivos Excel (`tests/estrategias.py`).

---

## 2.5 Guía de Uso del Sistema

El framework **K-MIP/IIT** ofrece dos perfiles de uso claramente diferenciados según las necesidades técnicas y el nivel de familiaridad del usuario con la codificación en Python:

---

### Perfil de Usuario No Avanzado: Ejecución por CLI e Interfaz Interactiva

Este perfil está diseñado para usuarios que desean evaluar subsistemas de forma directa sin necesidad de editar código fuente en Python o configurar archivos de automatización estructurados.

#### A. Interfaz Consola Interactiva (Recomendada)
El archivo unificado [main.py](file:///home/jacobo/escritorio/ADA_2026_1_KQ_NODES/main.py) ubicado en la raíz del repositorio actúa como un asistente guiado interactivo.

1.  Abra una terminal de comandos en la carpeta raíz del repositorio.
2.  Inicie el asistente interactivo:
    ```bash
    uv run main.py
    ```
    *(O `.venv/bin/python main.py` si utiliza el flujo clásico)*.
3.  El asistente le pedirá interactuar con una serie de preguntas utilizando las flechas del teclado y la tecla Enter:
    *   **Algoritmo**: Seleccione `QNodes` (Algoritmo Q) o `KGeoMIP` (Método Geométrico).
    *   **Tamaño de la TPM**: Seleccione la dimensión del sistema ($10$, $15$, $20$, $22$, $25$).
    *   **Valor de k**: Defina en cuántos bloques subdividir el subsistema ($2$, $3$, $4$, $5$).
    *   **Estado Inicial**: Seleccione entre las opciones automáticas (`Todo en 0`, `1 seguido de ceros`) o digite manualmente el vector de bits.
    *   **Condiciones / Alcance / Mecanismo**: Defina las máscaras seleccionando `Todo en 1` o ingrese el vector binario manualmente.
4.  El asistente llamará automáticamente al algoritmo seleccionado y mostrará el objeto solución final con la partición formateada en la terminal.

#### B. Ejecución CLI Directa (`exec_user.py`)
Tanto el subproyecto `QNodes` como `GeoMIP/src/Method2_Dynamic_Programming_Reformulation` contienen un script llamado `exec_user.py`. Estos scripts permiten invocar los algoritmos directamente mediante parámetros de línea de comandos (flags), ideal para automatizaciones externas breves o integración rápida en bash.

Las banderas disponibles para ambos scripts son:
*   `--estado`: Vector binario del estado inicial (ej. `1000000000`).
*   `--condiciones`: Vector binario de condiciones de fondo (ej. `1111111111`).
*   `--alcance`: Máscara binaria del alcance en el futuro (ej. `1101101101`).
*   `--mecanismo`: Máscara binaria del mecanismo en el presente (ej. `1101101101`).
*   `--k`: Entero con la cantidad de particiones a evaluar ($2, 3, 4, 5$).
*   `--tamano`: Dimensión de la TPM a cargar.

**Ejemplo de ejecución para QNodes:**
```bash
cd QNodes
uv run exec_user.py --estado 1000000000 --condiciones 1111111111 --alcance 1101101101 --mecanismo 1101101101 --k 3 --tamano 10
```

**Ejemplo de ejecución para KGeoMIP:**
```bash
cd GeoMIP/src/Method2_Dynamic_Programming_Reformulation
uv run exec_user.py --estado 1000000000 --condiciones 1111111111 --alcance 1101101101 --mecanismo 1101101101 --k 3 --tamano 10
```

---

### Perfil de Usuario Avanzado: Ejecución y Automatización por Lotes desde Excel

Este perfil está destinado a investigadores que necesitan ejecutar análisis masivos sobre plantillas estructuradas de Excel, requiriendo modificar directamente scripts internos para configurar comportamientos lógicos personalizados.

#### A. Automatización de pruebas por lotes en QNodes
La ejecución por lotes de QNodes lee la configuración de subsistemas mapeados por letras (ej: "A,B,C") desde un Excel de entrada e inyecta la partición mínima, pérdida y tiempo por cada valor de $k$ ($2 \le k \le 5$).

*   **Archivo Excel de entrada**: `QNodes/src/results/pruebas.xlsx`
*   **Archivo Excel de salida**: `QNodes/src/results/pruebas_con_resultados.xlsx`
*   **Procedimiento**:
    1.  Abra el editor y navegue a `QNodes/src/main.py`.
    2.  Modifique la constante `LONGITUD_ELEMENTOS` en la línea 15 para definir el tamaño del sistema a evaluar (ej. `LONGITUD_ELEMENTOS = 10` cargará la hoja `10A-Elementos`).
    3.  Ajuste el rango de particiones si desea limitar el procesamiento (línea 97: `for k in range(2, 6)`).
    4.  Ubicado en la carpeta `QNodes`, ejecute el script:
        ```bash
        uv run exec.py
        ```
    5.  Al finalizar, consulte el archivo de salida generado, que contendrá todas las métricas inyectadas de forma nativa.

#### B. Automatización de pruebas por lotes en KGeoMIP
El script de KGeoMIP procesa múltiples filas de un archivo Excel de forma concurrente mediante multiprocessing en Python (aislando la ejecución de cada subsistema en un proceso con timeout para evitar cuellos de botella en redes muy grandes).

*   **Archivo Excel de entrada/salida**: `GeoMIP/results/DatosPruebas2026_1.xlsx` (o la ruta en la variable de entorno `GEOMIP_INPUT_XLSX`).
*   **Procedimiento**:
    1.  Abra el editor y navegue a `GeoMIP/src/Method2_Dynamic_Programming_Reformulation/src/main.py`.
    2.  Modifique la función `iniciar()` al final del archivo:
        ```python
        def iniciar():
            ruta_excel = Path(os.getenv("GEOMIP_INPUT_XLSX", str(GEOMIP_ROOT / "results" / "DatosPruebas2026_1.xlsx")))
            for k in range(2, 3): # Defina aquí el rango de K a evaluar
                ejecutar_desde_excel(
                    ruta_excel=ruta_excel,
                    hoja=8,             # Índice de la hoja del Excel a leer
                    k=k,
                    tamaño_estado=10,   # Dimensión de la TPM (10, 15, 20, 22, 25)
                    cantidad=1          # Cantidad de filas consecutivas a evaluar
                )
        ```
    3.  Ubicado en el subdirectorio `GeoMIP/src/Method2_Dynamic_Programming_Reformulation`, ejecute el script:
        ```bash
        uv run exec.py
        ```
    4.  El script actualizará de forma directa las celdas del Excel de origen y mostrará los resultados intermedios por terminal.

---

## 2.6 Opciones y Parámetros Avanzados

Esta sección está destinada a usuarios e investigadores que requieren ajustar el comportamiento interno del algoritmo, ejecutar pruebas masivas mediante plantillas de Excel, o realizar optimizaciones para sistemas de dimensiones específicas.

### Configuración dinámica del pool de candidatos en KQNodes

En el archivo [candidates.py](file:///home/jacobo/escritorio/ADA_2026_1_KQ_NODES/QNodes/src/strategies/kqnodes/candidates.py), el software adapta dinámicamente el tamaño de la búsqueda heurística según el número de variables futuras $N$ para mantener una alta velocidad sin perder precisión causal. Estos parámetros controlan la generación de candidatos:

* **`top_q`:** Número máximo de candidatos de corte extraídos del historial de fusiones del Algoritmo Q (árbol de fusiones).  
* **`top_struct`:** Número de configuraciones estructurales heurísticas generadas por balanceo cíclico y cercanía.  
* **`max_pairs`:** Número máximo de combinaciones cruzadas permitidas en el pool.  
* **`tope`:** Límite superior de candidatos de emparejamiento evaluados en la búsqueda de local.

#### Valores dinámicos por defecto:

* **Sistemas Grandes ($N \ge 20$):** `top_q = 2`, `top_struct = 2`, `max_pairs = 4`, `tope = 3`.  
  * *Razón:* Minimiza la sobrecarga computacional en redes con millones de estados.  
* **Sistemas Medianos ($15 \le N < 20$):** `top_q = 4`, `top_struct = 3`, `max_pairs = 12`, `tope = 30`.  
* **Sistemas Pequeños ($N < 15$):** `top_q = 8`, `top_struct = 5`, `max_pairs = 30`, `tope = 50`.

---

### Límites del refinamiento local (VND) en KQNodes

La Búsqueda Local de Vecindario Variable (VND) en [refinement.py](file:///home/jacobo/escritorio/ADA_2026_1_KQ_NODES/QNodes/src/strategies/kqnodes/refinement.py) optimiza la partición seleccionada aplicando dos vecindarios de movimientos (Shift e Intercambio/Swap). Su presupuesto se escala automáticamente en función de la cantidad de variables futuras $N$:

* **`max_pasos`:** Controla la cantidad máxima de iteraciones locales permitidas.  
  * $N \ge 23$: `max_pasos = 0` *(la búsqueda local se desactiva por completo para prevenir retrasos en sistemas masivos)*.  
  * $20 \le N < 23$: `max_pasos = 100` *(se limita la iteración para proteger la CPU)*.  
  * $N < 20$: `max_pasos = 20` *(permite convergencia libre hasta el óptimo local)*.  
* **`permite_swaps`:** Booleano que habilita el vecindario de intercambio de elementos entre bloques.  
  * Desactivado para $N \ge 20$ (`permite_swaps = False`), limitando la búsqueda local a movimientos simples de inserción (*shift*) para mantener tiempos de respuesta de milisegundos.

---

### Configuración de la estrategia Branch and Bound en KGeoMIP

En el archivo [k_geometric.py](file:///home/jacobo/escritorio/ADA_2026_1_KQ_NODES/GeoMIP/src/Method2_Dynamic_Programming_Reformulation/src/controllers/strategies/k_geometric.py), la estrategia `aplicar_estrategia_k_geometric` implementa una poda estructurada para acelerar el descarte de particiones que no tienen probabilidad de ser el óptimo global:

* **Cota de Pérdida (`min_emd`)**: Se actualiza dinámicamente con el valor de la EMD de la mejor partición completa de tamaño $k$ encontrada. Si el análisis de una rama intermedia reporta un coste superior a esta cota, la rama se descarta (`break` temprano).
* **Frontera de Búsqueda (`frontera`)**: Estructura de tipo lista ordenada que implementa la búsqueda priorizada. Se extraen continuamente los estados con menor coste de transición Hamming acumulado, garantizando que el algoritmo explore primero las regiones del espacio de estados más prometedoras.

---

### Modos de operación y límites físicos

| Modo de Operación | Criterio de Activación | Descripción Técnica | Algoritmo Afectado |
| :--- | :--- | :--- | :--- |
| **Exhaustivo (Fuerza Bruta)** | $N \le 8$ variables futures | Evalúa el total de combinaciones del número de Stirling del segundo tipo de forma exacta. | QNodes / KGeoMIP |
| **Heurístico Submodular** | $7 \le N \le 22$ variables | Genera candidatos a partir de la estructura del árbol de fusiones Q y refina con VND. | QNodes |
| **Bypass Estructural** | $N > 22$ variables | Desactiva el árbol de fusiones Q. Genera y evalúa una sola partición estructural por balanceo. | QNodes |
| **Modo Pequeño** | $N < 20$ variables | Calcula y memoiza los costos en todos los niveles Hamming de transición del hipercubo. | KGeoMIP |
| **Modo Grande** | $N \ge 20$ variables | Calcula los costos de transición restringiéndolos únicamente a distancia Hamming 1. | KGeoMIP |

---

### Automatización de pruebas masivas en Excel

#### Estructura y lectura de Excel en QNodes (`pruebas.xlsx`)
El script carga la plantilla de entrada ubicada en `src/results/pruebas.xlsx` y lee la configuración de red y las variables del subsistema:
* **Configuración Superior (Filas 1 a 3):**  
  * **Celda B1 (Estado inicial):** Estado activo/inactivo del sistema al inicio de la corrida (Ej: `1000000000` en formato de 10 bits).  
  * **Celda B2 (Sistema):** El universo de variables consideradas (Ej: `ABCDEFGHIJ`).  
  * **Celda B3 (Sistema Candidato):** Las variables que forman el subsistema causal.  
* **Lectura de Filas del Subsistema (Fila 5 en adelante):** El script está programado en Pandas para omitir las primeras 4 filas de cabecera (`skiprows=4`), detectando los nombres de columna en la fila 5:  
  * **Columna A (`#Prueba`):** Índice o ID numérico del caso de prueba.  
  * **Columna B (`Alcance o Purview (t+1)`):** Lista de letras de variables a evaluar en el futuro (Ej: `ACEGI`).  
  * **Columna C (`Mecanismo(t)`):** Lista de letras de variables a evaluar en el presente (Ej: `ACEGI`).

> [!NOTE]
> **Conversión interna a binario:** Las cadenas de letras (como `ACEGI`) se procesan dinámicamente mediante la función `texto_a_binario(texto, universo)`. Si el universo es de 10 bits (`ABCDEFGHIJ`), `ACEGI` se convierte automáticamente en la máscara binaria `"1010101010"`.

---

#### Mapeo comparativo de lectura y escritura en hojas de cálculo

Al inyectar los resultados de los experimentos (Partición, Pérdida y Tiempo de Cómputo), ambos algoritmos mapean de forma diferente sus celdas de destino en las respectivas plantillas Excel:

| Parámetro $k$ | Columnas Resultantes en QNodes (`pruebas_con_resultados.xlsx`) | Columnas Resultantes en KGeoMIP (`DatosPruebas2026_1.xlsx`) |
| :--- | :--- | :--- |
| **$k=2$ (Biparticiones)** | Columnas **D, E, F** (Índices 4, 5, 6) | Columnas **K, L, M** |
| **$k=3$ (Tri-particiones)** | Columnas **G, H, I** (Índices 7, 8, 9) | Columnas **Q, R, S** |
| **$k=4$ (4-Particiones)** | Columnas **J, K, L** (Índices 10, 11, 12) | Columnas **Z, AA, AB** |
| **$k=5$ (5-Particiones)** | Columnas **M, N, O** (Índices 13, 14, 15) | Columnas **AI, AJ, AK** |

*   La pérdida mínima de información se guarda en el Excel como un tipo `float` numérico nativo de Python, permitiendo al usuario realizar formateos numéricos personalizados de celdas o gráficos automáticos sin pérdida de precisión decimal.

---

### Optimización y consejos de rendimiento

Para optimizar el rendimiento al procesar bases de datos y plantillas masivas, considere los siguientes lineamientos:

1. **Gestión de Procesos en KGeoMIP:** El script de GeoMIP Método 2 utiliza la API de `multiprocessing` para aislar el cálculo de cada fila de Excel. Puede configurar el tiempo de timeout (línea 232 de `src/main.py`) para definir cuándo descartar filas atascadas (por defecto: `timeout=3600` segundos).
2. **Caché en QNodes:** El framework QNodes utiliza internamente un diccionario de caché para `bipartir_y_emd`. Si realiza pruebas consecutivas del mismo subsistema dentro de un script avanzado, no olvide ejecutar `analizador.reset_estado()` para liberar la memoria caché acumulada y mantener el consumo de RAM bajo control.
3. **Caché NumPy (.npy)**: Al cargar redes por primera vez, el proceso puede demorar varios segundos mientras lee el CSV plano. Una vez generado el archivo `.npy` correspondiente en la carpeta `.samples/`, asegúrese de no borrarlo para que las ejecuciones posteriores comiencen instantáneamente.
