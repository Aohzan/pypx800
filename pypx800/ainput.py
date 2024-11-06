"""IPX800 Analog Input."""

from .ipx800 import IPX800


class AInput:
    """Representing an IPX800 Analog Input."""

    def __init__(self, ipx800: IPX800, analog_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = analog_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"A{self.id}"

    @property
    async def value(self) -> float:
        """Get Analog Input value."""
        params = {"Get": "A"}
        response = await self._ipx.request_api(params)
        return response[self.key]
