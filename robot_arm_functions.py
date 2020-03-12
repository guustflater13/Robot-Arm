# Robot Arm Functions
# Author: GuustFlater13

# Import the PCA9685 module.
import time

import Adafruit_PCA9685

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

max_arm_under = 100
max_arm_above = 120

# Initialise the PCA9685 using the default address (0x40)
# Alternatively specify a different address and/or bus:
# pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


def get_base_arm_under():
    return base_arm_under


def get_base_arm_above():
    return base_arm_above


# If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
def directly_back_to_base():
    pwm.set_pwm(channel_arm_above, 0, angle_to_pulse_arm(base_arm_above))
    pwm.set_pwm(channel_arm_under, 0, angle_to_pulse_arm(base_arm_under))


# calculate pule Width
def angle_to_pulse_gripper(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_sg90 - servo_min_sg90) / 100) * x) + servo_min_sg90
    # print("Gripper: angle= ", angle, " : pulse= ", pulse)
    return pulse


# calculate pule Width
def angle_to_pulse_arm(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_mg946r - servo_min_mg946r) / 100) * x) + servo_min_mg946r
    # print("Arm: angle= ", angle, " : pulse= ", pulse)
    return pulse


# go step by step
def go_arm_under_by_steps(current_angle, angle):
    channel = channel_arm_under
    angle = angle + base_arm_under
    if angle > max_arm_under:
        print("Angle Arm Under more then max angle, going to max!")
        angle = max_arm_under
    step = current_angle
    print("Arm under: Going from", current_angle, " to", angle)
    while step != angle:
        if current_angle < angle:
            step = step + 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        if current_angle > angle:
            step = step - 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        # print("step: ", step)
        time.sleep(.05)
    return angle


def go_arm_above_by_steps(current_angle, angle):
    channel = channel_arm_above
    angle = angle + base_arm_above
    if angle > max_arm_above:
        print("angle Arm Above more then max angle, going to max!")
        angle = max_arm_above
    step = current_angle
    print("Arm above: Going from", current_angle, " to", angle)
    while step != angle:
        if current_angle < angle:
            step = step + 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        if current_angle > angle:
            step = step - 1
            pwm.set_pwm(channel, 0, angle_to_pulse_arm(step))
        # print("step: ", step)
        time.sleep(.05)
    return angle


# Go to base
def go_to_base(current_angle_arm_under, current_angle_arm_above):
    print("Going back to base, from: ", current_angle_arm_under, "and", current_angle_arm_above, )
    go_arm_under_by_steps(current_angle_arm_under, 0)
    go_arm_above_by_steps(current_angle_arm_above, 0)
    gripper(0)


# gripper
def gripper(angle):
    print("Gripper:", angle)
    pwm.set_pwm(channel_gripper, 0, angle_to_pulse_gripper(angle))
