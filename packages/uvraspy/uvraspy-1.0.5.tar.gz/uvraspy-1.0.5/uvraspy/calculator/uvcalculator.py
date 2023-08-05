from uvraspy.preferences.preferences import Preferences


class UVCalculator:
    """
    Class to calculate if there is too much UV
    .
    Attributes
    ----------
    bluetooth : BluetoothHandler
        bluetooth handler that is used to communicate with other devices
    """
    inst = None
    MIN_UV = 2
    UV_DECREASE = 5 / 60 / 60 / 6
    UPDATE_TIME = 5
    RESET_THRESHOLD = 24
    SKIN_TYPES = {
        0: 65 * 2,
        1: 65 * 2,
        2: 82.5 * 2,
        3: 115 * 2,
        4: 150 * 2
    }
    WARN_MSG = "Too much UV! You should put on sunscreen!"

    def sunscreen_throughput(factor):
        if factor == 0:
            factor = 1
        return 1 / factor

    def calculate(self, skintype, uv_index, sunscreen):
        # do calculation:
        # (UV index / st(skin type)) / 60 -> progress per second
        basic_rate = (uv_index / UVCalculator.SKIN_TYPES[skintype]) / 60
        return basic_rate * UVCalculator.sunscreen_throughput(sunscreen)

    def __init__(self, main):
        self.value = 0
        self.main = main
        self.progress = 0
        self.last_time = 0
        self.warned = False
        UVCalculator.inst = self

    def updateUV(self, value, time):
        # self.main.warn(str(t) + " UV value updated: " + str(value))

        if self.last_time < time - self.UPDATE_TIME * self.RESET_THRESHOLD:
            # reset counter
            self.progress = 0

        self.progress -= self.UV_DECREASE * self.UPDATE_TIME

        # do the calculation
        self.progress += self.calculate(Preferences.tolerance, value, 1) * self.UPDATE_TIME

        if self.progress > 1:
            self.progress = 1
            if not self.warned:
                self.main.warn(self.WARN_MSG)
                self.warned = True

        if self.progress < 0.8:
            self.warned = False
