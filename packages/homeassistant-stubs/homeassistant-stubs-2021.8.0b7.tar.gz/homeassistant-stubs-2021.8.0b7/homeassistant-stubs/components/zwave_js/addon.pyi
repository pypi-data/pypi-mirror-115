import asyncio
from .const import ADDON_SLUG as ADDON_SLUG, CONF_ADDON_DEVICE as CONF_ADDON_DEVICE, CONF_ADDON_NETWORK_KEY as CONF_ADDON_NETWORK_KEY, DOMAIN as DOMAIN, LOGGER as LOGGER
from enum import Enum
from homeassistant.components.hassio import async_create_snapshot as async_create_snapshot, async_get_addon_discovery_info as async_get_addon_discovery_info, async_get_addon_info as async_get_addon_info, async_install_addon as async_install_addon, async_restart_addon as async_restart_addon, async_set_addon_options as async_set_addon_options, async_start_addon as async_start_addon, async_stop_addon as async_stop_addon, async_uninstall_addon as async_uninstall_addon, async_update_addon as async_update_addon
from homeassistant.components.hassio.handler import HassioAPIError as HassioAPIError
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.singleton import singleton as singleton
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])
DATA_ADDON_MANAGER: Any

def get_addon_manager(hass: HomeAssistant) -> AddonManager: ...
def api_error(error_message: str) -> Callable[[F], F]: ...

class AddonInfo:
    options: dict[str, Any]
    state: AddonState
    update_available: bool
    version: Union[str, None]

class AddonState(Enum):
    NOT_INSTALLED: str
    INSTALLING: str
    UPDATING: str
    NOT_RUNNING: str
    RUNNING: str

class AddonManager:
    _hass: Any
    _install_task: Any
    _restart_task: Any
    _start_task: Any
    _update_task: Any
    def __init__(self, hass: HomeAssistant) -> None: ...
    def task_in_progress(self) -> bool: ...
    async def async_get_addon_discovery_info(self) -> dict: ...
    async def async_get_addon_info(self) -> AddonInfo: ...
    def async_get_addon_state(self, addon_info: dict[str, Any]) -> AddonState: ...
    async def async_set_addon_options(self, config: dict) -> None: ...
    async def async_install_addon(self) -> None: ...
    def async_schedule_install_addon(self, catch_error: bool = ...) -> asyncio.Task: ...
    def async_schedule_install_setup_addon(self, usb_path: str, network_key: str, catch_error: bool = ...) -> asyncio.Task: ...
    async def async_uninstall_addon(self) -> None: ...
    async def async_update_addon(self) -> None: ...
    def async_schedule_update_addon(self, catch_error: bool = ...) -> asyncio.Task: ...
    async def async_start_addon(self) -> None: ...
    async def async_restart_addon(self) -> None: ...
    def async_schedule_start_addon(self, catch_error: bool = ...) -> asyncio.Task: ...
    def async_schedule_restart_addon(self, catch_error: bool = ...) -> asyncio.Task: ...
    async def async_stop_addon(self) -> None: ...
    async def async_configure_addon(self, usb_path: str, network_key: str) -> None: ...
    def async_schedule_setup_addon(self, usb_path: str, network_key: str, catch_error: bool = ...) -> asyncio.Task: ...
    async def async_create_snapshot(self) -> None: ...
    def _async_schedule_addon_operation(self, *funcs: Callable, catch_error: bool = ...) -> asyncio.Task: ...

class AddonError(HomeAssistantError): ...
