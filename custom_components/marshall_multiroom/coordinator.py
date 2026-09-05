"""DataUpdateCoordinator for Marshall Multi-Room speakers."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    NODE_EQ_BASS,
    NODE_EQ_PRESET,
    NODE_EQ_TREBLE,
    NODE_FRIENDLY_NAME,
    NODE_MODE,
    NODE_MUTE,
    NODE_PLAY_ALBUM,
    NODE_PLAY_ARTIST,
    NODE_PLAY_DURATION,
    NODE_PLAY_NAME,
    NODE_PLAY_POSITION,
    NODE_PLAY_STATUS,
    NODE_PLAY_TEXT,
    NODE_POWER,
    NODE_VOLUME,
    SCAN_INTERVAL_SECONDS,
)
from .fsapi_client import FsApiClient, FsApiError

_LOGGER = logging.getLogger(__name__)

# Nodes polled on every refresh cycle
POLLED_NODES = [
    NODE_POWER,
    NODE_VOLUME,
    NODE_MUTE,
    NODE_MODE,
    NODE_EQ_PRESET,
    NODE_EQ_BASS,
    NODE_EQ_TREBLE,
    NODE_FRIENDLY_NAME,
    NODE_PLAY_STATUS,
    NODE_PLAY_NAME,
    NODE_PLAY_TEXT,
    NODE_PLAY_ARTIST,
    NODE_PLAY_ALBUM,
    NODE_PLAY_POSITION,
    NODE_PLAY_DURATION,
]


class MarshallDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Polls the speaker's FSAPI nodes and exposes them as a single dict."""

    def __init__(self, hass: HomeAssistant, client: FsApiClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Marshall Multi-Room",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.client = client
        self.data_updated_at: datetime | None = None

    async def _async_update_data(self) -> dict:
        data: dict = {}
        for node in POLLED_NODES:
            try:
                data[node] = await self.client.get(node)
            except FsApiError as err:
                # Some nodes (e.g. play.info.* when nothing is playing) may
                # legitimately fail; don't kill the whole refresh for that.
                _LOGGER.debug("Node %s unavailable: %s", node, err)
                data[node] = None
            except Exception as err:  # noqa: BLE001 - network errors etc.
                raise UpdateFailed(f"Error communicating with speaker: {err}") from err
        self.data_updated_at = dt_util.utcnow()
        return data
