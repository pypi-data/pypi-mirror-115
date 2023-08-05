from aiohttp import web
from collections.abc import Iterable
from datetime import datetime as dt
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.http import HomeAssistantView as HomeAssistantView
from homeassistant.components.recorder import history as history, models as history_models
from homeassistant.components.recorder.statistics import list_statistic_ids as list_statistic_ids, statistics_during_period as statistics_during_period
from homeassistant.components.recorder.util import session_scope as session_scope
from homeassistant.const import CONF_DOMAINS as CONF_DOMAINS, CONF_ENTITIES as CONF_ENTITIES, CONF_EXCLUDE as CONF_EXCLUDE, CONF_INCLUDE as CONF_INCLUDE, HTTP_BAD_REQUEST as HTTP_BAD_REQUEST
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.deprecation import deprecated_class as deprecated_class, deprecated_function as deprecated_function
from homeassistant.helpers.entityfilter import CONF_ENTITY_GLOBS as CONF_ENTITY_GLOBS, INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA as INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA
from typing import Any

_LOGGER: Any
DOMAIN: str
CONF_ORDER: str
GLOB_TO_SQL_CHARS: Any
CONFIG_SCHEMA: Any

def get_significant_states(hass, *args, **kwargs): ...
def state_changes_during_period(hass, start_time, end_time: Any | None = ..., entity_id: Any | None = ...): ...
def get_last_state_changes(hass, number_of_states, entity_id): ...
def get_states(hass, utc_point_in_time, entity_ids: Any | None = ..., run: Any | None = ..., filters: Any | None = ...): ...
def get_state(hass, utc_point_in_time, entity_id, run: Any | None = ...): ...
async def async_setup(hass, config): ...

class LazyState(history_models.LazyState): ...

async def ws_get_statistics_during_period(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None: ...
async def ws_get_list_statistic_ids(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None: ...

class HistoryPeriodView(HomeAssistantView):
    url: str
    name: str
    extra_urls: Any
    filters: Any
    use_include_order: Any
    def __init__(self, filters, use_include_order) -> None: ...
    async def get(self, request: web.Request, datetime: Union[str, None] = ...) -> web.Response: ...
    def _sorted_significant_states_json(self, hass, start_time, end_time, entity_ids, include_start_time_state, significant_changes_only, minimal_response): ...

def sqlalchemy_filter_from_include_exclude_conf(conf): ...

class Filters:
    excluded_entities: Any
    excluded_domains: Any
    excluded_entity_globs: Any
    included_entities: Any
    included_domains: Any
    included_entity_globs: Any
    def __init__(self) -> None: ...
    def apply(self, query): ...
    @property
    def has_config(self): ...
    def bake(self, baked_query): ...
    def entity_filter(self): ...

def _glob_to_like(glob_str): ...
def _entities_may_have_state_changes_after(hass: HomeAssistant, entity_ids: Iterable, start_time: dt) -> bool: ...
