"""IPX800 Digital Input ."""

from .ipx800 import IPX800


class DInput:
    """Representing an IPX800 Digital Input."""

    def __init__(self, ipx800: IPX800, digital_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = digital_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"D{self.id}"

    @property
    async def value(self) -> bool:
        """Get Digital Input value."""
        params = {"Get": "D"}
        response = await self._ipx.request_api(params)
        return response[self.key] == 1
