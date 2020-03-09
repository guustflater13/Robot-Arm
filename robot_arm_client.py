import socket
import sys

ip = '192.168.178.7'
port = 6666

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip, port)
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)

try:

    message = ""
    while True:
        angle_rotate = input("Enter angle of rotation (or q to quit): ")
        if angle_rotate == "q" or angle_rotate == "":
            break
        angle_arm_under = input("Enter angle of lower arm (or q to quit): ")
        if angle_arm_under == "q" or angle_arm_under == "":
            break
        angle_arm_above = input("Enter angle of higher arm (or q to quit): ")
        if angle_arm_above == "q" or angle_arm_above == "":
            break
        angle_gripper = input("Enter angle of gripper (or q to quit): ")
        if angle_gripper == "q" or angle_gripper == "":
            break

        message_list = [angle_rotate, angle_arm_under, angle_arm_above, angle_gripper]
        delimiter = ";"
        message = delimiter.join(message_list)

        # Send data
        print('sending "%s"' % message)
        sock.sendto(message.encode(), (ip, port))

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received "%s"' % data)

    # reset and stop
    message = 'q;q;q;q'
    print('sending "%s"' % message)
    sock.sendto(message.encode(), (ip, port))

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
