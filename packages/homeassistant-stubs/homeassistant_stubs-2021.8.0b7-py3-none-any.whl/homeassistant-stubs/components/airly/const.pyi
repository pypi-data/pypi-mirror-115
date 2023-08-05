from .model import AirlySensorEntityDescription as AirlySensorEntityDescription
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT as STATE_CLASS_MEASUREMENT
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER as CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, DEVICE_CLASS_HUMIDITY as DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_PRESSURE as DEVICE_CLASS_PRESSURE, DEVICE_CLASS_TEMPERATURE as DEVICE_CLASS_TEMPERATURE, PERCENTAGE as PERCENTAGE, PRESSURE_HPA as PRESSURE_HPA, TEMP_CELSIUS as TEMP_CELSIUS
from typing import Final

ATTR_API_ADVICE: Final[str]
ATTR_API_CAQI: Final[str]
ATTR_API_CAQI_DESCRIPTION: Final[str]
ATTR_API_CAQI_LEVEL: Final[str]
ATTR_API_HUMIDITY: Final[str]
ATTR_API_PM10: Final[str]
ATTR_API_PM1: Final[str]
ATTR_API_PM25: Final[str]
ATTR_API_PRESSURE: Final[str]
ATTR_API_TEMPERATURE: Final[str]
ATTR_ADVICE: Final[str]
ATTR_DESCRIPTION: Final[str]
ATTR_LEVEL: Final[str]
ATTR_LIMIT: Final[str]
ATTR_PERCENT: Final[str]
SUFFIX_PERCENT: Final[str]
SUFFIX_LIMIT: Final[str]
ATTRIBUTION: Final[str]
CONF_USE_NEAREST: Final[str]
DEFAULT_NAME: Final[str]
DOMAIN: Final[str]
LABEL_ADVICE: Final[str]
MANUFACTURER: Final[str]
MAX_UPDATE_INTERVAL: Final[int]
MIN_UPDATE_INTERVAL: Final[int]
NO_AIRLY_SENSORS: Final[str]
SENSOR_TYPES: tuple[AirlySensorEntityDescription, ...]
