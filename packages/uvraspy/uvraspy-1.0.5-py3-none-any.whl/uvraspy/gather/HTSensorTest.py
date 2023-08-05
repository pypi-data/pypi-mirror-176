from time import sleep
import HTSensor as HT


def main():
    sensor = HT.HTsensor()
    while True:
        try:
            print("The temperature is:\t", sensor.readTemperature(), "°C")
            print("The humidity is:\t", sensor.readHumidity(), "%")
            sleep(2)

        except RuntimeError as error:
            print(error.args[0])
            continue


main()
