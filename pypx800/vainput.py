"""IPX800 Virtual Analog Input."""

from .ipx800 import IPX800


class VAInput:
    """Representing an IPX800 Virtual Analog Input."""

    def __init__(self, ipx800: IPX800, virtual_analog_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = virtual_analog_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"VA{self.id}"

    @property
    async def value(self) -> float:
        """Get Analog Input value."""
        params = {"Get": "VA"}
        response = await self._ipx.request_api(params)
        return response[self.key]

    async def set_value(self, value: float) -> None:
        """Set Virtual Analog input value."""
        params = {f"SetVA{self.id:02}": value}
        await self._ipx.request_api(params)
