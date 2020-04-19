# pypx800 - Python GCE IPX800 

Control the IPX800, X-PWM, X-8R, X-8D, X-24D and X-Dimmer trough:
* relay
* virtual output
* virtual input
* digital input
* analog input
* xdimmer output
* xpwm channel

## Parameters
* host: ip or hostname
* port
* api key
* user: name of user or admin (for X-PWM only)
* password: password of user or admin (for X-PWM only)

## Example
```python
from pypx800 import IPX800 as pypx800

ipx = pypx800('192.168.1.240','80','apikey','user', 'password')
values = ipx.global_get()

# Relay
r14 = ipx.relays[14]
r14.on()
print (r14.status)
r14.off()

# X-Dimmer
g1 = ipx.xdimmers[3]
g1.on()
g1.set_level(80)
print (g1.level)
print (g1.status)

# X-PWM
pwm1 = ipx.xpwm[5]
pwm1.on()
pwm1.set_level(50)
print (pwm1.status)
pwm1.off()

# Analog Input
print (ipx.analogin[1].value)

# Digital Input
d1 = ipx.digitalin[1]
print (d1.value)

# Virtual Input
vi = ipx.virtualinput[4]
vi.on()
print (vi.status)

# Virtual Output
vo = ipx.virtualoutput[4]
vo.on()
print (vo.status)
```

## Credits
Thank to [d3mi1](https://github.com/d4mi1/python-ipx800) and [marcaurele](https://github.com/marcaurele/gce-ipx800) to inspiration :)