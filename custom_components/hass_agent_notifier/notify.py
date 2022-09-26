"""
Custom component for Home Assistant to enable sending messages via HASS Agent.


Example configuration.yaml entry:

notify:
  - name: hass notifier
    platform: hass_agent_notifier
    resource: http://192.168.0.1:5115/notify

With this custom component loaded, you can send messaged to a HASS Agent.
"""

import logging
from typing import Any

from functools import partial

import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TITLE_DEFAULT,
    ATTR_TITLE,
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

from homeassistant.components import media_source

from http import HTTPStatus

from homeassistant.const import (
    CONF_RESOURCE,
)
import homeassistant.helpers.config_validation as cv

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_RESOURCE): cv.url})

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config, discovery_info=None):
    """Get the HASS Agent notification service."""
    resource = config.get(CONF_RESOURCE)

    _LOGGER.info("Service created")

    return HassAgentNotificationService(hass, resource)


class HassAgentNotificationService(BaseNotificationService):
    """Implementation of the HASS Agent notification service"""

    def __init__(self, hass, resource):
        """Initialize the service."""
        self._resource = resource
        self._hass = hass

    def send(self, url, data):
        return requests.post(url, json=data, timeout=10)

    async def async_send_message(self, message: str, **kwargs: Any):
        """Send the message to the provided resource."""
        _LOGGER.debug("Preparing notification ..")

        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        data = kwargs.get(ATTR_DATA, None)

        image = data.get("image", None)
        if image is not None:
            if media_source.is_media_source_id(image):
                sourced_media = await media_source.async_resolve_media(self.hass, image)
                sourced_media = media_source.async_process_play_media_url(
                    self.hass, sourced_media.url
                )

                data.update({"image": sourced_media})

        payload = {"message": message, "title": title, "data": data}

        _LOGGER.debug("Sending notification ..")

        try:

            response = await self.hass.async_add_executor_job(
                self.send, self._resource, payload
            )

            _LOGGER.debug("Checking result ..")

            if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                _LOGGER.error(
                    "Server error. Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.BAD_REQUEST:
                _LOGGER.error(
                    "Client error (bad request). Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.NOT_FOUND:
                _LOGGER.debug(
                    "Server error (not found). Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
                _LOGGER.error(
                    "Server error (method not allowed). Response %d",
                    response.status_code,
                )
            elif response.status_code == HTTPStatus.REQUEST_TIMEOUT:
                _LOGGER.debug(
                    "Server error (request timeout). Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.NOT_IMPLEMENTED:
                _LOGGER.error(
                    "Server error (not implemented). Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                _LOGGER.error(
                    "Server error (service unavailable). Response %d",
                    response.status_code,
                )
            elif response.status_code == HTTPStatus.GATEWAY_TIMEOUT:
                _LOGGER.error(
                    "Network error (gateway timeout). Response %d: %s",
                    response.status_code,
                    response.reason,
                )
            elif response.status_code == HTTPStatus.OK:
                _LOGGER.debug(
                    "Success. Response %d: %s", response.status_code, response.reason
                )
            else:
                _LOGGER.debug(
                    "Unknown response %d: %s", response.status_code, response.reason
                )

        except Exception as e:
            _LOGGER.debug("Error sending message: %s", e)
