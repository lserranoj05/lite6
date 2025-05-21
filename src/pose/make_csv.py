import csv

def convertir_a_csv(fichero_entrada, fichero_salida):
    # Abrir el archivo de entrada
    with open(fichero_entrada, 'r') as archivo:
        lineas = archivo.readlines()

    # Lista para almacenar los datos extraídos
    datos = []
    
    # Variables temporales para almacenar los datos actuales
    name = None
    id_ = None
    pos_x = pos_y = pos_z = None
    orient_x = orient_y = orient_z = orient_w = None

    # Iterar sobre las líneas del archivo utilizando un índice
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()  # Limpiar espacios extra
        
        # Buscar y extraer los datos
        if linea.startswith('name:'):
            name = linea.split('"')[1]  # Extracción de nombre (entre comillas)
        elif linea.startswith('id:'):
            id_ = int(linea.split(':')[1].strip())
        elif linea.startswith('position'):
            # Encontrar las coordenadas de la posición
            pos_x, pos_y, pos_z = None, None, None
            i += 1  # Saltamos a la siguiente línea
            while i < len(lineas):
                linea = lineas[i].strip()
                if linea.startswith('x:'):
                    pos_x = float(linea.split(':')[1].strip())
                elif linea.startswith('y:'):
                    pos_y = float(linea.split(':')[1].strip())
                elif linea.startswith('z:'):
                    pos_z = float(linea.split(':')[1].strip())
                elif linea == '}':  # Fin del bloque de 'position'
                    break
                i += 1  # Avanzar al siguiente índice
        elif linea.startswith('orientation'):
            # Encontrar las coordenadas de orientación
            orient_x, orient_y, orient_z, orient_w = None, None, None, None
            i += 1  # Saltamos a la siguiente línea
            while i < len(lineas):
                linea = lineas[i].strip()
                if linea.startswith('x:'):
                    orient_x = float(linea.split(':')[1].strip())
                elif linea.startswith('y:'):
                    orient_y = float(linea.split(':')[1].strip())
                elif linea.startswith('z:'):
                    orient_z = float(linea.split(':')[1].strip())
                elif linea.startswith('w:'):
                    orient_w = float(linea.split(':')[1].strip())
                elif linea == '}':  # Fin del bloque de 'orientation'
                    break
                i += 1  # Avanzar al siguiente índice

        # Cuando se han extraído todos los datos de un bloque, agregarlo a la lista
        if name and id_ and pos_x is not None and pos_y is not None and pos_z is not None and orient_x is not None:
            datos.append([name, id_, pos_x, pos_y, pos_z, orient_x, orient_y, orient_z, orient_w])

        i += 1  # Avanzar al siguiente índice

    # Abrir el archivo CSV para escribir los resultados
    with open(fichero_salida, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Escribir la cabecera del CSV
        writer.writerow([
            'indice', 'name', 'id', 'position_x', 'position_y', 'position_z',
            'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w'
        ])
        
        # Escribir los datos extraídos
        for i, fila in enumerate(datos):
            writer.writerow([i + 1] + fila)

    print(f"Archivo CSV generado correctamente: {fichero_salida}")

# Llamada a la función
convertir_a_csv('lite6_poses.txt', 'lite6_poses_CSV.csv')

