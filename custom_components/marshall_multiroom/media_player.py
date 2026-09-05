"""Media player entity for Marshall Multi-Room speakers."""
from __future__ import annotations

import logging

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    NODE_MODE,
    NODE_MUTE,
    NODE_PLAY_ALBUM,
    NODE_PLAY_ARTIST,
    NODE_PLAY_CONTROL,
    NODE_PLAY_DURATION,
    NODE_PLAY_NAME,
    NODE_PLAY_POSITION,
    NODE_PLAY_STATUS,
    NODE_PLAY_TEXT,
    NODE_POWER,
    NODE_VOLUME,
    PLAY_CONTROL_NEXT,
    PLAY_CONTROL_PAUSE,
    PLAY_CONTROL_PLAY,
    PLAY_CONTROL_PREVIOUS,
    SOURCE_MAP,
    SOURCE_MAP_REVERSE,
    VOLUME_MAX,
)
from .entity import MarshallEntity

_LOGGER = logging.getLogger(__name__)

# FSAPI netRemote.play.status values (typical Frontier Silicon mapping)
PLAY_STATUS_PLAYING = 2
PLAY_STATUS_PAUSED = 3


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the media_player entity."""
    stored = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [MarshallMediaPlayer(stored["coordinator"], stored["client"], entry.entry_id, entry.data[CONF_HOST])]
    )


class MarshallMediaPlayer(MarshallEntity, MediaPlayerEntity):
    """Represents a Marshall Multi-Room speaker as a media_player."""

    _attr_name = None  # use device name
    _attr_source_list = list(SOURCE_MAP.values())
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
    )

    def __init__(self, coordinator, client, entry_id: str, host: str) -> None:
        super().__init__(coordinator, entry_id, host)
        self._client = client
        self._attr_unique_id = f"{entry_id}_media_player"

    @property
    def state(self) -> MediaPlayerState:
        if not self.coordinator.data.get(NODE_POWER):
            return MediaPlayerState.OFF
        status = self.coordinator.data.get(NODE_PLAY_STATUS)
        if status == PLAY_STATUS_PLAYING:
            return MediaPlayerState.PLAYING
        if status == PLAY_STATUS_PAUSED:
            return MediaPlayerState.PAUSED
        return MediaPlayerState.IDLE

    @property
    def volume_level(self) -> float | None:
        raw = self.coordinator.data.get(NODE_VOLUME)
        if raw is None:
            return None
        return raw / VOLUME_MAX

    @property
    def is_volume_muted(self) -> bool | None:
        return bool(self.coordinator.data.get(NODE_MUTE))

    @property
    def source(self) -> str | None:
        raw = self.coordinator.data.get(NODE_MODE)
        return SOURCE_MAP.get(raw)

    @property
    def media_title(self) -> str | None:
        return self.coordinator.data.get(NODE_PLAY_NAME) or self.coordinator.data.get(NODE_PLAY_TEXT)

    @property
    def media_artist(self) -> str | None:
        return self.coordinator.data.get(NODE_PLAY_ARTIST)

    @property
    def media_album_name(self) -> str | None:
        return self.coordinator.data.get(NODE_PLAY_ALBUM)

    @property
    def media_duration(self) -> int | None:
        """Duration in seconds (FSAPI reports milliseconds)."""
        raw = self.coordinator.data.get(NODE_PLAY_DURATION)
        return round(raw / 1000) if raw is not None else None

    @property
    def media_position(self) -> int | None:
        """Position in seconds (FSAPI reports milliseconds)."""
        raw = self.coordinator.data.get(NODE_PLAY_POSITION)
        return round(raw / 1000) if raw is not None else None

    async def async_turn_on(self) -> None:
        await self._client.set(NODE_POWER, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        await self._client.set(NODE_POWER, 0)
        await self.coordinator.async_request_refresh()

    async def async_set_volume_level(self, volume: float) -> None:
        raw = round(volume * VOLUME_MAX)
        await self._client.set(NODE_VOLUME, raw)
        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        await self._client.set(NODE_MUTE, 1 if mute else 0)
        await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str) -> None:
        try:
            raw = SOURCE_MAP_REVERSE[source]
        except KeyError:
            _LOGGER.warning("Unknown source requested: %s", source)
            return
        await self._client.set(NODE_MODE, raw)
        await self.coordinator.async_request_refresh()

    async def async_media_play(self) -> None:
        await self._client.set(NODE_PLAY_CONTROL, PLAY_CONTROL_PLAY)
        await self.coordinator.async_request_refresh()

    async def async_media_pause(self) -> None:
        await self._client.set(NODE_PLAY_CONTROL, PLAY_CONTROL_PAUSE)
        await self.coordinator.async_request_refresh()

    async def async_media_next_track(self) -> None:
        await self._client.set(NODE_PLAY_CONTROL, PLAY_CONTROL_NEXT)
        await self.coordinator.async_request_refresh()

    async def async_media_previous_track(self) -> None:
        await self._client.set(NODE_PLAY_CONTROL, PLAY_CONTROL_PREVIOUS)
        await self.coordinator.async_request_refresh()
