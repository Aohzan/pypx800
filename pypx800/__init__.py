import collections
import requests

DEFAULT_TRANSITION = 500


class IPX800:
    """Class representing the IPX800 and its API"""

    def __init__(self, host, port, api_key, username="Undefined", password="Undefined"):
        self.host = host
        self.port = port
        self.api_key = api_key
        self.username = username
        self.password = password

        self._api_url = f"http://{host}:{port}/api/xdevices.json"
        self._cgi_url = f"http://{username}:{password}@{host}:{port}/user/api.cgi"

    def _request_api(self, params):
        params_with_api = {"key": self.api_key}
        params_with_api.update(params)
        r = requests.get(self._api_url, params=params_with_api, timeout=2)
        r.raise_for_status()
        content = r.json()
        result = content.get("status", None)
        if result == "Success":
            return content
        else:
            raise Exception(
                "IPX800 api request error, url: %s`r%s",
                f"{r.request.url[0:r.request.url.index('?key=') + 5]}removed{r.request.url[r.request.url.index('&')::]}",
                content,
            )

    def _request_cgi(self, params):
        r = requests.get(self._cgi_url, params=params, timeout=2)
        r.raise_for_status()
        content = r.text
        if "Success" in content:
            return content
        else:
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
        values.update(
            self._request_api({"Get": "XPWM|1-24"})
        )  # add separated XPWM values
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

    def on(self) -> bool:
        """Turn on a relay and return True if it was successful."""
        params = {"SetR": self.id}
        self._request_api(params)
        return True

    def off(self) -> bool:
        """Turn off a relay and return True if it was successful."""
        params = {"ClearR": self.id}
        self._request_api(params)
        return True

    def toggle(self) -> bool:
        """Toggle a relay and return True if it was successful."""
        params = {"ToggleR": self.id}
        self._request_api(params)
        return True


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

    def on(self) -> bool:
        params = {"SetVO": self.id}
        self._request_api(params)
        return True

    def off(self) -> bool:
        params = {"ClearVO": self.id}
        self._request_api(params)
        return True

    def toggle(self) -> bool:
        params = {"ToggleVO": self.id}
        self._request_api(params)
        return True


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

    def on(self) -> bool:
        params = {"SetVI": self.id}
        self._request_api(params)
        return True

    def off(self) -> bool:
        params = {"ClearVI": self.id}
        self._request_api(params)
        return True

    def toggle(self) -> bool:
        params = {"ToggleVI": self.id}
        self._request_api(params)
        return True


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

    def on(self, time=DEFAULT_TRANSITION) -> bool:
        """Turn on a X-Dimmer and return True if it was successful."""
        params = {f"SetG{self.id:02}": "101", "Time": time}
        self._request_api(params)
        return True

    def off(self, time=DEFAULT_TRANSITION) -> bool:
        """Turn off a X-Dimmer and return True if it was successful."""
        params = {f"SetG{self.id:02}": "0", "Time": time}
        self._request_api(params)
        return True

    def toggle(self) -> bool:
        """Toggle a X-Dimmer and return True if it was successful."""
        if self.status:
            self.off()
            return False
        self.on()
        return True

    def set_level(self, level, time=DEFAULT_TRANSITION) -> bool:
        """Turn on a X-Dimmer and return True if it was successful."""
        params = {f"SetG{self.id:02}": str(int(level)), "Time": time}
        self._request_api(params)
        return True


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

    def on(self, time=DEFAULT_TRANSITION) -> bool:
        """Turn on a X-PWM and return True if it was successful."""
        params = {f"SetPWM": self.id, "PWMValue": "100", "PWMDelay": time}
        self._request_cgi(params)
        return True

    def off(self, time=DEFAULT_TRANSITION) -> bool:
        """Turn off a X-PWM and return True if it was successful."""
        params = {f"SetPWM": self.id, "PWMValue": "0", "PWMDelay": time}
        self._request_cgi(params)
        return True

    def toggle(self) -> bool:
        """Toggle a X-PWM and return True if it was successful."""
        if self.status:
            self.off()
            return False
        self.on()
        return True

    def set_level(self, level, time=DEFAULT_TRANSITION) -> bool:
        """Turn on a X-PWM and return True if it was successful."""
        params = {f"SetPWM": self.id, "PWMValue": str(int(level)), "PWMDelay": time}
        self._request_cgi(params)
        return True


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
    """Representing an X-Dimmer out."""

    def __init__(self, ipx, ext_id: int, vr_id: int):
        super().__init__(ipx.host, ipx.port, ipx.api_key, ipx.username, ipx.password)
        self.ext_id = ext_id
        self.vr_id = vr_id
        self.vr_number = ext_id * vr_id

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

    def on(self) -> bool:
        """Open VR."""
        params = {f"SetVR{self.vr_number:02}": "100"}
        self._request_api(params)
        return True

    def off(self) -> bool:
        """Close VR."""
        params = {f"SetVR{self.vr_number:02}": "0"}
        self._request_api(params)
        return True

    def stop(self) -> bool:
        """Stop VR."""
        params = {f"SetVR{self.vr_number:02}": "101"}
        self._request_api(params)
        return True

    def set_level(self, level: int) -> bool:
        """Set VR level."""
        params = {f"SetVR{self.vr_number:02}": str(100 - level)}
        self._request_api(params)
        return True
