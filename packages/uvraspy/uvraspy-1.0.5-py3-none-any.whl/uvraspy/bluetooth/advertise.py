from uvraspy.bluetooth.ble import Advertisement
from uvraspy.bluetooth.const import BTPATH, SERVICE_UUID
from uvraspy.encryption.Cryptor import cryptor


class UVedoraAdvertisement(Advertisement):
    PATH_BASE = BTPATH
    inst = None

    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index,
                               'peripheral', base_path=BTPATH)
        self.add_service_uuid(SERVICE_UUID)
        self.add_service_uuid("1800")
        self.add_service_uuid("1801")
        self.add_local_name(cryptor.name)
        self.include_tx_power = True

        UVedoraAdvertisement.inst = self

    def change_name(self, name):
        self.add_local_name(name)
