#! /usr/bin/env python3

from evdev import InputDevice, list_devices

if __name__ == '__main__':
    devices = [InputDevice(dev) for dev in list_devices()]
    print("The following input devices are found on your system")
    for device in devices:
        print(device)
