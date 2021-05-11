# pypx800 - Python GCE IPX800 v4

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

## IPX800 parameters

- host: ip or hostname (mandatory)
- port: (default: `80`)
- api_key: (mandatory)
- user: name of user or admin (for X-PWM only)
- password: password of user or admin (for X-PWM only)
- request_retries: number of request retries on error (default: `3`)
- request_timeout: timeout for request (default: `5`)
- request_checkstatus: true to raise error if IPX800 return no success result like partial result, after `request_retries` retries (default: `True`)
- session: aiohttp.client.ClientSession

## Example

```python
import asyncio

from pypx800 import (IPX800, X4FP, X4VR, XPWM, XTHL, AInput, VAInput, DInput, Relay,
                     VInput, VOutput, XDimmer)


async def main():
    async with IPX800(host='192.168.1.123', api_key='xxx') as ipx:
        data = await ipx.global_get()
        print("all values:", data)
        
        print("## Relay ##")
        r15 = Relay(ipx, 15)
        print(await r15.status)
        await r15.on()
        await r15.off()

        print("## X-Dimmer ##")
        g1 = XDimmer(ipx, 1)
        await g1.on()  # default 500 milliseconds
        await g1.set_level(80)  # default 500 milliseconds delay
        await g1.set_level(20, 0)  # 0 milliseconds delay
        await g1.off(2000)  # 2 seconds delay
        print(await g1.level)
        print(await g1.status)
        
        print("## X-PWM ##")
        pwm1 = XPWM(ipx, 1)
        await pwm1.on()  # default 500 milliseconds delay
        await pwm1.on(1000)  # 1 second delay
        await pwm1.set_level(50)  # default 500 milliseconds delay
        await pwm1.set_level(20, 0)  # 0 millisecond delay
        print(await pwm1.status)
        await pwm1.off()
        
        print("## Analog Input ##")
        print(await AInput(ipx, 1).value)

        print("## Virtual Analog Input ##")
        print(await VAInput(ipx, 1).value)
    
        print("## Digital Output ##")
        d1 = DInput(ipx, 1)
        print(await d1.value)

        print("## Virtual Input ##")
        vi = VInput(ipx, 3)
        await vi.on()
        print(await vi.status)

        print("## Virtual Output ##")
        vo = VOutput(ipx, 12)
        await vo.on()
        print(await vo.status)

        print("## X-THL ##")
        sensor = XTHL(ipx, 1)
        print(await sensor.temp)
        print(await sensor.hum)
        print(await sensor.lum)

        print("## X-4VR ##")
        vr = X4VR(ipx, 1, 3)  # Extension number, VR number
        await vr.on()
        await vr.set_level(30)
        print(await vr.status)
        print(await vr.level)

        print("## X-4FP ##")
        fp = X4FP(ipx, 1, 3)  # Extension number, Zone number
        # 0 confort, 1 Eco, 2 Hors Gel, 3 Stop, 4 Confort -1, 5 Confort -2
        print(await fp.status)
        await fp.set_mode(1)
        await fp.set_mode_all(1)  # set for all zones
        print(await fp.status)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

## Credits

Thank to [d3mi1](https://github.com/d4mi1/python-ipx800) and [marcaurele](https://github.com/marcaurele/gce-ipx800) for inspiration :)
