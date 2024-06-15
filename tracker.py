while True:
    # Read analog values from LDRs
    ldr1_value = read_analog_input(ldr1_pin)
    ldr2_value = read_analog_input(ldr2_pin)
    ldr3_value = read_analog_input(ldr3_pin)
    ldr4_value = read_analog_input(ldr4_pin)
    
    # Calculate light disparity
    horizontal_disparity = (ldr1_value + ldr2_value) - (ldr3_value + ldr4_value)
    vertical_disparity = (ldr1_value + ldr4_value) - (ldr2_value + ldr3_value)
    
    # Control motor movement based on disparity
    if horizontal_disparity > threshold:
        move_motor_right()
    elif horizontal_disparity < -threshold:
        move_motor_left()
    
    if vertical_disparity > threshold:
        move_motor_up()
    elif vertical_disparity < -threshold:
        move_motor_down()
    
    # Add some delay to prevent rapid movements
    time.sleep(0.1)
