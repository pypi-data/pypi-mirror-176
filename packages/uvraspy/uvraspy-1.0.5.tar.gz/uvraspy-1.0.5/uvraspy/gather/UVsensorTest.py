from time import sleep

import UVsensor as UV


def main():
    sensor = UV.UVsensor()
    while True:
        if (sensor.ltr.data_ready):
            print("UV value is: ", sensor.readUV())
            print("UV index is: ", sensor.readUVI())
            print("Ambient Light is: ", sensor.readAmbientLight())
            print("")
            sleep(2)


main()
