"""IPX800 Virtual Analog Input."""
from . import IPX800


class VAInput:
    """Representing an IPX800 Virtual Analog Input."""

    def __init__(self, ipx800: IPX800, virtual_analog_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = virtual_analog_id

    @property
    async def value(self) -> float:
        """Get Analog Input value."""
        params = {"Get": "VA"}
        response = await self._ipx.request_api(params)
        return response[f"VA{self.id}"]
