"""IPX800 X-THL."""
from . import IPX800


class XTHL:
    """Representing an IPX800 X-THL."""

    def __init__(self, ipx800: IPX800, xthl_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = xthl_id

    @property
    async def temp(self) -> float:
        """Get temperature of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[f"THL{self.id}-TEMP"]

    @property
    async def hum(self) -> float:
        """Get humidity level of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[f"THL{self.id}-HUM"]

    @property
    async def lum(self) -> int:
        """Get luminosity level of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[f"THL{self.id}-LUM"]
