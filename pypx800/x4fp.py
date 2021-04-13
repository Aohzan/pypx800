"""IPX800 X-4FP."""
from . import IPX800


class X4FP:
    """Representing an X-4FP output."""

    def __init__(self, ipx800: IPX800, ext_id: int, zone_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.ext_id = ext_id
        self.zone_id = zone_id
        self.fp_number = (ext_id - 1) * 4 + zone_id

    @property
    async def status(self) -> bool:
        """Return the current FP status."""
        params = {"Get": "FP"}
        response = await self._ipx.request_api(params)
        return response[f"FP{self.ext_id} Zone {self.zone_id}"]

    async def set_mode(self, mode) -> None:
        """Set FP mode."""
        params = {f"SetFP{self.fp_number:02}": mode}
        await self._ipx.request_api(params)

    async def set_mode_all(self, mode) -> None:
        """Set FP mode for all zones."""
        params = {"SetFP00": mode}
        await self._ipx.request_api(params)
