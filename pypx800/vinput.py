"""IPX800 Virtual Input."""
from . import IPX800


class VInput:
    """Representing an IPX800 Virtual Input."""

    def __init__(self, ipx800: IPX800, relay_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = relay_id

    @property
    async def status(self) -> bool:
        """Get status of a Virtual Input."""
        params = {"Get": "VI"}
        response = await self._ipx.request_api(params)
        return response[f"VI{self.id}"] == 1

    async def on(self) -> None:
        """Turn on a Virtual Input."""
        params = {"SetVI": self.id}
        await self._ipx.request_api(params)

    async def off(self) -> None:
        """Turn off a Virtual Input."""
        params = {"ClearVI": self.id}
        await self._ipx.request_api(params)

    async def toggle(self) -> None:
        """Toggle a Virtual Input."""
        params = {"ToggleVI": self.id}
        await self._ipx.request_api(params)
