import pywifi
from pywifi import const
import time
import random
import socket
import threading

class Nodo:
    def __init__(self, direccion_ip):
        self.direccion_ip = direccion_ip
        self.vecinos = []


class RedMesh:
    def __init__(self):
        self.nodos = []

    def agregar_nodo(self, direccion_ip):
        self.nodos.append(Nodo(direccion_ip))

    def eliminar_nodo(self, direccion_ip):
        for nodo in self.nodos:
            if nodo.direccion_ip == direccion_ip:
                self.nodos.remove(nodo)
                for vecino in nodo.vecinos:
                    vecino.vecinos.remove(nodo)
                break

    def enrutamiento_congestion(self, direccion_ip_origen, direccion_ip_destino, datos):
        nodo_actual = None
        for nodo in self.nodos:
            if nodo.direccion_ip == direccion_ip_origen:
                nodo_actual = nodo
                break

        vecinos_disponibles = [vecino for vecino in nodo_actual.vecinos if len(vecino.vecinos) > 1]

        if not vecinos_disponibles:
            print("No hay vecinos disponibles para enrutar el paquete")
            return

        vecino_seleccionado = random.choice(vecinos_disponibles)

        print(f"Enviando datos a {direccion_ip_destino} a través del vecino {vecino_seleccionado.direccion_ip}")

    def configurar_red_inalambrica(self, ssid, password):
        # Crear un objeto PyWiFi
        wifi = pywifi.PyWiFi()
        # Obtener la primera interfaz de red inalámbrica disponible
        iface = wifi.interfaces()[0]
        # Apagar la interfaz de red inalámbrica
        iface.disconnect()
        # Crear un objeto Perfil de red
        profile = pywifi.Profile()
        # Establecer el SSID de la red
        profile.ssid = ssid
        # Establecer el tipo de cifrado
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # Establecer la contraseña de la red
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        # Agregar el perfil a la lista de perfiles de la interfaz de red inalámbrica
        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)
        # Conectar a la red
        iface.connect(temp_profile)
        # Esperar a que la conexión se establezca
        while iface.status() != const.IFACE_CONNECTED:
            pass

        # Imprimir información de la conexión
        print("Conectado a:", iface.ssid())
        print("Dirección IP:", iface.iface_addr())

    def iniciar(self):
        # Configurar la red inalámbrica
        self.configurar_red_inalambrica("MiRed", "contraseña")

        # Configurar los nodos de la red mesh
        for i in range(self.num_nodos):
            nodo = Nodo(i, self)
            self.nodos.append(nodo)

        # Iniciar los hilos de los nodos
        for nodo in self.nodos:
            nodo.iniciar_hilo()

        # Esperar a que todos los nodos se conecten
        time.sleep(5)
        # Establecer rutas
        self.establecer_rutas()
        # Iniciar la simulación
        self.simular()

    def enrutamiento(self, direccion_ip_origen, direccion_ip_destino, datos):
        nodo_actual = None
        for nodo in self.nodos:
            if nodo.direccion_ip == direccion_ip_origen:
                nodo_actual = nodo
                break

        for vecino in nodo_actual.vecinos:
            if vecino.direccion_ip == direccion_ip_destino:
                print(f"Enviando datos a {direccion_ip_destino} a través del vecino {vecino.direccion_ip}")
                return

        print(
            f"No se encontró un vecino directo para la dirección {direccion_ip_destino}, enviando a todos los vecinos conocidos")

        for vecino in nodo_actual.vecinos:
            print(f"Enviando datos a {direccion_ip_destino} a través del vecino {vecino.direccion_ip}")


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.red_mesh = RedMesh()
        self.red_mesh.configurar_red_inalambrica("MiRed", "contraseña")
        self.red_mesh.agregar_nodo(self.host)

    def aceptar_conexiones(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexión aceptada desde {client_address}")
            cliente = Nodo(client_address[0])
            self.red_mesh.agregar_nodo(cliente.direccion_ip)
            cliente_socket_thread = threading.Thread(target=self.escuchar_cliente, args=(client_socket, cliente))
            cliente_socket_thread.start()

    def escuchar_cliente(self, client_socket, cliente):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Mensaje recibido desde {cliente.direccion_ip}: {data}")
                self.red_mesh.enrutamiento_congestion(cliente.direccion_ip, self.host, data.encode())
            except Exception as e:
                print(e)
                break
        client_socket.close()
        self.red_mesh.eliminar_nodo(cliente.direccion_ip)

    def iniciar(self):
        print(f"Servidor de chat iniciado en {self.host}:{self.port}")
        aceptar_conexiones_thread = threading.Thread(target=self.aceptar_conexiones)
        aceptar_conexiones_thread.start()

class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.nodo = Nodo(socket.gethostbyname(socket.gethostname()))
        self.red_mesh = RedMesh()
        self.red_mesh.agregar_nodo(self.nodo.direccion_ip)
        self.red_mesh.configurar_red_inalambrica("MiRed", "contraseña")
        self.iniciar_escucha()

    def enviar_mensaje(self, mensaje):
        try:
            self.client_socket.sendall(mensaje.encode())
        except Exception as e:
            print(e)

    def recibir_mensaje(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                print(data)
            except Exception as e:
                print(e)
                break
        self.client_socket.close()

    def iniciar_escucha(self):
        recibir_mensaje_thread = threading.Thread(target=self.recibir_mensaje)
        recibir_mensaje_thread.start()
