import adafruit_ltr390
import board


class UVsensor:
    """
    Class used to gather information from the UVsensor

    The UV sensor (LTR390 ALS+UV Sensor) needs to be connected to the
    Raspberry Pi in the following way: (from left to right holding
    letters on sensor straight)
    - connect VIN to 3V3 power (pin 1)
    - do not connect 3V0
    - connect GND to Ground (pin 6)
    - connect SCL to GPIO 3 (SCL) (pin 5)
    - connect SDA to GPIO 2 (SDA) (pin 3)
    - do not connect INT
    """

    def __init__(self):
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.ltr = adafruit_ltr390.LTR390(self.i2c)

    def readUV(self):
        return self.ltr.uvs

    def readUVI(self):
        return self.ltr.uvi

    def readAmbientLight(self):
        return self.ltr.light
