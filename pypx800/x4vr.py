"""IPX800 X-4VR."""
from .ipx800 import IPX800


class X4VR:
    """Representing an X-4VR output."""

    def __init__(self, ipx800: IPX800, ext_id: int, vr_id: int) -> None:
        """Initialize object."""
        self._ipx = ipx800
        self.ext_id = ext_id
        self.vr_id = vr_id
        self.vr_number = (ext_id - 1) * 4 + vr_id

    @property
    def key(self) -> str:
        """Return the key to get the value from API call."""
        return f"VR{self.ext_id}-{self.vr_id}"

    @property
    async def status(self) -> bool:
        """Return the current cover status."""
        params = {"Get": f"VR{self.ext_id}"}
        response = await self._ipx.request_api(params)
        return response[self.key] < 100

    @property
    async def level(self) -> int:
        """Return the current cover level."""
        params = {"Get": f"VR{self.ext_id}"}
        response = await self._ipx.request_api(params)
        return 100 - int(response[self.key])

    async def on(self) -> None:
        """Open cover."""
        params = {f"SetVR{self.vr_number:02}": "0"}
        await self._ipx.request_api(params)

    async def off(self) -> None:
        """Close cover."""
        params = {f"SetVR{self.vr_number:02}": "100"}
        await self._ipx.request_api(params)

    async def stop(self) -> None:
        """Stop cover."""
        params = {f"SetVR{self.vr_number:02}": "101"}
        await self._ipx.request_api(params)

    async def set_level(self, level: int) -> None:
        """Set cover level."""
        params = {f"SetVR{self.vr_number:02}": str(100 - level)}
        await self._ipx.request_api(params)

    async def set_pulse_down(self, impulse: int) -> None:
        """Set cover impulse down."""
        params = {f"SetPulseDOWN{self.vr_number:02}": str(impulse)}
        await self._ipx.request_api(params)

    async def set_pulse_up(self, impulse: int) -> None:
        """Set cover impulse up."""
        params = {f"SetPulseUP{self.vr_number:02}": str(impulse)}
        await self._ipx.request_api(params)
