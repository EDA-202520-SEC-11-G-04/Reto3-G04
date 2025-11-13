import sys
from tabulate import tabulate
import App.logic as logic
from datetime import datetime
import DataStructures.List.array_list as list

def new_logic():
    """
    Crea una instancia del controlador (el catálogo).
    """
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos de vuelos desde un archivo CSV y muestra un resumen.
    """
    filename = input("Indiquez le chemin du fichier CSV: ")
    result = logic.load_data(control, filename)

    if not result:
        print(" No se pudo cargar el archivo.")
        return control

    elapsed = result["elapsed"]
    total = result["total"]
    elements = result["elements"]

    print(f"\nArchivo cargado correctamente en {elapsed:.2f} ms.")
    print(f" Total de vuelos cargados: {total}")

    # Si hay elementos, mostrar los primeros y últimos 5
    if total > 0:
        sample = elements[:5] + elements[-5:] if total > 10 else elements
        filtered_data = []

        for flight in sample:
            filtered_data.append({
                "Fecha": flight.get("date", ""),
                "Salida": flight.get("dep_time", ""),
                "Llegada": flight.get("arr_time", ""),
                "Duración (min)": flight.get("air_time", ""),
                "Distancia (mi)": flight.get("distance", ""),
                "Aerolínea": flight.get("carrier", ""),
                "Origen": flight.get("origin", ""),
                "Destino": flight.get("dest", "")
            })

        print("\nPrimeros y últimos vuelos cargados:")
        print(tabulate(filtered_data, headers="keys", tablefmt="grid", showindex=True))

    return result["catalog"]


def print_data(control, id):
    """Función que imprime un vuelo según su ID (placeholder)."""
    return logic.get_data(control, id)


def print_req_1(control):
    """
    Imprime la solución del Requerimiento 1 en consola.
    """
    airline_code = input("Ingrese el código de la aerolínea (ej: 'UA'): ").strip().upper()
    min_delay = int(input("Ingrese el retraso mínimo (en minutos): "))
    max_delay = int(input("Ingrese el retraso máximo (en minutos): "))

    result = logic.req_1(control, airline_code, (min_delay, max_delay))

    print(f"\n Tiempo de ejecución: {result['elapsed']:.2f} ms")
    print(f"  Total de vuelos encontrados: {result['total']}")

    if result["total"] > 0:
        print("\n Vuelos filtrados:")
        print(tabulate(result["flights"], headers="keys", tablefmt="grid", showindex=True))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n=== Requerimiento 3 ===")
    carrier = input("Código de aerolínea (ej: 'AA', 'EV'): ").strip().upper()
    dest = input("Código aeropuerto destino (ej: 'JFK'): ").strip().upper()
    dist_min = int(input("Distancia mínima (millas): "))
    dist_max = int(input("Distancia máxima (millas): "))

    result = logic.req_3(control, carrier, dest, (dist_min, dist_max))

    if not result or result["total_flights"] == 0:
        print("\n No se encontraron vuelos que cumplan los criterios.")
        return

    print(f"\n Tiempo de ejecución: {result['elapsed']} ms")
    print(f" Total de vuelos encontrados: {result['total_flights']}")
    
    if result["showing_sample"]:
        print("📋 Mostrando primeros 5 y últimos 5 vuelos\n")
    else:
        print("📋 Mostrando todos los vuelos\n")

    # Preparar tabla de resultados
    table = []
    flights = result["flights"]
    
    for i in range(0, list.size(flights)):
        f = list.get_element(flights, i)
        
        table.append({
            "ID": f["ID"],
            "Código": f["Código"],
            "Fecha": f["Fecha"],
            "Aerolínea": f["Aerolínea"],
            "Carrier": f["Carrier"],
            "Origen": f["Origen"],
            "Destino": f["Destino"],
            "Distancia (mi)": f["Distancia"]
        })

    print(tabulate(table, headers="keys", tablefmt="grid", showindex=True))


def print_req_4(control):
    print("\n=== Requerimiento 4 ===")
    date_min = input("Fecha inicial (YYYY-MM-DD): ").strip()
    date_max = input("Fecha final (YYYY-MM-DD): ").strip()
    time_min = input("Hora de inicio (HH:MM o HHMM): ").strip()
    time_max = input("Hora final (HH:MM o HHMM): ").strip()
    n = int(input("Cantidad de aerolíneas a mostrar (N): "))

    result = logic.req_4(control, (date_min, date_max), (time_min, time_max), n)

    if not result or result["total_airlines"] == 0:
        print("\n No se encontraron aerolíneas en el rango indicado.")
        return

    print(f"\n Tiempo de ejecución: {result['elapsed']} ms")
    print(f"  Total de aerolíneas mostradas: {result['total_airlines']}\n")

    table = []
    airlines = result["airlines"]
    for i in range(0, list.size(airlines)):
        a = list.get_element(airlines, i)
        m = a["Vuelo mínimo"]

        table.append({
            "Código": a["Carrier"],
            "N° Vuelos": a["Num vuelos"],
            "Dur Prom (min)": a["Duración promedio"],
            "Dist Prom (mi)": a["Distancia promedio"],
            "Vuelo ID": m["ID"],
            "Cod Vuelo": m["Código"],
            "Fecha": m["Fecha"],
            "Hora Salida": m["Hora salida"],
            "Origen": m["Origen"],
            "Destino": m["Destino"],
            "Duración (min)": m["Duración"],
        })

    print(tabulate(table, headers="keys", tablefmt="grid", showindex=True))


def print_req_5(control):
    print("\n=== Requerimiento 5 ===")
    date_min = input("Fecha inicial (YYYY-MM-DD): ").strip()
    date_max = input("Fecha final (YYYY-MM-DD): ").strip()
    dest = input("Código aeropuerto destino (ej: 'JFK'): ").strip().upper()
    n = int(input("Cantidad de aerolíneas a mostrar (N): "))

    result = logic.req_5(control, (date_min, date_max), dest, n)

    if not result or result["total_airlines"] == 0:
        print("\n No se encontraron aerolíneas para el filtro indicado.")
        return

    print(f"\n Tiempo de ejecución: {result['elapsed']} ms")
    print(f" Aerolíneas mostradas: {result['total_airlines']}\n")

    table = []
    airlines = result["airlines"]
    for i in range(0, list.size(airlines) ):
        a = list.get_element(airlines, i)
        maxf = a["Vuelo max distancia"] if a["Vuelo max distancia"] else {}
        table.append({
            "Código": a["Carrier"],
            "N° Vuelos": a["Num vuelos"],
            "Dur Prom (min)": a["Duración promedio"],
            "Dist Prom (mi)": a["Distancia promedio"],
            "Puntualidad Prom (min)": a["Puntualidad promedio"],
            "ID MaxDist": maxf.get("ID", ""),
            "Vuelo": maxf.get("Vuelo", ""),
            "Fecha-Hora llegada": maxf.get("Fecha-Hora llegada", ""),
            "Origen": maxf.get("Origen", ""),
            "Destino": maxf.get("Destino", ""),
            "Duración (min)": maxf.get("Duración", "")
        })

    print(tabulate(table, headers="keys", tablefmt="grid", showindex=True))


def print_req_6(control):
    print("\n=== Requerimiento 6 ===")
    date_min = input("Fecha inicial (YYYY-MM-DD): ").strip()
    date_max = input("Fecha final (YYYY-MM-DD): ").strip()
    dist_min = int(input("Distancia mínima (millas): "))
    dist_max = int(input("Distancia máxima (millas): "))
    m = int(input("Cantidad de aerolíneas a mostrar (M): "))

    result = logic.req_6(control, (date_min, date_max), (dist_min, dist_max), m)

    if not result or result["total_airlines"] == 0:
        print("\n No se encontraron aerolíneas en el rango indicado.")
        return

    print(f"\n Tiempo de ejecución: {result['elapsed']} ms")
    print(f" Total de aerolíneas analizadas: {result['total_airlines']}\n")

    table = []
    airlines = result["airlines"]
    
    for i in range(0, list.size(airlines)):
        a = list.get_element(airlines, i)
        closest = a["Vuelo más cercano al promedio"] if a["Vuelo más cercano al promedio"] else {}
        
        table.append({
            "Código": a["Carrier"],
            "N° Vuelos": a["Num vuelos"],
            "Prom Retraso (min)": f"{a['Promedio retraso']:.2f}",
            "Estabilidad (σ)": f"{a['Estabilidad']:.2f}",
            "ID Vuelo": closest.get("ID", ""),
            "Cod Vuelo": closest.get("Código", ""),
            "Fecha-Hora salida": closest.get("Fecha-Hora salida", ""),
            "Origen": closest.get("Origen", ""),
            "Destino": closest.get("Destino", "")
        })

    print(tabulate(table, headers="keys", tablefmt="grid", showindex=True))

# Se crea la lógica asociado a la vista
control = new_logic()

def get_time():
    """Devuelve el instante de tiempo en milisegundos."""
    return float(datetime.perf_counter() * 1000)


def delta_time(start, end):
    """Devuelve la diferencia de tiempo entre dos muestras (ms)."""
    return float(end - start)

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
