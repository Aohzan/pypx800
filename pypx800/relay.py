"""IPX800 relay."""
from . import IPX800


class Relay:
    """Representing an IPX800 relay."""

    def __init__(self, ipx800: IPX800, relay_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = relay_id

    @property
    async def status(self) -> bool:
        """Return the current relay status."""
        params = {"Get": "R"}
        response = await self._ipx.request_api(params)
        return response[f"R{self.id}"] == 1

    async def on(self) -> None:
        """Turn on a relay."""
        params = {"SetR": self.id}
        await self._ipx.request_api(params)

    async def off(self) -> None:
        """Turn off a relay."""
        params = {"ClearR": self.id}
        await self._ipx.request_api(params)

    async def toggle(self) -> None:
        """Toggle a relay."""
        params = {"ToggleR": self.id}
        await self._ipx.request_api(params)
