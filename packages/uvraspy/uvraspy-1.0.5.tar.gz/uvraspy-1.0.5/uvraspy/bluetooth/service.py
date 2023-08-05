from time import sleep
import uvraspy.bluetooth.ble as ble
import uvraspy.gather.gather as gather
# import main
from uvraspy.encryption.Cryptor import cryptor
from uvraspy.bluetooth.const import (
    ANALYZE_FILTER_UUID, ANALYZE_UUID, GBUS_UUID,
    PREFERENCES_UUID, WARNING_UUID,
    SENSOR_UUID, SERVICE_UUID)
from uvraspy.preferences.preferences import Preferences
from uvraspy.database.dbmanager import dbm
import threading

# ===================  Characteristics  ===================


class GbusCharacteristic(ble.Characteristic):
    """
    Characteristic for writing commands to the piHat
    This might eventually not be used but is still here for any eventualities
    """

    uuid = GBUS_UUID
    description = "General Bus"

    def __init__(self, bus, index, service, ):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["write"], service)
        self.value = [0]

    def WriteValue(self, value, options):
        # get the lock from main
        # main.lock.acquire()
        # # write the value to the main
        # main.command += value
        # # release the lock
        # main.lock.release()
        print("GbusCharacteristic: " + str(value))

    def ReadValue(self, options):
        return super().ReadValue(options)


class SensorDataCharacteristic(ble.Characteristic):
    """
    Characteristic for reading sensor data from the piHat
    """

    uuid = SENSOR_UUID
    description = "Sensor Data"

    def __init__(self, bus, index, service, gather: gather.Gather):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["read"], service)
        self.senser = gather
        self.crypt = cryptor

    def ReadValue(self, options):
        # use the sensor data from the sensor class
        u = self.senser.getUV()
        t = self.senser.getTemp()
        h = self.senser.getHumid()
        p = self.senser.getPressure()

        # convert the data to a byte array
        # x = bytes([u & 0xff, (u >> 8) & 0xff, (u >> 16) & 0xff, (u >> 24) & 0xff,
        #            t & 0xff, (t >> 8) & 0xff, (t >> 16) & 0xff, (t >> 24) & 0xff,
        #            h & 0xff, (h >> 8) & 0xff, (h >> 16) & 0xff, (h >> 24) & 0xff,
        #            p & 0xff, (p >> 8) & 0xff, (p >> 16) & 0xff, (p >> 24) & 0xff])

        x = "{:.1f}|{:.2f}|{:.0f}|{:.0f}".format(t, u, h, p)

        # encrpyt the data
        x, y, z = cryptor.encrypt(x)
        # print(self.crypt.decrypt(x, y))

        return y + z + x


class AnalyzeFilterCharacteristic(ble.Characteristic):
    """
    Characteristic for writing filters to the piHat
    """

    uuid = ANALYZE_FILTER_UUID
    description = "Analyze Filter"

    def __init__(self, bus, index, service, analyze):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["write"], service)
        self.analyze_char = analyze

        self.date_from = None
        self.date_to = None
        self.limit = 100
        self.accuracy = 1000  # the amount of datapoints to get in general
        self.spacing = 60  # minimum spacing in seconds from each datapoint

    def WriteValue(self, value, options):
        encrypted = ble.dbus_array_to_bytes(value)
        decrypt = cryptor.decrypt(
            encrypted[32:], encrypted[:16], encrypted[16:32])

        self.date_from = int.from_bytes(decrypt[:8], byteorder='little')
        self.date_to = int.from_bytes(decrypt[8:16], byteorder='little')
        self.limit = int.from_bytes(decrypt[16:20], byteorder='little')
        self.accuracy = int.from_bytes(decrypt[20:24], byteorder='little')
        self.spacing = int.from_bytes(decrypt[24:28], byteorder='little')

        if self.date_from == 0:
            self.date_from = None
        if self.date_to == 0:
            self.date_to = None
        if self.limit == 0:
            self.limit = None
        if self.accuracy == 0:
            self.accuracy = None
        if self.spacing == 0:
            self.spacing = None

        # start a new thread to send the data
        thread = threading.Thread(target=self.sendData, args=(options,))
        thread.start()

    def sendData(self, options):
        # send the data
        buf = dbm.retrieveData(self.date_from, self.date_to, self.limit, self.accuracy, self.spacing)

        # convert buf to a byte array
        x = bytes()
        for i in buf:
            x += i.toBytes()

        buf, y, z = cryptor.encrypt(x)

        # write the data to the analyze characteristic
        # do this in a loop to make sure all the data is written
        # this is because the data is too large to be written in one go
        SIZE = 512
        for i in range(0, len(buf), SIZE):
            b = buf[i:i + SIZE]
            self.analyze_char.WriteValue(b, options)
            if "callback" in options:
                options["callback"](b)
            # sleep(0.1)

        # write the end of file character
        self.analyze_char.WriteValue(b"EOF" + y + z, options)
        if "callback" in options:
            options["callback"](b"EOF" + y + z)


