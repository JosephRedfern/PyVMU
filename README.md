Variense VMU931 Toolkit
=======================

This project aims at implementing a pure-python VMU931 toolkit, including both parsing and communication with the Variense VMU931 Device.

The VMU931 is a USB-based accelrometer, gyroscope and magnetometer.

So far, basic processing of all outputs: Quaternion, Euler Angles, Accelerometer, Magnetometer, Gyroscope and Heading.

Basic usage is as follows:

```
with VMU931Parser(device="/dev/tty.usbmodem1411") as vp:
    vp.toggle_euler() # Toggleoutput of Euler angles (OFF by default)
    vp.toggler_quaternion() # Toggle output of quaternion data (ON by default)
    vp.toggle_accelerometer()  # Toggle output of accelerometer data (OFF by default)

    for n in range(100): # Print 100 datapoints
        packet = vp.parse()
        print(packet)
```

vp.parse() also supports a `callback` argument, which is a function to be run on each incoming packet.
