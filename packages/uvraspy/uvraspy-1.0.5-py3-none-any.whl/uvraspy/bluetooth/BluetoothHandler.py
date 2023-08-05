import os
import threading

import uvraspy.bluetooth.advertise as advertise
import uvraspy.bluetooth.ble as ble
import uvraspy.bluetooth.service as service
import dbus.mainloop.glib
import dbus.service
from uvraspy.bluetooth.const import AGENT_PATH, SERVICE_UUID
from gi.repository import GLib

# ===================  BluetoothHandler.py  ===================


# ===================  Variables  ===================
t = None
mainloop = None

# get the system bus
bus = dbus.SystemBus(mainloop=dbus.mainloop.glib.DBusGMainLoop())
adapter = ble.find_adapter(bus)
adapter_obj = bus.get_object(ble.BLUEZ_SERVICE_NAME, adapter)
obj = bus.get_object(ble.BLUEZ_SERVICE_NAME, "/org/bluez")
agent_manager = dbus.Interface(obj, "org.bluez.AgentManager1")
agent_manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")

# mainloop for the bluetooth service
MainLoop = GLib.MainLoop
#
socket = None
# ===================  Functions  ===================


def start(main):
    """ starts the bluetooth service

    @param recv_callback: callback function for when data is received
    @param accept_callback: callback function for when a device is accepted
     """
    # start the bluetooth service, if it happens to be down
    # os.system("sudo service bluetooth start")

    # soft unlock the bluetooth device
    os.system("sudo rfkill unblock bluetooth")

    global mainloop  # the mainloop for the bluetooth service

    mainloop = MainLoop()
    # set the main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # create a new thread for running the bluetooth service
    # this is done so that the main thread can continue running
    # and the bluetooth service can run in the background
    _setup(main)
    t = threading.Thread(target=mainloop.run, name="BluetoothThread")
    t.start()


advertising = False
ad_manager = None
advertisement = None
app = None
sv = None


def stop():
    # stop the bluetooth service
    global mainloop
    global advertising
    global ad_manager
    global advertisement
    global bus
    global adapter_obj
    global adapter
    global app
    global sv
    mainloop.quit()

    print("Stopping bluetooth service")

    if advertising:
        ad_manager.UnregisterAdvertisement(
            advertisement.get_path(),
            reply_handler=register_ad_cb,
            error_handler=register_ad_error_cb
        )
    if t is not None:
        t.join()

    # reset the bluetooth device
    hci0_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")
    hci0_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(0))

    # delete the objects we created so that they can be recreated
    app.close()
    advertisement.remove_from_connection()


def restart_advertising():
    global advertisement
    global advertising
    global ad_manager
    if advertising:
        ad_manager.UnregisterAdvertisement(
            advertisement.get_path(),
            reply_handler=register_ad_cb,
            error_handler=register_ad_error_cb
        )
    advertisement.remove_from_connection()
    advertisement = advertise.UVedoraAdvertisement(bus, 0)
    advertisement.add_service_uuid(SERVICE_UUID)

    # register the advertisement
    ad_manager.RegisterAdvertisement(
        advertisement.get_path(),
        {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb
    )


def _setup(main):
    global mainloop
    global advertising
    global ad_manager
    global advertisement
    global sv
    global bus
    global app
    # find hci0 on the device using dbus
    hci0_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")
    hci0_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    # create application for our service
    app = ble.Application(bus)
    # 2 is the index of the service, after generic access and generic attribute
    sv = service.UVedoraService(bus, 2, main, restart_advertising)
    app.add_service(sv)
    service_manager = dbus.Interface(adapter_obj, ble.GATT_MANAGER_IFACE)
    service_manager.RegisterApplication(
        app.get_path(),
        {},
        reply_handler=register_app_cb,
        error_handler=[register_app_error_cb],
    )

    # create advertisement for our service
    ad_manager = dbus.Interface(adapter_obj, ble.LE_ADVERTISING_MANAGER_IFACE)
    advertisement = advertise.UVedoraAdvertisement(bus, 0)
    advertisement.add_service_uuid(SERVICE_UUID)

    # configure the agent

    # register the advertisement
    ad_manager.RegisterAdvertisement(
        advertisement.get_path(),
        {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb
    )

    # write initial values
    sv.characteristics[0].WriteValue("Hello World".encode("utf-8"), {})

    # start the mainloop
    advertising = True
    # mainloop.run()


def sendwarning():
    # send a warning to the client
    # this is done by writing to the characteristic 0xffc1
    # which is the UUID of the warning characteristic
    # we only need to notify the client that the value has changed

    # edge cases:
    # - no client connected
    # - client does not have the warning characteristic
    # - client does not have the notify property

    # get the service
    # sv = service.UVedoraService(bus, 2)
    # TODO
    pass

# ===================  DEBUG  ===================


def register_ad_cb():
    # we got a reply
    # print("Advertisement registered")
    pass


def register_ad_error_cb(error):
    # something went wrong
    print("D-Bus call failed on ad: %s" % (error))
    pass


def register_app_cb():
    # we got a reply
    # print("Application registered")
    pass


def register_app_error_cb(error):
    # something went wrong
    print("D-Bus call failed on app: %s" % (error))
    pass
