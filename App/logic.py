import csv
import time
import math
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

    # Árbol BST: clave = minutos de retraso, valor = lista de vuelos
    tree = bst.new_map()
    result_list = list.new_list()

    # Recorrer todos los vuelos del catálogo
    for flight in catalog["elements"]:
        # Filtrar por aerolínea
        if flight.get("carrier", "") != airline_code:
            continue

        dep = flight.get("dep_time", "")
        sched = flight.get("sched_dep_time", "")
        if not dep or not sched or dep == "Unknown" or sched == "Unknown":
            continue

        # Calcular retraso en minutos
        try:
            dep_minutes = _time_to_minutes(dep)
            sched_minutes = _time_to_minutes(sched)
            delay = dep_minutes - sched_minutes

            # Ajuste por vuelos que cruzan medianoche
            if delay < -720:
                delay += 1440
            elif delay > 720:
                delay -= 1440
        except:
            continue

        # Filtrar por rango de retraso
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

            # Insertar vuelo en el árbol según el retraso
            delay_key = int(delay)
            if bst.contains(tree, delay_key):
                node_list = bst.get(tree, delay_key)
                list.add_last(node_list, flight_data)
                bst.put(tree, delay_key, node_list)
            else:
                new_list = list.new_list()
                list.add_last(new_list, flight_data)
                bst.put(tree, delay_key, new_list)

    # Obtener claves ordenadas (minutos de retraso)
    keys = bst.key_set(tree)
    size_keys = sl.size(keys)

    # Recorrer cada clave del árbol en orden
    for i in range(0, size_keys):
        delay_key = sl.get_element(keys, i)
        delay_key = int(delay_key)
        flights_with_delay = bst.get(tree, delay_key)
        if flights_with_delay:
            for j in range(0, list.size(flights_with_delay)):
                list.add_last(result_list, list.get_element(flights_with_delay, j))

    # Calcular tiempo total
    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000
    total = list.size(result_list)

    # Seleccionar los 5 primeros y 5 últimos vuelos
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


def sort_criteria_req4(a, b):
    """
    Criterio de ordenamiento:
    - Primero por número de vuelos (descendente)
    - En caso de empate, por código de aerolínea (ascendente)
    """
    if a["Num vuelos"] > b["Num vuelos"]:
        return True
    if a["Num vuelos"] < b["Num vuelos"]:
        return False
    return a["Carrier"] < b["Carrier"]


