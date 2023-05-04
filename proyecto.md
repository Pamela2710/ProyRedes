# Proyecto Redes NRC: 4005

Andrés Martínez (00213046), Máximo Pinta (00211312), Pamela Pupiales (00213871), Mateo Ruiz (00212195), Diego Reinoso (00214020)

Este proyecto implementa una red mesh utilizando las siguientes bibliotecas
*  **py2p**. En esta red se busca que cada nodo se comunique directamente con otros nodos cercanos en lugar de tener que entablar comunicacion a traves de un servidor central.
*  **threading**. Es un módulo en Python que proporciona clases y funciones para trabajar con hilos (también conocidos como threads).
*  **time**. Permite importar el módulo de tiempo estándar de Python. Este módulo proporciona funciones para trabajar con el tiempo, como medir la duración de una operación o hacer pausas en la ejecución de un programa.
*  **uuid**. Es un módulo en Python que proporciona funciones para trabajar con identificadores únicos universales (UUID).

Ejemplo:
![image](https://i.ibb.co/J3h70JH/id.jpg)

## Ejecución 

Al iniciar el programa, crea un nodo mesh en el puerto 5678. Muestra el ID del nodo, posteriormente se solicita ingresar la dirección (IP:Puerto) del nodo bootstrap. 
Este es el nodo que va a servir como nodo de arranque. Si se deja en blanco el programa asume que la computadora es el nodo bootstrap y recupera la direccion ip automaticamente. Caso contrario el programa intentará conectarse con el nodo bootstrap.

Ejemplo:
![image](https://i.ibb.co/2kfFqHt/f1.jpg)

* **handle_message(msg, sender_id)** La función extract_message que esta dentro de handle se utiliza para extraer el mensaje de la cadena de entrada.
* **show_connected_devices()** Utiliza la propiedad routing_table de node, esta propiedad se utiliza para obtener información sobre los nodos conectados a la red mesh a través de la instancia de MeshSocket proporcionada por el módulo py2p.
* **message\_handler()** Se encarga de manejar lo relacionado con mensajes entrantes en un hilo. Constantemente chequea si ha llegado un nuevo mensaje mediante. 
* **node.recv()**. Si ese es el caso entonces se llama a **handle\_message()**, que mostrara el mensaje en consola.
* Se ejecuta un lazo infinito en otro hilo creado a traves de la biblioteca **threading** que se encargará de esperar que el usuario escriba un mensaje para enviarlo a los demas.

## Instrucciones para ejecutar el programa

1. Definir el nodo de arranque en un cliente.
2. En el segundo cliente, al ingresar la direccion ip y puerto del nodo de arranque.
3. Del tercer cliente en adelante, ingresar la direccion ip y puerto del nodo anterior

### Salida CMD
1. py py2p_mesh.py (This node's address: 192.168.10.156:5678)
2. py py2p_mesh.py (This node's ID: f9ec9b55)
3. py py2p_mesh.py -> 192.168.10.156:5678 (This node's address: 192.168.10.157:5678)
4. py py2p_mesh.py -> 192.168.10.157:5678 (This node's address: 192.168.10.158:5678)
5. py py2p_mesh.py -> 192.168.10.158:5678 (This node's address: 192.168.10.159:5678)
