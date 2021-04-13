"""IPX800 X-PWM."""
from . import IPX800

DEFAULT_TRANSITION = 500


class XPWM:
    """Representing an X-PWM channel."""

    def __init__(self, ipx800: IPX800, channel_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = channel_id

    @property
    async def status(self) -> bool:
        """Return the current X-PWM status."""
        params = {"Get": f"XPWM|{self.id}"}
        response = await self._ipx.request_api(params)
        return response[f"PWM{self.id}"] > 0

    @property
    async def level(self) -> int:
        """Return the current X-PWM level."""
        params = {"Get": f"XPWM|{self.id}"}
        response = await self._ipx.request_api(params)
        return response[f"PWM{self.id}"]

    @property
    async def level_all_channels(self) -> int:
        """Return the current X-PWM level."""
        params = {"Get": "XPWM|1-24"}
        return await self._ipx.request_api(params)

    async def on(self, time: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM."""
        params = {"SetPWM": self.id, "PWMValue": "100", "PWMDelay": time}
        await self._ipx.request_cgi(params)

    async def off(self, time: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-PWM."""
        params = {"SetPWM": self.id, "PWMValue": "0", "PWMDelay": time}
        await self._ipx.request_cgi(params)

    async def toggle(self, time: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-PWM."""
        if self.status:
            self.off(time)
        else:
            self.on(time)

    async def set_level(self, level, time: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM."""
        params = {"SetPWM": self.id, "PWMValue": level, "PWMDelay": time}
        await self._ipx.request_cgi(params)
