# Simulación de laboratorio de microgravedad con el robot UFactory Lite 6

Este repositorio contiene el paquete de ROS 2 desarrollado para el Trabajo Fin de Grado de Lucas Serrano Jiménez. Se ha diseñado para ser utilizado en sistemas con Ubuntu 24.04, ROS2 Jazzy y Gazebo Harmonic.

Este paquete presenta una simulación de Gazebo de una mesa de trabajo como las de los simuladores de microgravedad planares. Se tiene la opción de cargar el robot UFactory Lite 6 sobre dicha mesa, para realizar control articular sobre él y llevar a cabo diferentes experimentos.

Se incluye un mundo base, que cuenta con dicha mesa, y varios mundos de experimentación: un plano inclinado, una pista horizontal y un mundo vacío. Tanto la mesa, como el plano, como la pista son superficies sin fricción que permiten un comportamiento similar al obtenido con microgravedad.

En este repositorio se encuentran todos los archivos necesarios para su instalación y uso, así como las instrucciones pertinentes.

---

## Instalación y compilación

Estos son los pasos para clonar el repositorio e instalar el paquete dentro de tu espacio de trabajo de ROS 2:

```bash
# Crea un espacio de trabajo si no tienes uno
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clona este repositorio
git clone https://github.com/lserranoj05/lite6

# Vuelve al directorio raíz del workspace
cd ~/ros2_ws

# Compila el workspace
colcon build

# Sourcing del entorno
source install/setup.bash

```

**IMPORTANTE:** Se debe acceder al fichero ```lite6.urdf```, dentro de la carpeta ```urdf```, y actualizar las rutas de las mallas de cada articulación a las locales de tu máquina. Se debe actualizar **cada etiqueta <mesh .../>**. 


---

## Uso del paquete
### Preparación de la escena
Para usar los servicios que ofrece el paquete, primero se debe lanzar la simulación. Dentro del fichero ```world.launch.py``` (en la carpeta ```launch```) se debe indicar el nombre del mundo a cargar de entre los disponibles. Por defecto se carga ```base_world_mesa.sdf```, que representa el mundo con la mesa de trabajo del laboratorio.

Con el mundo elegido:
```
# Acceder a la raiz del workspace
cd ~/ros2_ws
source install/setup.bash

# Lanzar la simulación
ros2 launch lite6 world.launch.py
```

Este comando lanza Gazebo con la escena indicada. Una vez haya cargado Gazebo, desde otra terminal:
```
# Acceder a la raiz del workspace
cd ~/ros2_ws
source install/setup.bash

# Incluir el robot en la escena
ros2 launch lite6 spawn_urdf.launch.py
```

**IMPORTANTE**: Si el robot no aparece sobre la mesa, comprobar sus coordenadas de origen en el fichero ```spawn_urdf.launch.py```, dentro de la carpeta ```launch```. En la misma parte del código se indican coordenadas de origen recomendadas para las distintas escenas de experimentación.

### Experimentación y recogida de datos
Para trabajar con el robot en la escena, se incluyen varios ficheros Python que ofrecen algunas opciones básicas. Se encuentran dentro de la carpeta ```src```, divididos en las carpetas ```movimiento articular``` y ```pose```.

En la carpeta ```movimiento articular```, se encuentran los ficheros:
- `capturar_mono.py`: Captura la posición articular de la articulación indicada en el script hasta que el usuario cancela su ejecución. Guarda los resultados en un fichero csv nombrado tras la fecha y hora de la captura de datos.
- `capturar_multi.py`: Programa similar al anterior que amplia la captura de datos a las seis articulaciones del robot.
- `comparar.py`: Este script genera una gráfica de matplotlib que compara los ficheros csv que se le indiquen. Viene preparado para comparar valores de par motor.
- `mover_mono.py`: Utiliza el controlador de trayectorias para enviar una consigna de posición articular a una sola articulación del robot. En el array de posiciones, el valor 0 equivale a la posición de origen.
- `moverYcapturar_mono.py`: Combina el script `capturar_mono.py` y el script `mover_mono.py` para enviar la orden de movimiento y capturar hasta que se complete. 
- `moverYcapturar_multi.py`: Ampliación del script anterior a consignas multiarticulares.
- `plot_mono.py`: Utiliza matplotlib para generar una gráfica de la posición articular de la articulación indicada en el código a lo largo de las mediciones tomadas.
- `plot_multi.py`: Extensión del programa anterior para representar varias articulaciones simultáneamente.

En la carpeta ```pose```, se encuentran los ficheros:
- `get_coords.py`: Almacena en un fichero las coordenadas espaciales de todos los elementos de la escena de Gazebo. Lo hace suscribiéndose y escuchando uno de los topics propios de Gazebo.
- `filter_coords.py`: Filtra el archivo anterior para guardar únicamente las coordenadas del elemento que se le indique. Por defecto, viene preparado para mantener las coordenadas del modelo del robot Lite 6.
- `make_csv.py`: A partir del fichero csv filtrado, organiza los datos en un fichero csv.
- `plot_csv.py`: Utiliza matplotlib para representar el csv generado por el script anterior.

Se debe tener al robot cargado en escena para utilizar correctamente cualquiera de estos programas. Para usarlos:

```
# Acceder a la localización de los ficheros
cd ~/ros2_ws/src/lite6/src

# Si se quiere uno de los scripts de movimiento o captura articular:
cd \movimiento \articular 

# Si se quiere uno de los scripts de captura de posición:
cd pose

# Para ejecutar:
python3 {scriptElegido.py}
```
