# Robot Arm Functions
# Author: GuustFlater13


# calculate pule Width
def angle_to_pulse_gripper(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_sg90 - servo_min_sg90) / 100) * x) + servo_min_sg90
    print("Gripper: angle= ", angle, " : pulse= ", pulse)
    return pulse


# calculate pule Width
def angle_to_pulse_arm(angle):
    x = float(angle) * (100 / 180)
    pulse = int(((servo_max_mg946r - servo_min_mg946r) / 100) * x) + servo_min_mg946r
    print("Arm: angle= ", angle, " : pulse= ", pulse)
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
def go_to_base(current_angle_arm_under, current_angle_arm_above):
    print("Going back to base, from: ", current_angle_arm_under, "and", current_angle_arm_above, )
    go_arm_by_steps(channel_arm_under, current_angle_arm_under, base_arm_under)
    go_arm_by_steps(channel_arm_above, current_angle_arm_above, base_arm_above)
    pwm.set_pwm(channel_gripper, 0, angle_to_pulse_gripper(0))