# robot_arm_control
# Author: GuustFlater13

from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
import logging

# Configure min and max servo pulse lengths
# MG946R
servo_min_mg946r = 90  # Min pulse length out of 4096
servo_max_mg946r = 600  # Max pulse length out of 4096

# SG60
servo_min_sg90 = 146  # Min pulse length out of 4096
servo_max_sg90 = 600  # Max pulse length out of 4096

channel_gripper = 3
channel_arm_under = 7
channel_arm_above = 11

base_arm_under = 20
base_arm_above = 50

# Initialise the PCA9685 using the default address (0x40)
# Alternatively specify a different address and/or bus:
# pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm = Adafruit_PCA9685.PCA9685()


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initialize starting point
    current_angle_arm_under = base_arm_under
    current_angle_arm_above = base_arm_above

    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

    # If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
    pwm.set_pwm(channel_arm_above, 0, angle_to_pulse_arm(base_arm_above))
    pwm.set_pwm(channel_arm_under, 0, angle_to_pulse_arm(base_arm_under))

    while True:
        angle_arm_under = input("Enter angle of lower arm (or q to quit): ")
        if angle_arm_under == "q" or angle_arm_under == "":
            go_to_base()
            quit()
        angle_arm_above = input("Enter angle of higher arm (or q to quit): ")
        if angle_arm_above == "q" or angle_arm_above == "":
            go_to_base()
            quit()
        angle_gripper = input("Enter angle of gripper (or q to quit): ")
        if angle_gripper == "q" or angle_gripper == "":
            go_to_base()
            quit()

        # Move
        # arm above
        go_arm_by_steps(channel_arm_above, current_angle_arm_above, angle_arm_above)
        current_angle_arm_above = angle_arm_above
        # arm under
        go_arm_by_steps(channel_arm_under, current_angle_arm_under, angle_arm_under)
        current_angle_arm_under = angle_arm_under
        # gripper
        pwm.set_pwm(channel_gripper, 0, angle_to_pulse_gripper(angle_gripper))


# Functions


# calculate pule Width
def angle_to_pulse_gripper(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_sg90 - servo_min_sg90) / 100) * x) + servo_min_sg90
    print("angle= ", angle, " : pulse= ", pulse)
    return pulse


# calculate pule Width
def angle_to_pulse_arm(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_mg946r - servo_min_mg946r) / 100) * x) + servo_min_mg946r
    print("angle= ", angle, " : pulse= ", pulse)
    return pulse


# go step by step
def go_arm_by_steps(channel, current_angle, angle):
    step = int(current_angle)
    while step != int(angle):
        if int(current_angle) < int(angle):
            step = step + 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        if int(current_angle) > int(angle):
            step = step - 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        print("step: ", step)
        time.sleep(.05)


# Go to base
def go_to_base():
    print("Going back to base, from: ", current_angle_arm_under, "and", current_angle_arm_above, )
    go_arm_by_steps(channel_arm_under, current_angle_arm_under, base_arm_under)
    go_arm_by_steps(channel_arm_above, current_angle_arm_above, base_arm_above)
    angle_to_pulse_gripper(0)


if __name__ == "__main__":
    main()
