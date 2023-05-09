import py2p
import threading
import time
import uuid

from py2p.mesh import MeshConnection


def handle_message(msg, sender):
    clean_msg = (msg.packets)[4:-2]
    clean_sender = sender[2:10]
    print(f"\nReceived message from {clean_sender}: {clean_msg}")
    
def sender_to_string(message_obj):
    return str(message_obj)[:8]

def show_connected_devices(node):
    print("Connected devices:")
    for peer in node.routing_table:
        print(f"ID: {peer}")
        
def message_to_string(message_obj):
    return str(message_obj.packets)

def main():
    # Create a new mesh node with a specified port
    node = py2p.MeshSocket('0.0.0.0', 5678)

    node.timeout = 10
    node.max_connections = 2

    # unique ID
    node.sender = str(uuid.uuid4())[:8]

    print(f"This node's address: {node.out_addr}")
    print(f"This node's ID: {node.sender}")

    
    
    # List to store the bootstrap nodes
    bootstraps = []
        
    bootstrap_address = input("Enter the bootstrap node's address (IP:Port) or leave empty: ")
    if bootstrap_address:
        ip, port = bootstrap_address.split(':')
        node.connect(ip, int(port))
        bootstraps.append((ip, int(port)))
        

    # Start a thread to handle incoming messages
    def message_handler():
        while True:
            received = node.recv()

            if received:
                msg = received
                sender = received.sender
                handle_message(msg, sender)
            time.sleep(0.1)

    message_thread = threading.Thread(target=message_handler)
    message_thread.daemon = True
    message_thread.start()


    # Reconnection mechanism
    def reconnection_handler():
       while (node.routing_table == 0):
           if not node.routing_table:
               print("No connections. Attempting to reconnect...")
               for ip, port in bootstraps:
                   try:
                       node.connect(ip, int(port))
                       print("Reconnected to the bootstrap node.")
                       break
                   except Exception as e:
                       print(f"Failed to reconnect: {e}")
                       time.sleep(5)

    reconnection_thread = threading.Thread(target=reconnection_handler)
    reconnection_thread.daemon = True
    reconnection_thread.start()

    # Send messages to the other nodes
    while True:

        message = input("Enter message to send, 'exit' or 'show': ")
        if message == 'exit':
            for value in tuple(node.routing_table.values()):
                node.disconnect(MeshConnection(value))
            break
        elif message == 'disconnect':
            for value in tuple(node.routing_table.values()):
                node.disconnect(MeshConnection(value))
            break
        elif message == 'show':
            show_connected_devices(node)
        else:
            node.send(bytes(message, 'utf-8'))

if __name__ == "__main__":
    main()