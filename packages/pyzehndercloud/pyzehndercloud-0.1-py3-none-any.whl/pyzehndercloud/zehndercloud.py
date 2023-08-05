import json
import logging

import aiohttp
from aiohttp import client_exceptions

from pyzehndercloud import AuthError
from pyzehndercloud.auth import AbstractAuth

_LOGGER = logging.getLogger(__name__)

API_ENDPOINT = "https://zehnder-prod-we-apim.azure-api.net/cloud/api/v2.1"
API_KEY = "23d97a1ba1724a0fb750faf3d8a24f95"


class DeviceDetails:
    """Represents the state of a device."""

    def __init__(self, data: dict):
        """Initialize the device state."""
        self.data = data
        self._properties = {
            prop.get("name"): prop.get("value") for prop in data.get("properties")
        }

    def value(self, name):
        """Return a property by name."""
        return self.data.get(name)

    def property(self, name):
        """Return a property by name."""
        return self._properties.get(name)


class DeviceState:
    """Represents the state of a device."""

    def __init__(self, data: dict):
        """Initialize the device state."""
        self.data = data

    def value(self, name):
        """Return a property by name."""
        return self.data["values"].get(name)


class ZehnderCloud:
    def __init__(self, session: aiohttp.ClientSession, auth: AbstractAuth):
        self.session = session
        self._auth = auth

    async def activate_scene(self, building_id: str, scene_id: str):
        """Activate a scene."""
        result = await self.make_request(
            "PUT",
            API_ENDPOINT
            + "/scenes/{building_id}/activate/{scene_id}".format(
                building_id=building_id, scene_id=scene_id
            ),
        )

        return result

    async def get_device_details(self, device_id: str) -> DeviceDetails:
        """Get details of a device including notifications, orders, properties and errors."""
        result = await self.make_request(
            "GET",
            API_ENDPOINT
            + "/devices/byid/{device_id}/details".format(device_id=device_id),
        )

        return DeviceDetails(result)

    async def get_scenes(self):
        """Get all supported scenes."""
        result = await self.make_request("GET", API_ENDPOINT + "/scenes")

        return result

    async def get_device_state(self, device_id: int) -> DeviceState:
        """Get the current state of a device as a list of name-value pairs.
        Works for all devices like Radiators, Comfosys or non-zehnder (external) devices."""
        result = await self.make_request(
            "GET",
            API_ENDPOINT + "/devices/{device_id}/state".format(device_id=device_id),
        )

        return DeviceState(result)

    async def get_devices(self):
        """Returns a list of device ids of the current customer."""
        result = await self.make_request("GET", API_ENDPOINT + "/devices/ids")

        return result

    async def get_health(self):
        """Provides an indication about the health of the API."""
        result = await self.make_request("GET", API_ENDPOINT + "/health")

        return result

    async def get_device_history(
        self,
        device_id: str,
        valuename: str,
        time_from: str,
        time_to: str,
        time_interval: int,
    ):
        """Returns the history of a value from a device."""
        # result = self.make_request('GET', API_ENDPOINT + '/devices/{device_id}/history[?valuename][&from][&to][&interval]')
        raise NotImplementedError()

    async def get_weather_data(self, device_id: str):
        """Returns current weather data."""
        result = await self.make_request(
            "GET",
            API_ENDPOINT + "/devices/{device_id}/weather".format(device_id=device_id),
        )

        return result

    async def get_weather_forecast(self, customer_oid: str, language: str):
        """Returns weather forecast for a customer."""
        # result = await self.make_request('GET', API_ENDPOINT + '/customers/{customer_oid}/weather/forecast[?language]')
        raise NotImplementedError()

    async def get_weather_history(
        self,
        device_id: str,
        valuename: str,
        time_from: str,
        time_to: str,
        time_interval: int,
    ):
        """Returns the history of a single weather value."""
        # result = await self.make_request('GET', API_ENDPOINT + '/devices/{device_id}/weather/history[?valuename][&from][&to][&interval]')
        raise NotImplementedError()

    async def set_device_settings(
        self, device_id: str, settings: dict, device_type: str = "comfosys"
    ):
        """Set the settings of a Comfo Air Q device."""
        result = await self.make_request(
            "PUT",
            API_ENDPOINT
            + "/devices/{device_id}/{device_type}/settings".format(
                device_id=device_id,
                device_type=device_type,
            ),
            settings,
        )

        return result

    async def make_request(self, method: str, endpoint: str, body=None):
        """Make a request."""
        if body:
            _LOGGER.debug("Sending %s to %s: %s", method, endpoint, body)
        else:
            _LOGGER.debug("Sending %s to %s", method, endpoint)

        try:
            token = await self._auth.async_get_access_token()
        except client_exceptions.ClientResponseError as ex:
            raise AuthError() from ex

        headers = {
            "Authorization": "Bearer " + token,
            "x-api-key": API_KEY,
        }

        async with self.session.request(
            method, endpoint, headers=headers, json=body
        ) as response:
            _LOGGER.debug("Response status: %s", response.status)
            _LOGGER.debug("Response body: %s", await response.json())

            if response.status == 401:
                message = await response.json()
                raise AuthError(message["message"])

            return await response.json()