def req_4(catalog, date_range, time_range, n):
    """
    Requerimiento 4:
    Para un rango de fechas y franja horaria, identificar las N aerolíneas con más vuelos
    y, de cada una, obtener el vuelo con la menor duración.
    """
    start_time = time.perf_counter()

    # Convertir fechas y horas
    date_min = datetime.strptime(date_range[0], "%Y-%m-%d")
    date_max = datetime.strptime(date_range[1], "%Y-%m-%d")
    time_min_m = _time_to_minutes(time_range[0])
    time_max_m = _time_to_minutes(time_range[1])

    # Árbol BST: clave = aerolínea, valor = lista de vuelos
    airlines_tree = bst.new_map()

    # Filtrar vuelos por rango de fechas y franja horaria
    for flight in catalog["elements"]:
        # Validar fecha
        try:
            fdate = datetime.strptime(flight.get("date", ""), "%Y-%m-%d")
        except:
            continue
        if not (date_min <= fdate <= date_max):
            continue

        # Hora programada de salida
        sched = flight.get("sched_dep_time", "")
        if sched == "" or sched == "Unknown":
            continue
        try:
            sched_m = _time_to_minutes(sched)
        except:
            continue

        # Validar franja horaria
        if not (time_min_m <= sched_m <= time_max_m):
            continue

        # Código de aerolínea
        carrier = flight.get("carrier", "").strip().upper()
        if carrier == "":
            continue

        # Insertar vuelo en el árbol BST
        if bst.contains(airlines_tree, carrier):
            flights_list = bst.get(airlines_tree, carrier)
        else:
            flights_list = list.new_list()

        list.add_last(flights_list, flight)
        bst.put(airlines_tree, carrier, flights_list)

    # Calcular estadísticas por aerolínea
    carriers_results = list.new_list()
    keys = bst.key_set(airlines_tree)

    for i in range(0, sl.size(keys)):
        carrier_code = sl.get_element(keys, i)
        flights = bst.get(airlines_tree, carrier_code)
        if flights is None or list.size(flights) == 0:
            continue

        # Variables de acumulación
        count = 0
        sum_duration = 0.0
        dur_count = 0
        sum_distance = 0.0
        dist_count = 0
        min_flight = None
        min_duration = None
        min_sched_dt = None

        # Recorrer vuelos de la aerolínea
        for j in range(0, list.size(flights)):
            f = list.get_element(flights, j)
            count += 1

            # Duración (air_time)
            try:
                dur = float(f.get("air_time", ""))
                sum_duration += dur
                dur_count += 1

                # Buscar vuelo con menor duración
                if min_duration is None or dur < min_duration:
                    min_duration = dur
                    min_flight = f
                    sched_str = f.get("sched_dep_time", "")
                    if ":" not in sched_str:
                        sched_str = sched_str[:-2] + ":" + sched_str[-2:]
                    min_sched_dt = datetime.strptime(
                        f.get("date", "") + " " + sched_str, "%Y-%m-%d %H:%M"
                    )
                elif dur == min_duration:
                    # Si hay empate, usar vuelo más antiguo
                    sched_str = f.get("sched_dep_time", "")
                    if ":" not in sched_str:
                        sched_str = sched_str[:-2] + ":" + sched_str[-2:]
                    cur_dt = datetime.strptime(
                        f.get("date", "") + " " + sched_str, "%Y-%m-%d %H:%M"
                    )
                    if min_sched_dt is None or cur_dt < min_sched_dt:
                        min_flight = f
                        min_sched_dt = cur_dt
            except:
                pass

            # Distancia
            try:
                dist = float(f.get("distance", ""))
                sum_distance += dist
                dist_count += 1
            except:
                pass

        if count == 0:
            continue

        # Promedios
        avg_duration = round(sum_duration / dur_count, 2) if dur_count > 0 else 0.0
        avg_distance = round(sum_distance / dist_count, 2) if dist_count > 0 else 0.0

        # Crear resultado para la aerolínea
        entry = {
            "Carrier": carrier_code,
            "Num vuelos": count,
            "Duración promedio": avg_duration,
            "Distancia promedio": avg_distance,
            "Vuelo mínimo": {
                "ID": min_flight.get("id", "") if min_flight else "",
                "Código": min_flight.get("flight", "") if min_flight else "",
                "Fecha": min_flight.get("date", "") if min_flight else "",
                "Hora salida": min_flight.get("sched_dep_time", "") if min_flight else "",
                "Origen": min_flight.get("origin", "") if min_flight else "",
                "Destino": min_flight.get("dest", "") if min_flight else "",
                "Duración": min_duration if min_duration is not None else "",
            },
        }
        list.add_last(carriers_results, entry)

    # Ordenar resultados (descendente por número de vuelos)
    carriers_results = list.merge_sort(carriers_results, sort_criteria_req4)

    # Tomar las primeras N aerolíneas
    top_n = list.sub_list(carriers_results, 0, min(n, list.size(carriers_results)))

    # Tiempo total
    end_time = time.perf_counter()
    elapsed = round((end_time - start_time) * 1000, 2)

    return {
        "elapsed": elapsed,
        "total_airlines": list.size(top_n),
        "airlines": top_n,
    }


def sort_criteria_req5(a, b):
    """
    Criterio para req_5:
    - Primero por |Puntualidad promedio| ascendente (más puntual = más cerca de 0)
    - En caso de empate, por código de aerolínea ascendente
    """
    pa = abs(a["Puntualidad promedio"])
    pb = abs(b["Puntualidad promedio"])
    if pa < pb:
        return True
    if pa > pb:
        return False
    return a["Carrier"] < b["Carrier"]


