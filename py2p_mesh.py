import py2p
import threading
import time
import uuid

def handle_message(msg, sender_id):
    clean_msg = extract_message(msg)
    print(f"Received message from {sender_id}: {clean_msg}")

def extract_message(input_string):
    start_index = input_string.index("(b'") + 3
    end_index = input_string.index("',)")
    message = input_string[start_index:end_index]
    return message

def show_connected_devices(node):
    print("Connected devices:")
    for peer in node.routing_table:
        print(f"ID: {peer.id}, Address: {peer.addr}")

def main():
    # Create a new mesh node with a specified port
    node = py2p.MeshSocket('0.0.0.0', 5678)
    
    node.timeout = 10
    node.max_connections = 2

    # unique ID
    node.id = str(uuid.uuid4())[:8]

    print(f"This node's address: {node.out_addr}")
    print(f"This node's ID: {node.id}")

    # Connect to the bootstrap node if you know its address
    bootstrap_address = input("Enter the bootstrap node's address (IP:Port) or leave empty: ")
    if bootstrap_address:
        ip, port = bootstrap_address.split(':')
        node.connect(ip, int(port))

    # Start a thread to handle incoming messages
    def message_handler():
        while True:
            received = node.recv()
            if received:
                msg = mrecived.packets
                sender = received.sender
                
                handle_message(msg, sender.id)
            time.sleep(0.1)


    message_thread = threading.Thread(target=message_handler)
    message_thread.daemon = True
    message_thread.start()

    # Send messages to the other nodes
    while True:
        message = input("Enter message to send, 'exit' or 'show': ")

        if message == 'exit':
            break
        elif message == 'disconnect':
            node.disconnect()
            break
        elif message == 'show':
            show_connected_devices(node)
        else:
            node.send(bytes(message, 'utf-8'))

if __name__ == "__main__":
    main()
