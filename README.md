# pypx800 - Python GCE IPX800

Control the IPX800 v4 ans its extensions: X-PWM, X-THL, X-4VR, X-4FP, X-8R, X-8D, X-24D and X-Dimmer trough:

- Relay
- Virtual output
- Virtual input
- Digital input
- Analog input
- X-Dimmer output
- X-PWM channel
- X-THL (temp, hum, lux)
- X-4VR output
- X-4FP zone

## Parameters

- host: ip or hostname
- port
- api key
- user: name of user or admin (for X-PWM only)
- password: password of user or admin (for X-PWM only)
- retries: number of request retries on error (default: 3)

## Example

```python
from pypx800 import *

ipx = IPX800('192.168.1.240','80','apikey','user', 'password')
print (ipx.ping())
values = ipx.global_get()
print (values)

# Relay
r14 = Relay(ipx, 14)
r14.on()
print (r14.status)
r14.off()

# X-Dimmer
g1 = XDimmer(ipx, 3)
g1.on() # default 0.5 second delay
g1.set_level(80) # default 0.5 second delay
g1.set_level(20, 0) # 0 second delay
print (g1.level)
print (g1.status)

# X-PWM
pwm1 = XPWM(ipx, 12)
pwm1.on() # default 0.5 second delay
pwm1.on(1000) # 1 second delay
pwm1.set_level(50) # default 0.5 second delay
pwm1.set_level(20, 0) # 0 second delay
print (pwm1.status)
pwm1.off()

# Analog Input
print (AInput(1).value)

# Digital Input
d1 = Dintput(ipx, 1)
print (d1.value)

# Virtual Input
vi = VInput(ipx, 3)
vi.on()
print (vi.status)

# Virtual Output
vo = VOutput(ipx, 12)
vo.on()
print (vo.status)

# X-THL
sensor = XTHRL(ipx, 1)
print (sensor.temp)
print (sensor.hum)
print (sensor.lum)

# X-4VR
vr = X4VR(ipx, 1, 3) # Extension number, VR number
vr.on()
vr.level(30)
print (vr.status)
print (vr.level)

# X-4FP
fp = X4FP(ipx, 1, 3) # Extension number, Zone number
fp.set_mode(2) # 0 confort, 1 Eco, 2 Hors Gel, 3 Stop, 4 Confort -1, 5 Confort -2
fp.set_mode_all(2) # set for all zones
print (fp.status)
```

## Credits

Thank to [d3mi1](https://github.com/d4mi1/python-ipx800) and [marcaurele](https://github.com/marcaurele/gce-ipx800) for inspiration :)
