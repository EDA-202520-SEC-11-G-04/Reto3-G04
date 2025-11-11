import csv
import time
import DataStructures.List.array_list as list
import DataStructures.List.single_linked_list as sl
import DataStructures.Tree.binary_search_tree as bst
from datetime import datetime

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog=list.new_list()
    return catalog


# Funciones para la carga de datos


def load_data(control, filename):
    """
    Carga los datos del archivo CSV en el catálogo.
    Retorna el catálogo actualizado si todo sale bien, o None si hay error.
    """
    start_time = time.perf_counter()

    try:
        csv.field_size_limit(2147483647)
        with open(filename, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Ignorer lignes vides ou malformées
                if not row or all(v is None or v == "" for v in row.values()):
                    continue

                clean_row = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    value = value.strip() if value else "Unknown"
                    clean_row[key] = value if value != "" else "Unknown"

                list.add_last(control, clean_row)

    except Exception as e:
        print(f" Error al leer el archivo: {e}")
        return None

    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000
    total = list.size(control)

    # Empaquetar los datos para la vista
    result = {
        "catalog": control,
        "elements": control["elements"],
        "elapsed": elapsed,
        "total": total
    }

    return result


def req_1(catalog, airline_code, delay_range):
    """
    Requerimiento 1:
    Dada una aerolínea, identificar los vuelos con retraso en salida dentro de un rango de minutos.
    Usa un Árbol Binario de Búsqueda (BST) para organizar los vuelos por retraso.
    """
    start_time = time.perf_counter()
    min_delay, max_delay = delay_range

    tree = bst.new_map()
    result_list = list.new_list()

    for flight in catalog["elements"]:
        if flight.get("carrier", "") != airline_code:
            continue

        dep = flight.get("dep_time", "")
        sched = flight.get("sched_dep_time", "")
        if not dep or not sched or dep == "Unknown" or sched == "Unknown":
            continue

        try:
            dep_minutes = _time_to_minutes(dep)
            sched_minutes = _time_to_minutes(sched)
            delay = dep_minutes - sched_minutes

            # Correction si vol passe minuit
            if delay < -720:
                delay += 1440
            elif delay > 720:
                delay -= 1440
        except:
            continue

        # Filtrer par le range
        if min_delay <= delay <= max_delay:
            flight_data = {
                "ID": flight.get("id", ""),
                "Vuelo": flight.get("flight", ""),
                "Fecha": flight.get("date", ""),
                "Aerolínea": flight.get("name", ""),
                "Código": flight.get("carrier", ""),
                "Origen": flight.get("origin", ""),
                "Destino": flight.get("dest", ""),
                "Retraso (min)": delay
            }

            delay_key = int(delay)  # ✅ clé uniforme

            if bst.contains(tree, delay_key):
                node_list = bst.get(tree, delay_key)
                list.add_last(node_list, flight_data)
                bst.put(tree, delay_key, node_list)
            else:
                new_list = list.new_list()
                list.add_last(new_list, flight_data)
                bst.put(tree, delay_key, new_list)

    keys = bst.key_set(tree)
    size_keys = sl.size(keys)

    for i in range(0, size_keys ):
        delay_key = sl.get_element(keys, i)
        delay_key = int(delay_key)
        flights_with_delay = bst.get(tree, delay_key)
        if flights_with_delay:
            for j in range(0, list.size(flights_with_delay)):
                list.add_last(result_list, list.get_element(flights_with_delay, j))

    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000
    total = list.size(result_list)

    # Échantillon d’affichage
    if total > 10:
        flights_to_display = result_list["elements"][:5] + result_list["elements"][-5:]
    else:
        flights_to_display = result_list["elements"]

    return {
        "elapsed": elapsed,
        "total": total,
        "flights": flights_to_display
    }


def _time_to_minutes(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m




def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
