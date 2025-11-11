import csv
import time
import DataStructures.List.array_list as list

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


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


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
