"""Select entity for the Marshall EQ preset."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, EQ_PRESET_MAP, EQ_PRESET_MAP_REVERSE, NODE_EQ_PRESET
from .entity import MarshallEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the EQ preset select entity."""
    stored = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [MarshallEqPresetSelect(stored["coordinator"], stored["client"], entry.entry_id, entry.data[CONF_HOST])]
    )


class MarshallEqPresetSelect(MarshallEntity, SelectEntity):
    """EQ preset selector (Normal, Flat, Jazz, ... My EQ)."""

    _attr_name = "EQ preset"
    _attr_options = list(EQ_PRESET_MAP.values())
    _attr_icon = "mdi:equalizer"

    def __init__(self, coordinator, client, entry_id: str, host: str) -> None:
        super().__init__(coordinator, entry_id, host)
        self._client = client
        self._attr_unique_id = f"{entry_id}_eq_preset"

    @property
    def current_option(self) -> str | None:
        raw = self.coordinator.data.get(NODE_EQ_PRESET)
        return EQ_PRESET_MAP.get(raw)

    async def async_select_option(self, option: str) -> None:
        raw = EQ_PRESET_MAP_REVERSE[option]
        await self._client.set(NODE_EQ_PRESET, raw)
        await self.coordinator.async_request_refresh()
