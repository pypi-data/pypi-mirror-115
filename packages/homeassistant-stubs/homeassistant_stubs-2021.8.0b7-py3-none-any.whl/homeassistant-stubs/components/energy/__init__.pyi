from . import websocket_api as websocket_api
from .const import DOMAIN as DOMAIN
from homeassistant.components import frontend as frontend
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers import discovery as discovery
from homeassistant.helpers.typing import ConfigType as ConfigType

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool: ...
