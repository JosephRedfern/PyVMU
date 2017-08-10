#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pyvmu.vmu931 import VMU931Parser
from pyvmu import messages


# We want to be able to update the plot in real-time, plt.ion() is non-blocking.
plt.ion()

figure = plt.figure()
head_axes = figure.add_subplot(111)
head_axes.set_title("Compass Heading")
head_axes.set_xlabel("Timestamp (ms)")
head_axes.set_ylabel("Heading (°)")
head_axes.set_ylim([0, 360])

head_line, = head_axes.plot([], [], label="Heading (°)")

plt.legend()

ts_points = []
h_points = []

with VMU931Parser(heading=True) as vp:

    while True:
        pkt = vp.parse()

        if isinstance(pkt, messages.Status):
            print(pkt)

        if isinstance(pkt, messages.Heading):
            ts, h = pkt
            ts_points.append(ts)
            h_points.append(h)

        # Only plot every 100 points (still quite smooth), otherwise we're bottle-necked by matplotlib.
        # Note that when angular data is not being streamed, the faster update rate is assumed.
        if len(ts_points) % 10 == 0:

            # set_data is faster than drawing a whole new line
            head_line.set_data(ts_points[-1000:], h_points[-1000:])

            head_axes.relim()
            head_axes.autoscale_view()
            figure.canvas.draw()

            # Pause to force redraw. Actually blocks until re-draw is complete, 0.00001 is an arbitrary small number.
            plt.pause(0.00001)
