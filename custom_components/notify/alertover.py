"""
Alertover platform for notify component.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/notify.clertover/
"""
import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_NAME, CONF_API_KEY, CONF_RECIPIENT)
from homeassistant.components.notify import (
    PLATFORM_SCHEMA, BaseNotificationService, ATTR_TITLE, ATTR_TITLE_DEFAULT)

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'alertover'

BASE_API_URL = 'https://api.alertover.com/v1/alert'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_RECIPIENT): cv.string,
})


def get_service(hass, config, discovery_info=None):
    """Get the Alertover notification service."""
    return AlertoverNotificationService(config)


class AlertoverNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Alertover service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config.get(CONF_API_KEY)
        self.recipient = config.get(CONF_RECIPIENT)

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""
        data = {
            'source': self.api_key,
            'receiver': self.recipient,
            'content': message,
            ATTR_TITLE: kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT),
        }
        
        try:
            resp = requests.post(BASE_API_URL, data=data, timeout=5)

        except requests.exceptions.Timeout:
            return

        if resp.status_code == 200:
            response = resp.json()
            if response['code'] != 0:
                _LOGGER.error("Error %s : %s", response['code'], response['msg'])
    