class AnalyzeCharacteristic(ble.Characteristic):
    """
    Characteristic for reading the analysis from the piHat
    """

    uuid = ANALYZE_UUID
    description = "Analyze"

    def __init__(self, bus, index, service):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["read", "notify"], service)
        self.value = b""
        self.notify = False

    def ReadValue(self, options):
        # TODO
        # get all the data from the database
        # using the filters from the filter characteristic
        # and return the data

        # DEBUG
        # send the contents of the database as a test
        return self.value

    def WriteValue(self, value, options):
        # notify the client that the value has changed
        if self.notify:
            self.PropertiesChanged(ble.GATT_CHRC_IFACE, {
                                   "Value": ble.bytes_to_dbus_array(value)}, [])
        self.value = value

    def StartNotify(self):
        self.notify = True
        print("Notify started")

    def StopNotify(self):
        self.notify = False
        print("Notify stopped")


class PreferenceCharacteristic(ble.Characteristic):
    """
    Characteristic for reading and writing preferences to the piHat
    """

    uuid = PREFERENCES_UUID
    description = "Preferences"

    def __init__(self, bus, index, service, restart_adv):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["read", "write"], service)
        self.preferences = Preferences()
        self.restart_advertising = restart_adv

    def WriteValue(self, value, options):
        try:
            # decode the value
            # get the tag and nonce from the value

            # convert the value to a byte array
            value = b"".join([bytes([i]) for i in value])
            # tag = value[:16]
            # nonce = value[16:32]
            decrypt = value  # cryptor.decrypt(value[32:], tag, nonce)
            # verify the value
            splt = decrypt.split(b"\x00")
            print(splt)
            if cryptor.hash(splt[0]) != cryptor.key:
                # incorrect password

                sleep(1)  # sleep for 5 seconds to prevent brute force attacks
                raise Exception("Incorrect Password")

            Preferences.fromBytes(splt[1])

            # change the name of the device
            newname = splt[2]
            if newname != b"" and newname != cryptor.name:
                cryptor.updateName(newname.decode())
                self.restart_advertising()

            # modify the password
            newpass = splt[3]

            hs = cryptor.hash(newpass)
            if newpass != b"" and hs != cryptor.key:
                cryptor.updatekey(hs)

        except Exception as e:
            print("Invalid Preferences")
            print(e)
            return

        print("Preferences Updated")
        return

    def ReadValue(self, options):
        # return predefined matcher values
        sleep(1)  # sleep for 1 second to prevent brute force attacks
        x, y, z = cryptor.encrypt("Hello World!")
        return y + z + x


class WarningCharacteristic(ble.Characteristic):
    """
    Characteristic for reading warnings from the piHat
    """

    uuid = WARNING_UUID
    description = "Warnings"

    def __init__(self, bus, index, service, ):
        ble.Characteristic.__init__(self, bus, index, self.uuid,
                                    ["read", "notify"], service)
        self.notify = False

    # this is a remote warning characteristic
    # it will be used to send warnings to the user
    # when the UV index is too high

    # TODO
    def WriteValue(self, value, options):
        # send a warning to the user
        # this will be done by sending a notification
        # to the client
        if self.notify:
            self.PropertiesChanged(ble.GATT_CHRC_IFACE, {
                                   "Value": ble.bytes_to_dbus_array(value)}, [])
        return

    def StartNotify(self):
        # start sending notifications
        self.notify = True
        return

    def StopNotify(self):
        # stop sending notifications
        self.notify = False
        return


# ===================  Services  ===================


class UVedoraService(ble.Service):
    def __init__(self, bus, index, main, restartadv):
        ble.Service.__init__(self, bus, index, SERVICE_UUID, True)
        self.add_characteristic(GbusCharacteristic(bus, 0, self))
        self.add_characteristic(
            SensorDataCharacteristic(bus, 1, self, gather.Gather.inst))
        analyze = AnalyzeCharacteristic(bus, 3, self)
        self.add_characteristic(
            AnalyzeFilterCharacteristic(bus, 2, self, analyze))
        self.add_characteristic(analyze)
        self.add_characteristic(PreferenceCharacteristic(bus, 4, self, restartadv))
        self.add_characteristic(WarningCharacteristic(bus, 5, self))
        # TODO: add the other characteristics
