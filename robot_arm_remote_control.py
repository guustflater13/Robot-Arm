# robot_arm_remote_control
# author: GuustFlater13
from __future__ import division

import socket
import sys

# Uncomment to enable debug output.
import logging

# Robot arm functions
import robot_arm_functions


def main():
    ip = 'localhost'
    port = 6666

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip, port)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    logging.basicConfig(level=logging.DEBUG)

    # Initialize starting point
    current_angle_arm_under = robot_arm_functions.get_base_arm_under()
    current_angle_arm_above = robot_arm_functions.get_base_arm_above()

    # If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
    robot_arm_functions.directly_back_to_base()

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        realdata_string = ""

        try:
            print('connection from', client_address)

            while True:
                data = connection.recv(16)
                print('received "%s"' % data)
                if data:
                    print('sending data back to the client')
                    connection.sendto(data, client_address)
                    realdata_string = (data.decode('utf-8'))
                    if realdata_string == 'q;q;q;q':
                        break
                    realdata = realdata_string.split(";")
                    rotate, arm_under, arm_above, gripper = realdata
                    print("rotate=", rotate)
                    print("arm_under=", arm_under)
                    print("arm_above=", arm_above)
                    print("gripper=", gripper)

                else:
                    print('no more data from', client_address)
                    break

            print(realdata_string)
        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    main()
