import board
import adafruit_bmp280
import busio

# PT stands for Pressure and Temperature


class PTsensor:
    """
    Class used to gather information from the Pressure
    and Temperature (PT) sensor

    The PT sensor (BMP280) needs to be connected to the
    Raspberry Pi in the following way: (from left to right holding
    the connections below)
    - connect GND to Ground (pin 6)
    - do not connect VCC
    - connect SCL to GPIO 3 (SCL) (pin 5)
    - connect SDA to GPIO 2 (SDA) (pin 3)
    - do not connect CSB
    - connect SDO to 3V3 power (pin 1)
    """

    def __init__(self):
        # Initialize the sensor. Signal is connected to GPIO 8
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ptSensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    def readPressure(self):
        for i in range(3):
            try:
                pressure = self.ptSensor.pressure
                if pressure is not None:
                    return pressure
            except RuntimeError:
                continue
        raise Exception("Could not gather the pressure")
