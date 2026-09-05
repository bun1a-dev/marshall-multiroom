"""Constants for the Marshall Multi-Room integration."""

DOMAIN = "marshall_multiroom"

CONF_PIN = "pin"
DEFAULT_PIN = "1234"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 10

VOLUME_MAX = 32

SOURCE_MAP = {
    0: "AUX",
    1: "AirPlay",
    4: "Chromecast",
    5: "Bluetooth",
    6: "Internet Radio",
    7: "RCA",
    8: "Spotify",
    9: "Inactive",
}
SOURCE_MAP_REVERSE = {v: k for k, v in SOURCE_MAP.items()}

EQ_PRESET_MAP = {
    0: "My EQ",
    1: "Normal",
    2: "Flat",
    3: "Jazz",
    4: "Rock",
    5: "Movie",
    6: "Classic",
    7: "Pop",
    8: "News",
}
EQ_PRESET_MAP_REVERSE = {v: k for k, v in EQ_PRESET_MAP.items()}
EQ_CUSTOM_PRESET_KEY = 0  # "My EQ"

EQ_BASS_MIN = 0
EQ_BASS_MAX = 10
EQ_TREBLE_MIN = 0
EQ_TREBLE_MAX = 10

# FSAPI node names
NODE_POWER = "netRemote.sys.power"
NODE_VOLUME = "netRemote.sys.audio.volume"
NODE_MUTE = "netRemote.sys.audio.mute"
NODE_MODE = "netRemote.sys.mode"
NODE_EQ_PRESET = "netRemote.sys.audio.eqPreset"
NODE_EQ_BASS = "netRemote.sys.audio.eqCustom.param0"
NODE_EQ_TREBLE = "netRemote.sys.audio.eqCustom.param1"
NODE_FRIENDLY_NAME = "netRemote.sys.info.friendlyName"
NODE_VERSION = "netRemote.sys.info.version"
NODE_PLAY_STATUS = "netRemote.play.status"
NODE_PLAY_CONTROL = "netRemote.play.control"
NODE_PLAY_NAME = "netRemote.play.info.name"
NODE_PLAY_TEXT = "netRemote.play.info.text"
NODE_PLAY_ARTIST = "netRemote.play.info.artist"
NODE_PLAY_ALBUM = "netRemote.play.info.album"

NODE_PLAY_POSITION = "netRemote.play.position"
NODE_PLAY_DURATION = "netRemote.play.info.duration"
NODE_PLAY_CONTROL = "netRemote.play.control"

PLAY_CONTROL_PLAY = 1
PLAY_CONTROL_PAUSE = 2
PLAY_CONTROL_NEXT = 3
PLAY_CONTROL_PREVIOUS = 4
