#!/usr/bin/env python3

import matplotlib.pyplot as plt
from variensevmu.vmu931 import VMU931Parser
from variensevmu import messages


# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
plt.ion()

figure = plt.figure()
quat_axes = figure.add_subplot(111)
quat_axes.set_title("Quaternions")
quat_axes.set_xlabel("Timestamp (ms)")
quat_axes.set_ylabel("Quaternion Value(°)")
quat_axes.set_ylim([-1, 1])

w_line, = quat_axes.plot([], [], label="W")
x_line, = quat_axes.plot([], [], label="X")
y_line, = quat_axes.plot([], [], label="Y")
z_line, = quat_axes.plot([], [], label="Z")

plt.legend()

ts_points = []
w_points = []
x_points = []
y_points = []
z_points = []

with VMU931Parser(quaternion=True) as vp:

    while True:
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Quaternion):
            ts, x, y, z, w = pkt
            ts_points.append(ts)
            w_points.append(w)
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)

        # Only plot every 10 points (still quite smooth), otherwise we risk being bottle-necked by matplotlib.
        if len(ts_points) % 10 == 0:
            # set_data is faster than drawing a whole new line
            w_line.set_data(ts_points[-1000:], w_points[-1000:])
            x_line.set_data(ts_points[-1000:], x_points[-1000:])
            y_line.set_data(ts_points[-1000:], y_points[-1000:])
            z_line.set_data(ts_points[-1000:], z_points[-1000:])

            quat_axes.relim()
            quat_axes.autoscale_view()
            figure.canvas.draw()

            # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
            plt.pause(0.00001)
