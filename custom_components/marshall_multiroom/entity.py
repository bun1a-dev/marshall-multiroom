"""Base entity for Marshall Multi-Room."""
from __future__ import annotations

from homeassistant.const import CONF_HOST
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NODE_FRIENDLY_NAME
from .coordinator import MarshallDataUpdateCoordinator


class MarshallEntity(CoordinatorEntity[MarshallDataUpdateCoordinator]):
    """Base entity tying a Marshall speaker's device info together."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MarshallDataUpdateCoordinator, entry_id: str, host: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._host = host

    @property
    def device_info(self) -> DeviceInfo:
        name = self.coordinator.data.get(NODE_FRIENDLY_NAME) or self._host
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=name,
            manufacturer="Marshall",
            model="Multi-Room (Frontier Silicon)",
            configuration_url=f"http://{self._host}",
        )
