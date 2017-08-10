Variense VMU931 Toolkit
=======================

This project aims at implementing a pure-python VMU931 toolkit,
including both parsing and communication with the Variense VMU931
Device.

The `VMU931 <http://variense.com/product/vmu931/>`__ is a high
resolution, USB-based accelerometer, gyroscope and magnetometer made by
`Variense <http://variense.com/>`__. Please note that this library is
unofficial, and is not produced/endorsed by Variense.

So far, basic processing of all outputs is supported: Quaternion, Euler
Angles, Accelerometer, Magnetometer, Gyroscope and Heading. These
outputs can be controlled using the ``set_*`` methods, or by pasing in
flags to the VMU931Parser constructor. Status messages are parsed,
allowing setting rather than toggling of different data streams. The
toolkit does not currently support self-test or callibration
functionality.

Basic usage is as follows:

::

    with VMU931Parser(device="/dev/tty.usbmodem1411", euler=True, accelerometer=True) as vp:
        for n in range(100): # Print 100 datapoints
            packet = vp.parse()
            print(packet)

vp.parse() also supports a ``callback`` argument, which is a function to
be run on each incoming packet.

For more examples, please see the `examples/ <examples/>`__ directory.

.. |Documentation Status| image:: https://readthedocs.org/projects/pyvmu/badge/?version=latest
   :target: http://pyvmu.readthedocs.io/en/latest/?badge=latest
