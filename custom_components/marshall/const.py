DOMAIN = "marshall"

CONF_HOST = "host"
CONF_PIN = "pin"

DEFAULT_PIN = "1234"
SCAN_INTERVAL = 10

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
