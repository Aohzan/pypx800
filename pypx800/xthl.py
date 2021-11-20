"""IPX800 X-THL."""
from enum import Enum

from .ipx800 import IPX800


class XTHLTypes(str, Enum):
    Temperature = "TEMP"
    Humidity = "HUM"
    Luminosity = "LUM"


class XTHL:
    """Representing an IPX800 X-THL."""

    def __init__(self, ipx800: IPX800, xthl_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = xthl_id

    # @property
    def key(self, sensor_type: XTHLTypes) -> str:
        """Return the key to get the value from API call."""
        return f"THL{self.id}-{sensor_type.value}"

    @property
    async def temp(self) -> float:
        """Get temperature of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[self.key(sensor_type=XTHLTypes.Temperature)]

    @property
    async def hum(self) -> float:
        """Get humidity level of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[self.key(XTHLTypes.Humidity)]

    @property
    async def lum(self) -> int:
        """Get luminosity level of the X-THL."""
        params = {"Get": "XTHL"}
        response = await self._ipx.request_api(params)
        return response[self.key(XTHLTypes.Luminosity)]
