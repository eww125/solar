import spidev
import RPi.GPIO as GPIO
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# GPIO setup for servos
GPIO.setmode(GPIO.BCM)
servo_x_pin = 17
servo_y_pin = 18
GPIO.setup(servo_x_pin, GPIO.OUT)
GPIO.setup(servo_y_pin, GPIO.OUT)

pwm_x = GPIO.PWM(servo_x_pin, 50) # 50Hz PWM frequency
pwm_y = GPIO.PWM(servo_y_pin, 50)
pwm_x.start(7.5) # Neutral position
pwm_y.start(7.5)

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def set_servo_angle(pwm, angle):
    duty = 2.5 + (angle / 18.0) * 10.0
    pwm.ChangeDutyCycle(duty)

try:
    while True:
        ldr_values = [read_adc(i) for i in range(4)]
        print("LDR values:", ldr_values)

        # Determine the position adjustments based on LDR values
        if ldr_values[0] > ldr_values[1]: # Adjust X-axis
            set_servo_angle(pwm_x, 0)
        else:
            set_servo_angle(pwm_x, 180)

        if ldr_values[2] > ldr_values[3]: # Adjust Y-axis
            set_servo_angle(pwm_y, 0)
        else:
            set_servo_angle(pwm_y, 180)

        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pwm_x.stop()
    pwm_y.stop()
    GPIO.cleanup()
