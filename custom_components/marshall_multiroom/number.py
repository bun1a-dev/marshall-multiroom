"""Number entities for Marshall EQ bass/treble."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    EQ_BASS_MAX,
    EQ_BASS_MIN,
    EQ_TREBLE_MAX,
    EQ_TREBLE_MIN,
    NODE_EQ_BASS,
    NODE_EQ_TREBLE,
)
from .entity import MarshallEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up bass/treble number entities."""
    stored = hass.data[DOMAIN][entry.entry_id]
    coordinator = stored["coordinator"]
    client = stored["client"]
    entry_id = entry.entry_id
    host = entry.data[CONF_HOST]

    async_add_entities(
        [
            MarshallEqNumber(
                coordinator, client, entry_id, host,
                name="Bass", node=NODE_EQ_BASS, min_value=EQ_BASS_MIN, max_value=EQ_BASS_MAX,
                icon="mdi:music-clef-bass",
            ),
            MarshallEqNumber(
                coordinator, client, entry_id, host,
                name="Treble", node=NODE_EQ_TREBLE, min_value=EQ_TREBLE_MIN, max_value=EQ_TREBLE_MAX,
                icon="mdi:music-note",
            ),
        ]
    )


class MarshallEqNumber(MarshallEntity, NumberEntity):
    """Generic bass/treble slider backed by an FSAPI s16 node."""

    _attr_native_step = 1

    def __init__(self, coordinator, client, entry_id: str, host: str, *, name: str, node: str,
                 min_value: int, max_value: int, icon: str) -> None:
        super().__init__(coordinator, entry_id, host)
        self._client = client
        self._node = node
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_unique_id = f"{entry_id}_{node.replace('.', '_')}"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get(self._node)

    async def async_set_native_value(self, value: float) -> None:
        await self._client.set(self._node, int(value))
        await self.coordinator.async_request_refresh()
