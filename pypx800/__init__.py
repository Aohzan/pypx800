import collections
import requests
from random import randrange
from time import sleep

DEFAULT_TRANSITION = 500


class IPX800:
    """Class representing the IPX800 and its API"""

    def __init__(self, host, port, api_key, username="", password="", retries=3):
        self.host = host
        self.port = port
        self.api_key = api_key
        self.username = username
        self.password = password

        self.retries = retries

        self._api_url = f"http://{host}:{port}/api/xdevices.json"
        self._cgi_url = f"http://{username}:{password}@{host}:{port}/user/api.cgi"

    def _request_api(self, params):
        request_retries = self.retries
        params_with_api = {"key": self.api_key}
        params_with_api.update(params)
        while request_retries > 0:
            r = requests.get(self._api_url, params=params_with_api, timeout=2)
            r.raise_for_status()
            content = r.json()
            result = content.get("status", None)
            if result == "Success":
                return content
            request_retries -= 1
            sleep(randrange(200, 800)/1000)
            pass
        raise Exception(
            "IPX800 api request error, url: %s`r%s",
            f"{r.request.url[0:r.request.url.index('?key=') + 5]}removed{r.request.url[r.request.url.index('&')::]}",
            content,
        )

    def _request_cgi(self, params):
        request_retries = self.retries
        while request_retries > 0:
            r = requests.get(self._cgi_url, params=params, timeout=2)
            r.raise_for_status()
            content = r.text
            if "Success" in content:
                return content
            request_retries -= 1
            sleep(randrange(200, 800)/1000)
            pass
        raise Exception(
            "IPX800 cgi request error, url: %s`r%s",
            f"{r.request.url[0:r.request.url.index('http://') + 7]}removed{r.request.url[r.request.url.index('@')::]}",
            r.request.content,
        )

    def ping(self):
        try:
            self._request_api({"Get": "R"})
            return True
        except:
            pass
        return False

    def global_get(self):
        values = self._request_api({"Get": "all"})
        # add separated XPWM values if username for control them have been specified
        if self.username:
            values.update(
                self._request_api({"Get": "XPWM|1-24"})
            )
        return values


