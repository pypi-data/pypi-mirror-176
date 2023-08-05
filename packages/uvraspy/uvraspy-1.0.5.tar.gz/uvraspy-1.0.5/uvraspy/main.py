
# ====================  Imports  ====================
from datetime import datetime
import sys
import os
import threading
from uvraspy.gather.gather import Gather
from uvraspy.database.dbmanager import dbm
import uvraspy.calculator.uvcalculator as uvcalc

import uvraspy.bluetooth.BluetoothHandler as bt


# ====================  Initialization  ====================


class Main:
    command = ""
    lock = threading.Lock()
    notify_cmd = threading.Condition(lock)
    notify_usr = threading.Condition(lock)
    commandline_thread = None
    end = False
    bton = False
    clean = False

    def __init__(self):
        Main.updateClean()
        Gather(dbm).start_gather()
        bt.start(self)
        uvcalc.UVCalculator(self)
        Main.bton = True
        print("Bluetooth server started")

        Main.commandline_thread = threading.Thread(target=Main.commandline, name="Commandline")
        Main.commandline_thread.start()

        # ====================  Main  ====================
        while True:
            # This is the main loop of the program. It is used to control the program.
            # With this you can control the program without having to restart it.
            try:
                usr_cmd = input("RasPy> ")
                Main.lock.acquire()
                Main.command += usr_cmd + "\n"
                Main.notify_cmd.notify()
                Main.notify_usr.wait()
                Main.lock.release()

                if Main.end:
                    if not Main.clean:
                        Main.cleanup()
                    break
            except:
                # if there is an error, stop the program gracefully
                # print("Error")
                if not Main.clean:
                    Main.cleanup()
                break

    def updateClean():
        # cleans out redundant files
        # loop through all files in the working directory
        # if the file is empty, delete it
        # if the file is a directory, that is empty, delete it
        pass

    def warn(self, message):
        # send a warning to the user
        bt.sv.get_characteristics()[5].WriteValue(message.encode(), {})

    def cleanup():
        # stop the bluetooth server
        if Main.bton:
            bt.stop()

        # stop the commandline
        Main.end = True
        Main.lock.acquire()
        Main.notify_cmd.notify()
        Main.lock.release()

        # join the commandline thread
        if Main.commandline_thread is not None and threading.current_thread() != Main.commandline_thread:
            Main.commandline_thread.join()

        # join the gather thread
        if Gather.inst.thread is not None:
            Gather.inst.running = False
            Gather.inst.thread.join()

    def commandline():
        # This is the commandline for the program. It is used to control program.
        # With this you can control the program without having to restart it.
        while not Main.end:
            # lock command in case it is being accessed by another thread
            Main.lock.acquire()
            Main.notify_cmd.wait()
            if Main.end:
                Main.lock.release()
                return
            if Main.command.count("\n") == 0:
                Main.notify_usr.notify()  # notify the lock
                Main.lock.release()
                continue  # if there is no command, continue

            # if there is a command, get it until the newline
            # and then remove everything before the newline
            cmd = Main.command[:Main.command.index("\n")]
            Main.command = Main.command[Main.command.index("\n") + 1:]

            if cmd == "exit":
                Main.end = True

                Main.notify_usr.notify()  # notify the lock
                Main.lock.release()

                break
            elif cmd == "data":
                # get the data from the database
                # and print it to the screen
                data = dbm.retrieveData(None, None, 10)
                for d in data:
                    time = datetime.fromtimestamp(d.timestamp).strftime("%H:%M:%S")
                    print("Time: " + str(time) +
                          " Temp: " + str(d.temperature) +
                          " Humidity: " + str(d.humidity) +
                          " UV: " + str(d.Ultraviolet) +
                          " Pressure: " + str(d.pressure))
            elif cmd[:7] == "update ":
                # update the script
                # there should be a zip file called update.zip
                # in the same directory as this script
                # the argument to the update command is the new version number

                # get the version number
                version = cmd[cmd.index(" ") + 1:]

                # edit the version file
                with open("version.txt", "w") as f:
                    f.write(version)

                # exit the program
                Main.end = True
                Main.clean = True
                Main.lock.release()
                Main.cleanup()

                # start the new version
                os.execv(sys.executable, ['python'] + sys.argv)

                os._exit(0)  # force exit the program
            elif cmd[:4] == "las ":
                args = cmd.split(" ")
                l = int(args[1])
                a = int(args[2])
                s = int(args[3])
                data = dbm.retrieveData(limit=l, accurracy=a, spacing=s)
                for d in data:
                    time = datetime.fromtimestamp(d.timestamp).strftime("%H:%M:%S")
                    print("Time: " + str(time) +
                          " Temp: " + str(d.temperature) +
                          " Humidity: " + str(d.humidity) +
                          " UV: " + str(d.Ultraviolet) +
                          " Pressure: " + str(d.pressure))
            elif cmd[:5] == "warn ":  # warn the user
                Main.warn(None, cmd[5:])
            elif cmd == "":
                pass
            else:
                print("Command not found")
            Main.notify_usr.notify()  # notify the lock
            Main.lock.release()  # release the lock

    def write(self, cmd):
        Main.lock.acquire()
        Main.command += cmd + "\n"
        Main.notify_cmd.notify()
        Main.lock.release()

# ====================  Commandline  ====================
# This is the commandline for the program. It is used to control the program.
# With this you can control the program without having to restart it.


def main():
    Main()
    exit()


if __name__ == "__main__":
    main()
