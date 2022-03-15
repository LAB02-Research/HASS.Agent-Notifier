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

import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE,
    ATTR_TITLE,
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

from http import HTTPStatus

from homeassistant.const import (
    CONF_RESOURCE,
)
import homeassistant.helpers.config_validation as cv

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_RESOURCE): cv.url
    }
)

_LOGGER = logging.getLogger(__name__)

ATTR_IMAGE = 'image'
ATTR_DURATION = 'duration'


def get_service(hass, config, discovery_info=None):
    """Get the HASS Agent notification service."""
    resource = config.get(CONF_RESOURCE)

    _LOGGER.info("Service created")

    return HassAgentNotificationService(
        hass,
        resource
    )


class HassAgentNotificationService(BaseNotificationService):
    """Implementation of the HASS Agent notification service"""

    def __init__(
            self,
            hass,
            resource
    ):
        """Initialize the service."""
        self._resource = resource
        self._hass = hass

    def send_message(self, message="", title="", **kwargs):
        """Send the message to the provided resource."""
        _LOGGER.debug("Preparing notification ..")

        data = kwargs.get(ATTR_DATA, None)
        image = data.get(ATTR_IMAGE) if data is not None and ATTR_IMAGE in data else None
        duration = data.get(ATTR_DURATION) if data is not None and ATTR_DURATION in data else 0

        payload = ({
            'message': message,
            'title': title,
            'image': image,
            'duration': duration
        })

        _LOGGER.debug("Sending notification ..")

        try:

            response = requests.post(
                self._resource,
                json=payload,
                timeout=10
            )

            _LOGGER.debug("Checking result ..")

            if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                _LOGGER.error("Server error. Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.BAD_REQUEST:
                _LOGGER.error("Client error (bad request). Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                _LOGGER.debug("Server error (not found). Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
                _LOGGER.error("Server error (method not allowed). Response %d", response.status_code)
            elif response.status_code == HTTPStatus.REQUEST_TIMEOUT:
                _LOGGER.debug("Server error (request timeout). Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.NOT_IMPLEMENTED:
                _LOGGER.error("Server error (not implemented). Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                _LOGGER.error("Server error (service unavailable). Response %d", response.status_code)
            elif response.status_code == HTTPStatus.GATEWAY_TIMEOUT:
                _LOGGER.error("Network error (gateway timeout). Response %d: %s", response.status_code, response.reason)
            elif response.status_code == HTTPStatus.OK:
                _LOGGER.debug("Success. Response %d: %s", response.status_code, response.reason)
            else:
                _LOGGER.debug("Unknown response %d: %s", response.status_code, response.reason)

        except Exception as e:
            _LOGGER.debug("Error sending message: %s", e)

