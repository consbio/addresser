import re

from .config import NORMALIZE_MAP, DIRECTION_CODE
from .patterns import ADDR_MATCH
from .utils import is_number


def _normalize_address(parts=None):
    if parts is None:
        return

    parsed = {}

    valid_keys = (
        x for x in parts.keys() if not (x in ("input", "index") or is_number(x))
    )

    for key in valid_keys:
        new_key = (
            "_".join(key.split("_")[:-1]) if is_number(key.split("_").pop()) else key
        )
        if parts.get(key) is not None:
            parsed[new_key] = re.sub(r"^\s+|\s+$|[^\w\s\-#&]", "", parts[key].strip())

    for key, map_ in NORMALIZE_MAP.items():
        try:
            parsed[key] = map_[parsed[key].lower()]
        except KeyError:
            continue

    for key in ("type", "type1", "type2"):
        try:
            parsed[key] = parsed[key].capitalize()
        except KeyError:
            continue

    if parsed.get("city") is not None:
        parsed["city"] = re.sub(
            r"^(?P<dircode>{dircode})\s+(?=\S)".format(**ADDR_MATCH),
            lambda x: DIRECTION_CODE[x["dircode"].upper()].capitalize() + " ",
            parsed["city"],
            flags=re.I | re.X,
        )

    return parsed


def _parse_po_address(address):
    match = ADDR_MATCH["po_address"].search(address)
    return match and _normalize_address(match.groupdict())


def parse_address(address):
    match = ADDR_MATCH["address"].search(address)
    return match and _normalize_address(match.groupdict())


def parse_informal_address(address):
    match = ADDR_MATCH["informal_address"].search(address)
    return match and _normalize_address(match.groupdict())


def parse_intersection(address):
    match = ADDR_MATCH["intersection"].search(address)
    parts = match and _normalize_address(match.groupdict())

    if parts:
        parts["type2"] = parts.get("type2") or ""
        parts["type1"] = parts.get("type1") or ""
        if parts["type2"] and not parts["type1"] or (parts["type1"] == parts["type2"]):
            type_ = re.sub(r"s\W*$", "", parts["type2"])
            if re.search(r"^{}$".format(ADDR_MATCH["type"]), type_, re.X | re.I):
                parts["type1"] = parts["type2"] = type_

    return parts


def parse_location(address):
    if re.search(ADDR_MATCH["corner"], address, re.X | re.I):
        return parse_intersection(address)

    if re.search(r"^" + ADDR_MATCH["po_box"], address, re.X | re.I):
        return _parse_po_address(address)

    return parse_address(address) or parse_informal_address(address)
