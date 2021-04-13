"""IPX800 X-Dimmer."""
from . import IPX800

DEFAULT_TRANSITION = 500


class XDimmer:
    """Representing an X-Dimmer out."""

    def __init__(self, ipx800: IPX800, relay_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = relay_id

    @property
    async def status(self) -> bool:
        """Return the current X-Dimmer status."""
        params = {"Get": "G"}
        response = await self._ipx.request_api(params)
        return response[f"G{self.id}"]["Etat"] == "ON"

    @property
    async def level(self) -> int:
        """Return the current X-Dimmer level."""
        params = {"Get": "G"}
        response = await self._ipx.request_api(params)
        return response[f"G{self.id}"]["Valeur"]

    async def on(self, time: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer."""
        params = {f"SetG{self.id:02}": "101", "Time": time}
        await self._ipx.request_api(params)

    async def off(self, time: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-Dimmer."""
        params = {f"SetG{self.id:02}": "0", "Time": time}
        await self._ipx.request_api(params)

    async def toggle(self, time: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-Dimmer."""
        if await self.status:
            await self.off(time)
        else:
            await self.on(time)

    async def set_level(self, level: int, time: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer on a specific level."""
        params = {f"SetG{self.id:02}": level, "Time": time}
        await self._ipx.request_api(params)
