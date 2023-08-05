from uvraspy.encryption.Cryptor import cryptor
from datetime import datetime


def decode(ciphertext):
    # decode the value
    # get the tag and nonce from the value

    # convert the value to a byte array
    nonce = ciphertext[:16]
    plaintext = cryptor.decrypt(ciphertext[16:], None, nonce)
    return plaintext


class DataPoint:
    RECORD_SIZE = 16
    RECORD_SIZE_FULL = 32

    def __init__(self, timestamp, temperature, humidity, pressure, Ultraviolet):
        self.timestamp = int(round(timestamp))
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.Ultraviolet = Ultraviolet

    def fromEncoded(encoded):
        dec = decode(encoded)

        # timestamp: 8 bytes
        # temperature: 2 bytes
        # humidity: 2 bytes
        # pressure: 2 bytes
        # Ultraviolet: 2 bytes
        timestamp = int.from_bytes(dec[:8], byteorder='big')
        temperature = int.from_bytes(dec[8:10], byteorder='big') / 10
        humidity = int.from_bytes(dec[10:12], byteorder='big')
        pressure = int.from_bytes(dec[12:14], byteorder='big')
        Ultraviolet = int.from_bytes(dec[14:16], byteorder='big') / 100
        return DataPoint(timestamp, temperature, humidity, pressure, Ultraviolet)

    def toBytes(self):
        buf = bytes()
        buf += (self.timestamp).to_bytes(8, byteorder='big')
        buf += (int(self.temperature * 10) & 0xffff).to_bytes(2, byteorder='big')
        buf += (self.humidity & 0xffff).to_bytes(2, byteorder='big')
        buf += (self.pressure & 0xffff).to_bytes(2, byteorder='big')
        buf += (int(self.Ultraviolet * 100) & 0xffff).to_bytes(2, byteorder='big')
        return buf

    def toEncoded(self):
        buf = self.toBytes()
        x, y, z = cryptor.encrypt(buf)
        return z + x  # no need for the tag

    def average(list):
        # average a list of data points
        # return a single data point
        now = int(datetime.now().timestamp())
        dt = 0
        t = 0
        h = 0
        p = 0
        u = 0
        for dp in list:
            dt += dp.timestamp - now
            t += dp.temperature
            h += dp.humidity
            p += dp.pressure
            u += dp.Ultraviolet
        dt /= len(list)
        t /= len(list)
        h /= len(list)
        p /= len(list)
        u /= len(list)
        return DataPoint(int(round(dt)) + now, t, int(round(h)), int(round(p)), u)
