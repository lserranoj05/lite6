import subprocess

# Comando a ejecutar
command = ['gz', 'topic', '-e', '-t', '/world/base_world/pose/info']

# Archivo donde se guardará la salida
output_file = 'raw_poses.txt'

# Abrir el archivo en modo escritura
with open(output_file, 'w') as file:
    try:
        # Ejecutar el comando y redirigir la salida en tiempo real
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Leer la salida en tiempo real
        for line in iter(process.stdout.readline, b''):
            # Decodificar la línea y escribirla en el archivo
            file.write(line.decode('utf-8'))
            print(line.decode('utf-8'), end='')  # También imprimir en consola si lo deseas
        
        # Esperar a que termine el proceso
        process.wait()
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")
        process.terminate()