def req_5(catalog, date_range, dest_code, n):
    """
    Requerimiento 5:
    Para un aeropuerto de destino y un rango de fechas, identificar las N aerolíneas
    con vuelos más puntuales y, de cada una, obtener el vuelo con la mayor distancia recorrida.
    """
    start_time = time.perf_counter()

    # Convertir fechas de entrada
    date_start = datetime.strptime(date_range[0], "%Y-%m-%d")
    date_end = datetime.strptime(date_range[1], "%Y-%m-%d")
    dest_code = dest_code.strip().upper()

    # Árbol BST: clave = aerolínea, valor = lista de vuelos filtrados
    airlines_tree = bst.new_map()

    # Filtrar vuelos por fecha y aeropuerto de destino
    for flight in catalog["elements"]:
        try:
            fdate = datetime.strptime(flight.get("date", ""), "%Y-%m-%d")
        except:
            continue
        if not (date_start <= fdate <= date_end):
            continue

        # Verificar destino
        dest = flight.get("dest", "").strip().upper()
        if dest != dest_code:
            continue

        # Obtener horas programadas y reales de llegada
        sched_arr = flight.get("sched_arr_time", "")
        arr = flight.get("arr_time", "")
        if not sched_arr or sched_arr == "Unknown" or not arr or arr == "Unknown":
            continue

        # Calcular puntualidad (diferencia en minutos)
        try:
            sched_arr_m = _time_to_minutes(sched_arr)
            arr_m = _time_to_minutes(arr)
            punct = arr_m - sched_arr_m
            # Ajustar si el vuelo pasa medianoche
            if punct < -720:
                punct += 1440
            elif punct > 720:
                punct -= 1440
        except:
            continue

        # Aerolínea
        carrier = flight.get("carrier", "").strip().upper()
        if carrier == "":
            continue

        # Insertar vuelo en el BST bajo la clave de la aerolínea
        if bst.contains(airlines_tree, carrier):
            flist = bst.get(airlines_tree, carrier)
        else:
            flist = list.new_list()
        list.add_last(flist, flight)
        bst.put(airlines_tree, carrier, flist)

    # 2️⃣ Calcular estadísticas y encontrar vuelo con mayor distancia por aerolínea
    carriers_results = list.new_list()
    keys = bst.key_set(airlines_tree)

    for i in range(0, sl.size(keys)):
        carrier = sl.get_element(keys, i)
        flights = bst.get(airlines_tree, carrier)
        if flights is None or list.size(flights) == 0:
            continue

        # Variables de acumulación
        count = 0
        sum_duration = 0.0
        dur_count = 0
        sum_distance = 0.0
        dist_count = 0
        sum_punct = 0.0
        punct_count = 0
        max_dist_flight = None
        max_distance = None

        # Recorrer todos los vuelos de la aerolínea
        for j in range(0, list.size(flights)):
            f = list.get_element(flights, j)
            count += 1

            # Duración promedio (air_time)
            try:
                at = float(f.get("air_time", ""))
                sum_duration += at
                dur_count += 1
            except:
                pass

            # Distancia promedio + vuelo con mayor distancia
            try:
                d = float(f.get("distance", ""))
                sum_distance += d
                dist_count += 1
                if max_distance is None or d > max_distance:
                    max_distance = d
                    max_dist_flight = f
            except:
                pass

            # Puntualidad (arr - sched)
            try:
                sched_arr = f.get("sched_arr_time", "")
                arr = f.get("arr_time", "")
                if sched_arr and arr and sched_arr != "Unknown" and arr != "Unknown":
                    sched_m = _time_to_minutes(sched_arr)
                    arr_m = _time_to_minutes(arr)
                    p = arr_m - sched_m
                    if p < -720:
                        p += 1440
                    elif p > 720:
                        p -= 1440
                    sum_punct += p
                    punct_count += 1
            except:
                pass

        # Si no hay vuelos válidos, continuar
        if count == 0:
            continue

        # Calcular promedios
        avg_duration = round((sum_duration / dur_count), 2) if dur_count > 0 else 0.0
        avg_distance = round((sum_distance / dist_count), 2) if dist_count > 0 else 0.0
        avg_punct = (sum_punct / punct_count) if punct_count > 0 else 0.0

        # Crear entrada de resultados
        entry = {
            "Carrier": carrier,
            "Num vuelos": count,
            "Duración promedio": avg_duration,
            "Distancia promedio": avg_distance,
            "Puntualidad promedio": avg_punct,
            "Vuelo max distancia": {
                "ID": max_dist_flight.get("id", "") if max_dist_flight else "",
                "Vuelo": max_dist_flight.get("flight", "") if max_dist_flight else "",
                "Fecha-Hora llegada": (max_dist_flight.get("date", "") + " " + 
                                       (max_dist_flight.get("arr_time", "") if ":" in max_dist_flight.get("arr_time","") 
                                        else (max_dist_flight.get("arr_time","")[:-2] + ":" + max_dist_flight.get("arr_time","")[-2:])))
                                       if max_dist_flight else "",
                "Origen": max_dist_flight.get("origin", "") if max_dist_flight else "",
                "Destino": max_dist_flight.get("dest", "") if max_dist_flight else "",
                "Duración": float(max_dist_flight.get("air_time", "")) if (max_dist_flight and max_dist_flight.get("air_time","") not in (None,"","Unknown")) else ""
            } if max_dist_flight else None
        }

        list.add_last(carriers_results, entry)

    # 3️⃣ Ordenar por puntualidad promedio (más cerca de 0 primero) y luego por código
    carriers_results = list.merge_sort(carriers_results, sort_criteria_req5)

    # 4️⃣ Tomar las primeras N aerolíneas
    top_n = list.sub_list(carriers_results, 0, min(n, list.size(carriers_results)))

    # Tiempo total de ejecución
    end_time = time.perf_counter()
    elapsed = round((end_time - start_time) * 1000, 2)

    return {
        "elapsed": elapsed,
        "total_airlines": list.size(top_n),
        "airlines": top_n
    }

    

