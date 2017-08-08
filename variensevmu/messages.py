from collections import namedtuple

Accelerometer = namedtuple('Accelerometer', 'timestamp x y z')
Magnetometer = namedtuple('Magnetometer', 'timestamp x y z')
Gyroscope = namedtuple('Gyroscope', 'timestamp x y z')
Euler = namedtuple('Euler', 'timestamp x y z')

Quaternion = namedtuple('Quaternion', 'timestamp w x y z')

Heading = namedtuple('Heading', 'timestamp h')
