import pywifi
from pywifi import const
import time
import random

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
        self.configurar_red_inalambrica("MiRed", 1234)

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

        print(f"No se encontró un vecino directo para la dirección {direccion_ip_destino}, enviando a todos los vecinos conocidos")
        for vecino in nodo_actual.vecinos:
            print(f"Enviando datos a {direccion_ip_destino} a través del vecino {vecino.direccion_ip}")

# red = RedMesh()
# red.agregar_nodo("192.168.0.1")
# red.agregar_nodo("192.168.0.2")
# red.agregar_nodo("192.168.0.3")
#
# #red.eliminar_nodo("192.168.0.3")
#
# red.nodos[0].vecinos = [red.nodos[1], red.nodos[2]]
# red.nodos[1].vecinos = [red.nodos[0], red.nodos[2]]
# red.nodos[2].vecinos = [red.nodos[0], red.nodos[1]]
#
# red.enrutamiento("192.168.0.1", "192.168.0.2", "Hola, nodo 2")
# red.enrutamiento("192.168.0.1", "192.168.0.3", "Hola, nodo 3")
