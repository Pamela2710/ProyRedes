## Proyecto Redes 1

Este proyecto implementa una red mesh utilizando la biblioteca py2p. En esta red se busca que cada nodo se comunique directamente con otros nodos cercanos en lugar de tener que entablar comunicacion a traves de un servidor central.

Al iniciar el programa, crea un nodo mesh en el puerto 5678. Luego se solicita ingresar la dirección (IP:Puerto) del nodo bootstrap. Este es el nodo que va a servir como nodo de arranque. Si se deja en blanco el programa asume que la computadora es el nodo bootstrap y recupera la direccion ip automaticamente. Caso contrario el programa intentara conectarse con el nodo bootstrap.

La funcion message\_handler() se encarga de manejar lo relacionado con mensajes entrantes en un hilo. Constantemente chequea si ha llegado un nuevo mensaje mediante node.recv(). Si ese es el caso entonces se llama a handle\_message(), que mostrara el mensaje en consola.

Ademas se ejecuta un lazo infinito en otro hilo creado a traves de la biblioteca threading que se encargará de esperar que el usuario escriba un mensaje para enviarlo a los demas.
