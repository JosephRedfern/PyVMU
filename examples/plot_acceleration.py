#!/usr/bin/env python3

import matplotlib.pyplot as plt
from variensevmu.vmu931 import VMU931Parser
from variensevmu import messages


# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
plt.ion()

figure = plt.figure()
acc_axes = figure.add_subplot(111)
acc_axes.set_title("Accelerometer")
acc_axes.set_xlabel("Timestamp (ms)")
acc_axes.set_ylabel("Force (g)")
acc_axes.set_ylim([-8, 8])  # -8 <= g <= 8

x_line, = acc_axes.plot([], [], label="X")
y_line, = acc_axes.plot([], [], label="Y")
z_line, = acc_axes.plot([], [], label="Z")

plt.legend()

ts_points = []
x_points = []
y_points = []
z_points = []

with VMU931Parser(accelerometer=True) as vp:

    vp.set_accelerometer_resolution(8)  # Set resolution of accelerometer to 8g.

    while True:
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Accelerometer):
            ts, x, y, z = pkt
            ts_points.append(ts)
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)

        # Only plot every 100 points (still quite smooth), otherwise we're bottle-necked by matplotlib.
        # Note that when angular data is not being streamed, the faster update rate is assumed.
        if len(ts_points) % 100 == 0:

            # set_data is faster than drawing a whole new line
            x_line.set_data(ts_points[-1000:], x_points[-1000:])
            y_line.set_data(ts_points[-1000:], y_points[-1000:])
            z_line.set_data(ts_points[-1000:], z_points[-1000:])

            acc_axes.relim()
            acc_axes.autoscale_view()
            figure.canvas.draw()

            # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
            plt.pause(0.00001)
