Variense VMU931 Toolkit
=======================

This project aims at implementing a pure-python VMU931 toolkit, including both parsing and communication with the Variense VMU931 Device.

The [VMU931](http://variense.com/product/vmu931/) is a high resolution, USB-based accelerometer, gyroscope and magnetometer made by [Variense](http://variense.com/). Please note that this library is unofficial, and is not produced/endorsed by Variense.

So far, basic processing of all outputs is supported: Quaternion, Euler Angles, Accelerometer, Magnetometer, Gyroscope and Heading. There is basic support for toggling these outputs, but we don't currently process status messages (or support calibration/self-test). This should come in the future, and all pull requests are welcome.

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