class Relay(IPX800):
    """Representing an IPX800 relay."""

    def __init__(self, ipx, relay_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = relay_id

    @property
    def status(self) -> bool:
        """Return the current relay status."""
        params = {"Get": "R"}
        response = self._request_api(params)
        return response[f"R{self.id}"] == 1

    def on(self):
        """Turn on a relay."""
        params = {"SetR": self.id}
        self._request_api(params)

    def off(self):
        """Turn off a relay."""
        params = {"ClearR": self.id}
        self._request_api(params)

    def toggle(self):
        """Toggle a relay."""
        params = {"ToggleR": self.id}
        self._request_api(params)


class VOutput(IPX800):
    """Representing an IPX800 Virtual Out."""

    def __init__(self, ipx, relay_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = relay_id

    @property
    def status(self) -> bool:
        params = {"Get": "VO"}
        response = self._request_api(params)
        return response[f"VO{self.id}"] == 1

    def on(self):
        params = {"SetVO": self.id}
        self._request_api(params)

    def off(self):
        params = {"ClearVO": self.id}
        self._request_api(params)

    def toggle(self):
        params = {"ToggleVO": self.id}
        self._request_api(params)


class VInput(IPX800):
    """Representing an IPX800 Virtual In."""

    def __init__(self, ipx, relay_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = relay_id

    @property
    def status(self) -> bool:
        params = {"Get": "VI"}
        response = self._request_api(params)
        return response[f"VI{self.id}"] == 1

    def on(self):
        params = {"SetVI": self.id}
        self._request_api(params)

    def off(self):
        params = {"ClearVI": self.id}
        self._request_api(params)

    def toggle(self):
        params = {"ToggleVI": self.id}
        self._request_api(params)


class XDimmer(IPX800):
    """Representing an X-Dimmer out."""

    def __init__(self, ipx, relay_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = relay_id

    @property
    def status(self) -> bool:
        """Return the current X-Dimmer status."""
        params = {"Get": "G"}
        response = self._request_api(params)
        return response[f"G{self.id}"]["Etat"] == "ON"

    @property
    def level(self) -> int:
        """Return the current X-Dimmer level."""
        params = {"Get": "G"}
        response = self._request_api(params)
        return response[f"G{self.id}"]["Valeur"]

    def on(self, time=DEFAULT_TRANSITION):
        """Turn on a X-Dimmer."""
        params = {f"SetG{self.id:02}": "101", "Time": time}
        self._request_api(params)

    def off(self, time=DEFAULT_TRANSITION):
        """Turn off a X-Dimmer."""
        params = {f"SetG{self.id:02}": "0", "Time": time}
        self._request_api(params)

    def toggle(self, time=DEFAULT_TRANSITION):
        """Toggle a X-Dimmer."""
        if self.status:
            self.off(time)
        else:
            self.on(time)

    def set_level(self, level, time=DEFAULT_TRANSITION):
        """Turn on a X-Dimmer."""
        params = {f"SetG{self.id:02}": str(int(level)), "Time": time}
        self._request_api(params)


class XPWM(IPX800):
    """Representing an X-PWM channel."""

    def __init__(self, ipx, channel_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = channel_id

    @property
    def status(self) -> bool:
        """Return the current X-PWM status."""
        params = {"Get": f"XPWM|{self.id}"}
        response = self._request_api(params)
        return response[f"PWM{self.id}"] > 0

    @property
    def level(self) -> int:
        """Return the current X-PWM level."""
        params = {"Get": f"XPWM|{self.id}"}
        response = self._request_api(params)
        return response[f"PWM{self.id}"]

    @property
    def level_all_channels(self) -> int:
        """Return the current X-PWM level."""
        params = {"Get": f"XPWM|1-24"}
        response = self._request_api(params)
        return response

    def on(self, time=DEFAULT_TRANSITION):
        """Turn on a X-PWM."""
        params = {f"SetPWM": self.id, "PWMValue": "100", "PWMDelay": time}
        self._request_cgi(params)

    def off(self, time=DEFAULT_TRANSITION):
        """Turn off a X-PWM."""
        params = {f"SetPWM": self.id, "PWMValue": "0", "PWMDelay": time}
        self._request_cgi(params)

    def toggle(self, time=DEFAULT_TRANSITION):
        """Toggle a X-PWM."""
        if self.status:
            self.off(time)
        else:
            self.on(time)

    def set_level(self, level, time=DEFAULT_TRANSITION):
        """Turn on a X-PWM."""
        params = {f"SetPWM": self.id, "PWMValue": str(
            int(level)), "PWMDelay": time}
        self._request_cgi(params)


class AInput(IPX800):
    """Representing an IPX800 Analog Input."""

    def __init__(self, ipx, analog_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = analog_id

    @property
    def value(self) -> float:
        params = {"Get": "A"}
        response = self._request_api(params)
        return response[f"A{self.id}"]


class DInput(IPX800):
    """Representing an IPX800 Digital Input."""

    def __init__(self, ipx, digital_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = digital_id

    @property
    def value(self) -> bool:
        params = {"Get": "D"}
        response = self._request_api(params)
        return response[f"D{self.id}"] == 1


class XTHL(IPX800):
    """Representing an IPX800 X-THL."""

    def __init__(self, ipx, xthl_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.id = xthl_id

    @property
    def temp(self) -> float:
        params = {"Get": "XTHL"}
        response = self._request_api(params)
        return response[f"THL{self.id}-TEMP"]

    @property
    def hum(self) -> float:
        params = {"Get": "XTHL"}
        response = self._request_api(params)
        return response[f"THL{self.id}-HUM"]

    @property
    def lum(self) -> int:
        params = {"Get": "XTHL"}
        response = self._request_api(params)
        return response[f"THL{self.id}-LUM"]


class X4VR(IPX800):
    """Representing an X-4VR output."""

    def __init__(self, ipx, ext_id: int, vr_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.ext_id = ext_id
        self.vr_id = vr_id
        self.vr_number = (ext_id - 1) * 4 + vr_id

    @property
    def status(self) -> bool:
        """Return the current VR status."""
        params = {"Get": f"VR{self.ext_id}"}
        response = self._request_api(params)
        return response[f"VR{self.ext_id}-{self.vr_id}"] < 100

    @property
    def level(self) -> int:
        """Return the current VR level."""
        params = {"Get": f"VR{self.ext_id}"}
        response = self._request_api(params)
        return 100 - int(response[f"VR{self.ext_id}-{self.vr_id}"])

    def on(self):
        """Open VR."""
        params = {f"SetVR{self.vr_number:02}": "0"}
        self._request_api(params)

    def off(self):
        """Close VR."""
        params = {f"SetVR{self.vr_number:02}": "100"}
        self._request_api(params)

    def stop(self):
        """Stop VR."""
        params = {f"SetVR{self.vr_number:02}": "101"}
        self._request_api(params)

    def set_level(self, level: int):
        """Set VR level."""
        params = {f"SetVR{self.vr_number:02}": str(100 - level)}
        self._request_api(params)


class X4FP(IPX800):
    """Representing an X-4FP output."""

    def __init__(self, ipx, ext_id: int, zone_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.ext_id = ext_id
        self.zone_id = zone_id
        self.fp_number = (ext_id - 1) * 4 + zone_id

    @property
    def status(self) -> bool:
        """Return the current FP status."""
        params = {"Get": f"FP"}
        response = self._request_api(params)
        return response[f"FP{self.ext_id} Zone {self.zone_id}"]

    def set_mode(self, mode):
        """Set FP mode."""
        params = {f"SetFP{self.fp_number:02}": mode}
        self._request_api(params)

    def set_mode_all(self, mode):
        """Set FP mode for all zones."""
        params = {f"SetFP00": mode}
        self._request_api(params)
