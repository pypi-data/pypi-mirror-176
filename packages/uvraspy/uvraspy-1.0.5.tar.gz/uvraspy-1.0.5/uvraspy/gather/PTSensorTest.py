from time import sleep
import PTsensor as PT


def main():
    sensor = PT.PTsensor()
    while True:
        try:
            # hPa is hectoPascal this is 100 Pascal
            print("The pressure is:\t", sensor.readPressure(), "hPa")
            sleep(2)

        except RuntimeError as error:
            print(error.args[0])
            continue


main()
