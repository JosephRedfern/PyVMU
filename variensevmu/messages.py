from collections import namedtuple

Accelerometer = namedtuple('Accelerometer', ["timestamp", "x", "y", "z"])
Magnetometer = namedtuple('Magnetometer', ['timestamp', 'x', 'y', 'z'])
Gyroscope = namedtuple('Gyroscope', ['timestamp', 'x', 'y', 'z'])
Euler = namedtuple('Euler', ['timestamp', 'x', 'y', 'z'])

Quaternion = namedtuple('Quaternion', ['timestamp', 'w', 'x', 'y', 'z'])

Heading = namedtuple('Heading', ['timestamp', 'h'])

Status = namedtuple('Status', ['magnetometer_enabled',
                               'gyroscope_enabled',
                               'accelerometer_enabled',
                               'gyroscope_resolution',
                               'accelerometer_resolution',
                               'low_output_rate',
                               'heading_streaming',
                               'euler_streaming',
                               'magnetometer_streaming',
                               'quaternions_streaming',
                               'gyroscope_streaming',
                               'accelerometer_streaming'])
