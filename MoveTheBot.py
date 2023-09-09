import socket

# Define the IP address and port for communication
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345

# Set up a socket for communication
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print('Waiting for commands...')

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            command = data.decode('utf-8').strip()

            if command == 'F':
                # Code to move the robot forward
                print('Moving forward')
            elif command == 'L':
                # Code to turn the robot left
                print('Turning left')
            elif command == 'R':
                # Code to turn the robot right
                print('Turning right')
            elif command == 'S':
                # Code to stop the robot
                print('Stopping')
            else:
                print('Unknown command:', command)

        except KeyboardInterrupt:
            break

print('Closing the server')
