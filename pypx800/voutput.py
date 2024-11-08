"""IPX800 Virtual Output."""

from .ipx800 import IPX800


class VOutput:
    """Representing an IPX800 Virtual Output."""

    def __init__(self, ipx800: IPX800, relay_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = relay_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"VO{self.id}"

    @property
    async def status(self) -> bool:
        """Get status of a Virtual Output."""
        params = {"Get": "VO"}
        response = await self._ipx.request_api(params)
        return response[self.key] == 1

    async def on(self) -> None:
        """Turn on a Virtual Output."""
        params = {"SetVO": self.id}
        await self._ipx.request_api(params)

    async def off(self) -> None:
        """Turn off a Virtual Output."""
        params = {"ClearVO": self.id}
        await self._ipx.request_api(params)

    async def toggle(self) -> None:
        """Toggle a Virtual Output."""
        params = {"ToggleVO": self.id}
        await self._ipx.request_api(params)
