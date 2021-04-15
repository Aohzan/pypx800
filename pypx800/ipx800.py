"""Get information and control a GCE IPX800v4."""
import asyncio
import socket
from time import sleep

import aiohttp
import async_timeout

from .exceptions import (
    Ipx800CannotConnectError,
    Ipx800InvalidAuthError,
    Ipx800RequestError,
)


class IPX800:
    """Class representing the IPX800 and its API."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 80,
        username: str = None,
        password: str = None,
        request_retries: int = 3,
        request_timeout: int = 5,
        request_checkstatus: bool = True,
        session: aiohttp.client.ClientSession = None,
    ) -> None:
        """Init a IPX800v4 API."""
        self.host = host
        self.port = port
        self._api_key = api_key
        self._username = username
        self._password = password

        self._request_retries = request_retries
        self._request_timeout = request_timeout
        self._request_checkstatus = request_checkstatus

        self._api_url = f"http://{host}:{port}/api/xdevices.json"
        self._cgi_url = f"http://{host}:{port}/user/api.cgi"

        self._session = session
        self._close_session = False

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

    async def request_api(self, params: dict) -> dict:
        """Make a request to get the IPX800 JSON API."""
        params_with_api = {"key": self._api_key}
        params_with_api.update(params)

        try:
            request_retries = self._request_retries
            while request_retries > 0:
                with async_timeout.timeout(self._request_timeout):
                    response = await self._session.get(
                        self._api_url,
                        params=params_with_api,
                    )

                if response.status:
                    content = await response.json()
                    response.close()

                    if (
                        not self._request_checkstatus
                        or content.get("status") == "Success"
                    ):
                        return content

                request_retries -= 1

            raise Ipx800RequestError("IPX800 API request error")

        except asyncio.TimeoutError as exception:
            raise Ipx800CannotConnectError(
                "Timeout occurred while connecting to IPX800."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Ipx800CannotConnectError(
                "Error occurred while communicating with the IPX800."
            ) from exception

    async def request_cgi(self, params: dict) -> dict:
        """Make a request to get the IPX800 CGI API."""
        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        try:
            request_retries = self._request_retries
            while request_retries > 0:
                with async_timeout.timeout(self._request_timeout):
                    response = await self._session.get(
                        self._cgi_url,
                        auth=auth,
                        params=params,
                    )

                if response.status == 401:
                    raise Ipx800InvalidAuthError("Auth failed on the IPX800.")

                if response.status:
                    content = await response.text()
                    response.close()
                    if not self._request_checkstatus or "Success" in content:
                        return content

                request_retries -= 1
                sleep(1)

            raise Ipx800RequestError("IPX800 API request error")

        except asyncio.TimeoutError as exception:
            raise Ipx800CannotConnectError(
                "Timeout occurred while connecting to IPX800."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Ipx800CannotConnectError(
                "Error occurred while communicating with the IPX800."
            ) from exception

    async def ping(self) -> bool:
        """Return True if the IPX800 answer to API request."""
        try:
            result = await self.request_api({"Get": "R"})
            return result.get("status") == "Success"
        except Ipx800CannotConnectError:
            pass
        return False

    async def global_get(self) -> dict:
        """Get all values from the IPX800 answer."""
        values = await self.request_api({"Get": "all"})
        # add separated XPWM values if username and password set
        if self._username and self._password:
            values.update(await self.request_api({"Get": "XPWM|1-24"}))
        return values

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit."""
        await self.close()
