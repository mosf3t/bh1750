# Adapted from: https://github.com/octaprog7/BH1750
# Tested with:
# - Raspberry Pi Pico (H) 2021
# - BH1750 Ambient Light Sensor | GY-302 (generic)
# - https://makershop.ie/GY-302?srsltid=AfmBOopouDok9p2jn5mwUpmofrJu2gPpPGsaXa0btYGsQm0pr9uKmuZg
# - This guide may be comparable: https://www.mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf
from machine import I2C, Pin
import bh1750
from sensor_base.bus_service import I2cAdapter
import time

if __name__ == '__main__':
    # Set scl and sda pins for your board
    # https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
    # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # for esp8266
    i2c = I2C(1, scl=Pin(3, Pin.IN, Pin.PULL_UP), sda=Pin(2, Pin.IN, Pin.PULL_UP), freq=400000)  # for Raspberry Pi Pico (H)
    adaptor = I2cAdapter(i2c)
    
    # If you get EIO exceptions, then check all connections.
    # Typical measurement_accuracy is 1.2 (from 0.96 to 1.44 times).
    # See Measurement Accuracy in datasheet!
    sol = bh1750.Bh1750(adaptor)
    sol.power(on=True)
    sol.set_mode(continuously=True, high_resolution=True)
    sol.measurement_accuracy = 1.0
    
    old_lux = curr_max = 1.0
    
    for lux in sol:
        if lux != old_lux:
            curr_max = max(lux, curr_max)
            lt = time.localtime()
            print(f"{lt[3:6]}\tIllumination [lux]: {lux}.; max: {curr_max}.; Normalized [%]: {100*lux/curr_max}.")
        old_lux = lux        
        time.sleep_ms(sol.get_conversion_cycle_time())