def req_6(control, date_range, distance_range, m):
    
    start_time = time.perf_counter()
    
    # Extraer parametros
    date_min_str, date_max_str = date_range
    dist_min, dist_max = distance_range
    
    # Convertir fechas a objetos datetime
    try:
        date_min = datetime.strptime(date_min_str, "%Y-%m-%d")
        date_max = datetime.strptime(date_max_str, "%Y-%m-%d")
    except ValueError:
        return {"total_airlines": 0, "airlines": list.new_list(), "elapsed": 0}
    
    flights_by_distance = bst.new_map()
    
    # Insertar vuelos por distancia
    for flight in control["elements"]:
        
        # Filtrar por rango de fechas
        try:
            flight_date_str = flight.get("date", "Unknown")
            if flight_date_str == "Unknown":
                continue
            flight_date = datetime.strptime(flight_date_str, "%Y-%m-%d")
            
            if not (date_min <= flight_date <= date_max):
                continue
        except ValueError:
            continue
        
        # Obtener distancia
        try:
            distance_str = flight.get("distance", "Unknown")
            if distance_str == "Unknown" or distance_str == "":
                continue
            distance = float(distance_str)
        except (ValueError, TypeError):
            continue
        
        # Insertar en BST
        if bst.contains(flights_by_distance, distance):
            flight_list = bst.get(flights_by_distance, distance)
            list.add_last(flight_list, flight)
        else:
            flight_list = list.new_list()
            list.add_last(flight_list, flight)
            bst.put(flights_by_distance, distance, flight_list)
    
    # Obtener vuelos en el rango de distancias
    flights_in_range_values = bst.values(flights_by_distance, dist_min, dist_max)
    
    # Diccionario para agrupar por aerolinea
    airlines_data = {}
    
    # Procesar todos los vuelos que están en el rango de distancias
    for i in range(list.size(flights_in_range_values)):
        flight_list = list.get_element(flights_in_range_values, i)
        
        for j in range(list.size(flight_list)):
            flight = list.get_element(flight_list, j)
            delay = calculate_departure_delay(flight)
            if delay is None:
                continue
            carrier = flight.get("carrier", "Unknown")
            if carrier == "Unknown":
                continue
                
            if carrier not in airlines_data:
                airlines_data[carrier] = {
                    "delays": [],
                    "flights": []
                }
            
            airlines_data[carrier]["delays"].append(delay)
            airlines_data[carrier]["flights"].append(flight)
    
    # Calcular estadisticas para cada aerolinea
    airlines_stats = list.new_list()
    
    for carrier, data in airlines_data.items():
        delays = data["delays"]
        flights = data["flights"]
        
        if len(delays) == 0:
            continue
        
        average_delay = sum(delays) / len(delays)
        
        # Calcular desviacion
        variance = sum((d - average_delay) ** 2 for d in delays) / len(delays)
        std_deviation = math.sqrt(variance)
        
        # Encontrar vuelo con retraso cerca al promedio
        closest_flight = None
        min_difference = float('inf')
        
        for idx, delay in enumerate(delays):
            difference = abs(delay - average_delay)
            if difference < min_difference:
                min_difference = difference
                closest_flight = flights[idx]
        
        # Crear objeto de estadisticas de aerolinea
        airline_stat = {
            "carrier": carrier,
            "num_flights": len(delays),
            "average_delay": average_delay,
            "stability": std_deviation,
            "closest_flight": closest_flight
        }
        
        list.add_last(airlines_stats, airline_stat)
    
    def sort_criteria(a1, a2):
        diff = abs(a1["stability"] - a2["stability"])
        if diff < 0.0001:
            return a1["average_delay"] < a2["average_delay"]
        return a1["stability"] < a2["stability"]
    
    sorted_airlines = list.merge_sort(airlines_stats, sort_criteria)
    
    # Tomar las M primeras aerolíneas
    result_airlines = list.new_list()
    total = min(m, list.size(sorted_airlines))
    
    for i in range(total):
        airline = list.get_element(sorted_airlines, i)
        
        # Cambiar informacion del vuelo más cercano
        closest = airline["closest_flight"]
        closest_info = {}
        
        if closest:
            dep_time = closest.get("dep_time", "Unknown")
            date_str = closest.get("date", "Unknown")
            
            closest_info = {
                "ID": closest.get("id", "Unknown"),
                "Código": closest.get("flight", "Unknown"),
                "Fecha-Hora salida": f"{date_str} {dep_time}",
                "Origen": closest.get("origin", "Unknown"),
                "Destino": closest.get("dest", "Unknown")
            }
        
        # Formatear información de la aerolinea
        airline_info = {
            "Carrier": airline["carrier"],
            "Num vuelos": airline["num_flights"],
            "Promedio retraso": airline["average_delay"],
            "Estabilidad": airline["stability"],
            "Vuelo más cercano al promedio": closest_info
        }
        
        list.add_last(result_airlines, airline_info)
    
    end_time = time.perf_counter()
    elapsed_ms = (end_time - start_time) * 1000
    
    return {
        "total_airlines": list.size(result_airlines),
        "airlines": result_airlines,
        "elapsed": f"{elapsed_ms:.2f}"
    }


