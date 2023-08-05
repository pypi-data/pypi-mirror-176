from uvraspy.encryption.Cryptor import cryptor


class Alert:
    ALERT_RECORD_SIZE = 120
    ALERT_RECORD_SIZE_FULL = 120 + 16
    ALERT_MESSAGE_SIZE = 112

    def __init__(self, timestamp, warning):
        self.warning = warning
        self.timestamp = int(round(timestamp))

    def __str__(self):
        return self.warning

    def toEncoded(self):
        buf = bytes()
        buf += self.timestamp.to_bytes(8, byteorder='big')
        buf += self.warning.ljust(Alert.ALERT_MESSAGE_SIZE, '\x55').encode("utf-8")
        x, y, z = cryptor.encrypt(buf)
        assert len(z + x) == Alert.ALERT_RECORD_SIZE_FULL
        return z + x

    def fromEncoded(encoded):
        dec = cryptor.decrypt(encoded[16:], None, encoded[:16])
        timestamp = int.from_bytes(dec[:8], byteorder='big')
        # depad the warning message, so remove the trailing 0s
        warning = dec[8:8 + Alert.ALERT_MESSAGE_SIZE].decode("utf-8").rstrip('\x55')
        return Alert(timestamp, warning)
