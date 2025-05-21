def filtrar_pose_lite6_robot(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    filtered_lines = []
    inside_block = False
    current_block = []

    for line in lines:
        # Si encontramos un bloque "pose", verificamos si es "lite6_robot"
        if line.strip().startswith('pose {'):
            inside_block = False  # Reset
            current_block = []  # Limpiar el bloque anterior

        if inside_block:
            current_block.append(line)
        #lite6_robot
        if 'name: "link6"' in line:
            inside_block = True
            current_block.append(line)

        # Si hemos alcanzado el final del bloque "pose", agregamos el bloque completo
        if inside_block and line.strip() == '}':
            current_block.append(line)
            filtered_lines.extend(current_block)
            current_block = []  # Limpiar para el siguiente bloque

    # Guardamos el resultado en un nuevo archivo
    with open(output_file, 'w') as out_file:
        out_file.writelines(filtered_lines)

    print(f"Se han guardado los bloques de 'lite6_robot' en {output_file}")

# Uso
input_file = 'raw_poses.txt'  # Nombre de tu archivo original
output_file = 'lite6_poses.txt'  # Nombre del archivo donde se guardarán los bloques filtrados
filtrar_pose_lite6_robot(input_file, output_file)

