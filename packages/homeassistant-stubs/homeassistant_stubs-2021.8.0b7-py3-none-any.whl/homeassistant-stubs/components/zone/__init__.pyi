from .const import ATTR_PASSIVE as ATTR_PASSIVE, ATTR_RADIUS as ATTR_RADIUS, CONF_PASSIVE as CONF_PASSIVE, DOMAIN as DOMAIN, HOME_ZONE as HOME_ZONE
from homeassistant import config_entries as config_entries
from homeassistant.const import ATTR_EDITABLE as ATTR_EDITABLE, ATTR_LATITUDE as ATTR_LATITUDE, ATTR_LONGITUDE as ATTR_LONGITUDE, CONF_ICON as CONF_ICON, CONF_ID as CONF_ID, CONF_LATITUDE as CONF_LATITUDE, CONF_LONGITUDE as CONF_LONGITUDE, CONF_NAME as CONF_NAME, CONF_RADIUS as CONF_RADIUS, EVENT_CORE_CONFIG_UPDATE as EVENT_CORE_CONFIG_UPDATE, SERVICE_RELOAD as SERVICE_RELOAD, STATE_UNAVAILABLE as STATE_UNAVAILABLE
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, ServiceCall as ServiceCall, State as State, callback as callback
from homeassistant.helpers import collection as collection, entity as entity, entity_component as entity_component, service as service, storage as storage
from homeassistant.loader import bind_hass as bind_hass
from homeassistant.util.location import distance as distance
from typing import Any

_LOGGER: Any
DEFAULT_PASSIVE: bool
DEFAULT_RADIUS: int
ENTITY_ID_FORMAT: str
ENTITY_ID_HOME: Any
ICON_HOME: str
ICON_IMPORT: str
CREATE_FIELDS: Any
UPDATE_FIELDS: Any

def empty_value(value: Any) -> Any: ...

CONFIG_SCHEMA: Any
RELOAD_SERVICE_SCHEMA: Any
STORAGE_KEY = DOMAIN
STORAGE_VERSION: int

def async_active_zone(hass: HomeAssistant, latitude: float, longitude: float, radius: int = ...) -> Union[State, None]: ...
def in_zone(zone: State, latitude: float, longitude: float, radius: float = ...) -> bool: ...

class ZoneStorageCollection(collection.StorageCollection):
    CREATE_SCHEMA: Any
    UPDATE_SCHEMA: Any
    async def _process_create_data(self, data: dict) -> dict: ...
    def _get_suggested_id(self, info: dict) -> str: ...
    async def _update_data(self, data: dict, update_data: dict) -> dict: ...

async def async_setup(hass: HomeAssistant, config: dict) -> bool: ...
def _home_conf(hass: HomeAssistant) -> dict: ...
async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool: ...
async def async_unload_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool: ...

class Zone(entity.Entity):
    _config: Any
    editable: bool
    _attrs: Any
    def __init__(self, config: dict) -> None: ...
    @classmethod
    def from_yaml(cls, config: dict) -> Zone: ...
    @property
    def state(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def unique_id(self) -> Union[str, None]: ...
    @property
    def icon(self) -> Union[str, None]: ...
    @property
    def extra_state_attributes(self) -> Union[dict, None]: ...
    @property
    def should_poll(self) -> bool: ...
    async def async_update_config(self, config: dict) -> None: ...
    def _generate_attrs(self) -> None: ...
