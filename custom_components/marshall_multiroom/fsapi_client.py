"""Minimal async client for Frontier Silicon FSAPI (used by Marshall speakers)."""
from __future__ import annotations

import logging
from xml.etree import ElementTree as ET

import aiohttp

_LOGGER = logging.getLogger(__name__)


class FsApiError(Exception):
    """Raised when the FSAPI device returns a non-OK status or is unreachable."""


class FsApiClient:
    """Thin async wrapper around the FSAPI GET/SET HTTP interface."""

    def __init__(self, host: str, pin: str, session: aiohttp.ClientSession, port: int = 80) -> None:
        self._host = host
        self._port = port
        self._pin = pin
        self._session = session

    def _url(self, operation: str, node: str) -> str:
        return f"http://{self._host}:{self._port}/fsapi/{operation}/{node}"

    @staticmethod
    def _parse_value(value_el: ET.Element):
        """Parse a <value> element's child into a python value."""
        child = list(value_el)[0]
        tag = child.tag
        text = (child.text or "").strip()
        if tag in ("u8", "u16", "u32", "s8", "s16", "s32"):
            return int(text) if text else 0
        if tag == "c8_array":
            return text
        if tag == "array":
            # hex-encoded bytes, e.g. SSID
            try:
                return bytes.fromhex(text).decode("utf-8", errors="replace")
            except ValueError:
                return text
        return text

    async def get(self, node: str):
        """GET a single FSAPI node value."""
        url = self._url("GET", node)
        async with self._session.get(url, params={"pin": self._pin}, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text = await resp.text()
        root = ET.fromstring(text)
        status = root.findtext("status")
        if status != "FS_OK":
            raise FsApiError(f"GET {node} failed: {status}")
        value_el = root.find("value")
        if value_el is None:
            return None
        return self._parse_value(value_el)

    async def set(self, node: str, value) -> None:
        """SET a single FSAPI node value."""
        url = self._url("SET", node)
        params = {"pin": self._pin, "value": str(value)}
        async with self._session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text = await resp.text()
        root = ET.fromstring(text)
        status = root.findtext("status")
        if status != "FS_OK":
            raise FsApiError(f"SET {node}={value} failed: {status}")

    async def list_get_next(self, node: str, key: int = 4294967295, max_items: int = 20) -> list[dict]:
        """LIST_GET_NEXT a node, returning parsed items as list of dicts."""
        url = self._url("LIST_GET_NEXT", f"{node}/{key}")
        params = {"pin": self._pin, "maxItems": str(max_items)}
        async with self._session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text = await resp.text()
        root = ET.fromstring(text)
        status = root.findtext("status")
        if status != "FS_OK":
            raise FsApiError(f"LIST_GET_NEXT {node} failed: {status}")
        items = []
        for item_el in root.findall("item"):
            entry = {"key": item_el.get("key")}
            for field_el in item_el.findall("field"):
                name = field_el.get("name")
                entry[name] = self._parse_value(field_el) if len(field_el) else None
            items.append(entry)
        return items
