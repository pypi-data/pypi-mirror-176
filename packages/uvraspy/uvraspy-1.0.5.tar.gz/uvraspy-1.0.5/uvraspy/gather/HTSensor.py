import board
import adafruit_dht

# HT stands for Humidity and Temperature


class HTsensor:
    """
    Class used to gather information from the Humidity and
    Temperature (HT) sensor

    The HT (KY-015 DHT11) needs to be connected to the
    Raspberry Pi in the following way: (from left to right holding
    the connections downwards)
    - connect left connection to GPIO 23 (pin 16)
    - connect middle connection to 3V3 power (pin 1)
    - connect right connection to Ground (pin 6)
    """

    def __init__(self):
        # Initialize the sensor. Signal is connected to GPIO23.
        self.htSensor = adafruit_dht.DHT11(board.D23)

    def readTemperature(self):
        for i in range(3):
            try:
                temperature = self.htSensor.temperature
                if temperature is not None:
                    return temperature
            except RuntimeError:
                continue
        raise Exception("Could not gather the temperature")

    def readHumidity(self):
        for i in range(3):
            try:
                humidity = self.htSensor.humidity
                if humidity is not None:
                    return humidity
            except RuntimeError:
                continue
        raise Exception("Could not gather the humidity")
