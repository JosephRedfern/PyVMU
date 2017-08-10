from pyvmu.vmu931 import VMU931Parser
import time

to_try = [chr(c) for c in range(ord('a'), ord('z')+1) if chr(c) not in ('e', 'q', 'h', 'a', 'g', 'c', 's', 't', 'l', 'b')][::-1]

to_try += range(8,10)

to_try += [chr(c) for c in range(ord('A'), ord('Z'))]

n = 6

with VMU931Parser() as vp:
    vp._send_message('var{}'.format(to_try[n]))
    print("sending {}".format(to_try[n]))
    while True:
        print(vp.parse())


