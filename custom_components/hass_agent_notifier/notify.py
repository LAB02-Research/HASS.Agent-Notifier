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
from homeassistant.const import (
    CONF_RESOURCE,
    HTTP_BAD_REQUEST,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_OK,
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
        data = kwargs.get(ATTR_DATA, None)
        image = data.get(ATTR_IMAGE) if data is not None and ATTR_IMAGE in data else None
        duration = data.get(ATTR_DURATION) if data is not None and ATTR_DURATION in data else 0

        payload = ({
            'message': message,
            'title': title,
            'image': image,
            'duration': duration
        })

        response = requests.post(
            self._resource,
            json=payload,
            timeout=10
        )

        if HTTP_INTERNAL_SERVER_ERROR <= response.status_code < 600:
            _LOGGER.exception("Server error. Response %d: %s:", response.status_code, response.reason)
        elif HTTP_BAD_REQUEST <= response.status_code < HTTP_INTERNAL_SERVER_ERROR:
            _LOGGER.exception("Client error. Response %d: %s:", response.status_code, response.reason)
        elif HTTP_OK <= response.status_code < 300:
            _LOGGER.debug("Success. Response %d: %s:", response.status_code, response.reason)
        else:
            _LOGGER.debug("Response %d: %s:", response.status_code, response.reason)
