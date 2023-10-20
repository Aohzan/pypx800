"""IPX800 Counter."""
from .ipx800 import IPX800


class Counter:
    """Representing an IPX800 Counter."""

    def __init__(self, ipx800: IPX800, counter_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.id = counter_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"C{self.id}"

    @property
    async def value(self) -> float:
        """Get Counter value."""
        params = {"Get": "C"}
        response = await self._ipx.request_api(params)
        return response[self.key]

    async def set_value(self, value: int) -> None:
        """Set Counter value."""
        params = {f"SetC{self.id:02}": value}
        await self._ipx.request_api(params)

    async def increment(self, value: int = 1) -> None:
        """Increment Counter value."""
        params = {f"SetC{self.id:02}": f"+{value}"}
        await self._ipx.request_api(params)

    async def decrement(self, value: int = 1) -> None:
        """Increment Counter value."""
        params = {f"SetC{self.id:02}": f"-{value}"}
        await self._ipx.request_api(params)
