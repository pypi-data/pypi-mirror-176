import random
import threading
from time import sleep
from uvraspy.database.DataPoint import DataPoint
from datetime import datetime

from uvraspy.calculator.uvcalculator import UVCalculator


def avg(l):
    return sum(l) / len(l)


BUF_SIZE = 50
SEND_TIME_S = 5


class Gather:
    """
    Class used to gather information from the sensors

    Attributes
    ----------
    db_manager : dbmanager
        the database manager
    calculator : UVCalculator
        the calculator that is responsible for alerts
    """

    inst = None

    def __init__(self, db_manager):
        self.db_manager = db_manager
        Gather.inst = self

        try:
            from uvraspy.gather.UVsensor import UVsensor
            self.UVSensor = UVsensor()
        except:
            # Sensor not connected
            self.UVSensor = None
        try:
            from uvraspy.gather.HTSensor import HTsensor
            self.HTSensor = HTsensor()
        except:
            # Sensor not connected
            self.HTSensor = None
        try:
            from uvraspy.gather.PTsensor import PTsensor
            self.pSensor = PTsensor()
        except:
            # Sensor not connected
            self.pSensor = None

        # define averages
        self.avg_uv = [0] * BUF_SIZE
        self.avg_temp = [21] * BUF_SIZE
        self.avg_humid = [50] * BUF_SIZE
        self.avg_pressure = [1000] * BUF_SIZE

        self.lock = threading.Lock()
        self.running = False
        self.thread = threading.Thread(
            target=self.threadStart, name="Gatherer")

    def start_gather(self):
        # start the thread
        self.running = True
        self.thread.start()

    def _uv(self):
        if self.UVSensor is not None:
            return self.UVSensor.readUVI()
        else:
            return random.randint(0, 12)  # Random number for testing
            raise Exception("UV sensor is not connected")

    def getUV(self):
        return avg(self.avg_uv)

    def _temp(self):
        if self.HTSensor is not None:
            try:
                return self.HTSensor.readTemperature()
            except:
                return random.randint(-20, 40)  # Random number for testing
                raise Exception("Temperature sensor is not connected")
        else:
            return random.randint(-20, 40)
            raise Exception("Temperature sensor is not connected")

    def getTemp(self):
        return avg(self.avg_temp)

    def _humid(self):
        if self.HTSensor is not None:
            try:
                return self.HTSensor.readHumidity()
            except:
                return random.randint(0, 100)
                raise Exception("Humidity sensor is not connected")
        else:
            return random.randint(0, 100)
            raise Exception("Humidity sensor is not connected")

    def getHumid(self):
        return avg(self.avg_humid)

    def _pressure(self):
        if self.pSensor is not None:
            try:
                return self.pSensor.readPressure()
            except:
                return random.randint(900, 1100)
                raise Exception("Pressure sensor is not connected")
        else:
            return random.randint(900, 1100)
            raise Exception("Pressure sensor is not connected")

    def getPressure(self):
        """
        Returns the pressure in hPa, averaged over 5 seconds
        """
        return avg(self.avg_pressure)

    def threadStart(self):
        """
        function that gathers data from the sensors continuously
        """
        iter = 1

        while self.running:
            try:
                self.lock.acquire()

                try:
                    from uvraspy.gather.UVsensor import UVsensor
                    self.UVSensor = UVsensor()
                except:
                    # Sensor not connected
                    self.UVSensor = None
                try:
                    from uvraspy.gather.PTsensor import PTsensor
                    self.pSensor = PTsensor()
                except:
                    # Sensor not connected
                    self.pSensor = None

                # get the data from the sensors
                timestamp = int(round(datetime.now().timestamp()))
                self.avg_uv[iter] = self._uv()
                self.avg_temp[iter] = self._temp()
                self.avg_humid[iter] = self._humid()
                self.avg_pressure[iter] = self._pressure()

                if iter == 0:
                    # every 5 seconds

                    # calculate the average
                    uv = avg(self.avg_uv)
                    temp = avg(self.avg_temp)
                    humid = avg(self.avg_humid)
                    pressure = avg(self.avg_pressure)

                    self.db_manager.addDataPoint(
                        DataPoint(timestamp, temp, int(humid), int(pressure), uv))
                    if UVCalculator.inst is not None:
                        UVCalculator.inst.updateUV(uv, timestamp)

                self.lock.release()
                sleep(SEND_TIME_S / BUF_SIZE)
                iter = (iter + 1) % BUF_SIZE
            except KeyboardInterrupt:
                break