def calculate_departure_delay(flight):
    try:
        dep_time = flight.get("dep_time", "Unknown")
        sched_dep_time = flight.get("sched_dep_time", "Unknown")
        
        if dep_time == "Unknown" or sched_dep_time == "Unknown":
            return None
        
        if dep_time == "" or sched_dep_time == "":
            return None
        
        # Convertir horas a minutos
        dep_minutes = convert_time_to_minutes(dep_time)
        sched_minutes = convert_time_to_minutes(sched_dep_time)
        
        if dep_minutes is None or sched_minutes is None:
            return None
        
        # Calcular diferencia
        difference = dep_minutes - sched_minutes
        
        if difference > 720: 
            difference -= 1440
        elif difference < -720:
            difference += 1440 
        
        return difference
        
    except Exception:
        return None


def convert_time_to_minutes(time_str):
    
    try:
        # Limpiar espacios
        time_str = time_str.strip()
        
        if ':' in time_str:
            parts = time_str.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
        else:
            if len(time_str) == 4:
                hours = int(time_str[:2])
                minutes = int(time_str[2:])
            elif len(time_str) == 3:
                hours = int(time_str[0])
                minutes = int(time_str[1:])
            elif len(time_str) == 2:
                hours = int(time_str)
                minutes = 0
            elif len(time_str) == 1:
                hours = int(time_str)
                minutes = 0
            else:
                return None
        
        # Validar rangos
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            return None
        
        return hours * 60 + minutes
        
    except (ValueError, IndexError, AttributeError):
        return None


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
