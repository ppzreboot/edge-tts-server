import re
from typing import Any

# 格式与 edge-tts TTSConfig 一致；范围为微软在线服务常用区间，超出可能合成失败。
PROSODY_LIMITS: dict[str, dict[str, Any]] = {
    "rate": {
        "format": r"^[+-]\d+%$",
        "example": "+10%",
        "range": "[-50%, +100%]",
        "min": -50,
        "max": 100,
    },
    "volume": {
        "format": r"^[+-]\d+%$",
        "example": "-20%",
        "range": "[-50%, +50%]",
        "min": -50,
        "max": 50,
    },
    "pitch": {
        "format": r"^[+-]\d+Hz$",
        "example": "+5Hz",
        "range": "[-50Hz, +50Hz]",
        "min": -50,
        "max": 50,
    },
}

_PERCENT_RE = re.compile(r"^([+-])(\d+)%$")
_PITCH_RE = re.compile(r"^([+-])(\d+)Hz$")


def field_description(name: str) -> str:
    spec = PROSODY_LIMITS[name]
    return f"格式 {spec['format']}，常用范围 {spec['range']}，例 {spec['example']}"


def prosody_summary() -> dict[str, dict[str, str]]:
    return {
        name: {
            "format": spec["format"],
            "range": spec["range"],
            "example": spec["example"],
        }
        for name, spec in PROSODY_LIMITS.items()
    }


def _parse_signed_percent(value: str) -> int:
    match = _PERCENT_RE.match(value)
    if not match:
        raise ValueError(f"invalid percent value: {value}")
    sign = -1 if match.group(1) == "-" else 1
    return sign * int(match.group(2))


def _parse_signed_hz(value: str) -> int:
    match = _PITCH_RE.match(value)
    if not match:
        raise ValueError(f"invalid pitch value: {value}")
    sign = -1 if match.group(1) == "-" else 1
    return sign * int(match.group(2))


def validate(name: str, value: str) -> str:
    spec = PROSODY_LIMITS[name]
    if re.match(spec["format"], value) is None:
        raise ValueError(
            f"{name} must match {spec['format']} (e.g. {spec['example']})"
        )
    amount = _parse_signed_hz(value) if name == "pitch" else _parse_signed_percent(value)
    if amount < spec["min"] or amount > spec["max"]:
        raise ValueError(f"{name} must be within {spec['range']} (got {value})")
    return value
