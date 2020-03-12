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
    ip = '192.168.178.7'
    port = 6666

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip, port)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # logging.basicConfig(level=logging.DEBUG)

    # Initialize starting point
    current_angle_arm_under = robot_arm_functions.get_base_arm_under()
    current_angle_arm_above = robot_arm_functions.get_base_arm_above()

    # If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
    print("Robot to base position, if not already")
    robot_arm_functions.directly_back_to_base()

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        realdata_string = ""
        no_more_data = False

        try:
            print('connection from', client_address)

            while True:
                data = connection.recv(16)
                print('received "%s"' % data)
                if data:
                    print('sending data back to the client')
                    connection.sendto(data, client_address)
                    realdata_string = (data.decode('utf-8'))
                    # print("realdata_string:", realdata_string)
                    if realdata_string == 'q;q;q;q':
                        no_more_data = True
                        break
                    realdata = realdata_string.split(";")
                    input1, input2, input3, input4 = realdata
                    rotate = int(input1)
                    angle_arm_under = int(input2)
                    angle_arm_above = int(input3)
                    angle_gripper = int(input4)
                    print("rotate=", rotate, "arm_under=", angle_arm_under, "arm_above=", angle_arm_above,
                          "gripper=", angle_gripper)

                    # Move robot
                    # arm above
                    current_angle_arm_above = robot_arm_functions.go_arm_above_by_steps(int(current_angle_arm_above),
                                                                                        int(angle_arm_above))
                    # current_angle_arm_above = angle_arm_above
                    # arm under
                    current_angle_arm_under = robot_arm_functions.go_arm_under_by_steps(int(current_angle_arm_under),
                                                                                        int(angle_arm_under))
                    # current_angle_arm_under = angle_arm_under
                    # gripper
                    robot_arm_functions.gripper(int(angle_gripper))

                else:
                    print('no more data from', client_address)
                    break

            if no_more_data:
                break

        finally:
            # Clean up the connection
            print('Received "%s"' % realdata_string, ' closing connection with', client_address)
            connection.close()

    # bring robot to base position
    print("Robot to base position:")
    robot_arm_functions.go_to_base(int(current_angle_arm_under), int(current_angle_arm_above))
    print("shutting down application")


if __name__ == "__main__":
    main()
