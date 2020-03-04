import re
from itertools import chain

from .config import DIRECTIONAL, STREET_TYPE, STATE_CODE, DIRECTION_CODE

SEP = r"(?:\W+|$)"

ADDR_MATCH = {
    "type": "|".join(sorted(set(chain(STREET_TYPE.keys(), STREET_TYPE.values())))),
    "fraction": r"\d+\/\d+",
    "state": r"\b(?:{})\b".format(
        "|".join([re.escape(x) for x in chain(STATE_CODE.keys(), STATE_CODE.values())])
    ),
    "direct": "|".join(
        list(DIRECTIONAL.keys())
        + list(
            chain.from_iterable(
                [
                    (re.escape(".".join(x) + "."), x)
                    for x in reversed(
                        sorted(DIRECTIONAL.values(), key=lambda x: len(x))
                    )
                ]
            )
        )
    ),
    "dircode": "|".join(DIRECTION_CODE.keys()),
    "zip": r"(?P<zip>\d{5})[- ]?(?P<plus4>\d{4})?",
    "corner": r"(?:\band\b|\bat\b|&|\@)",
    "number": r"(?P<number>(\d+-?\d*)|([N|S|E|W]\d{1,3}[N|S|E|W]\d{1,6}))(?=\D)",
    "po_box": r"p\W*(?:[om]|ost\ ?office)\W*b(?:ox)?",
    "sec_unit_type_unnumbered": r"""
(?P<sec_unit_type_2>ba?se?me?n?t
    |fro?nt
    |lo?bby
    |lowe?r
    |off?i?ce?
    |pe?n?t?ho?u?s?e?
    |rear
    |side
    |uppe?r
)\b
""",
}

ADDR_MATCH[
    "street"
] = r"""
(?:
    (?:(?P<street_0>{direct})\W+
        (?P<type_0>{type})\b
    )
    |
    (?:(?P<prefix_0>{direct})\W+)?
    (?:
        (?P<street_1>[^,]*\d)
        (?:[^\w,]*(?P<suffix_1>{direct})\b)
        |
        (?P<street_2>[^,]+)
        (?:[^\w,]+(?P<type_2>{type})\b)
        (?:[^\w,]+(?P<suffix_2>{direct})\b)?
        |
        (?P<street_3>[^,]+?)
        (?:[^\w,]+(?P<type_3>{type})\b)?
        (?:[^\w,]+(?P<suffix_3>{direct})\b)?
    )
)
""".format(
    **ADDR_MATCH
)

ADDR_MATCH[
    "sec_unit_type_numbered"
] = r"""
(?P<sec_unit_type_1>su?i?te
    |{po_box}
    |(?:ap|dep)(?:ar)?t(?:me?nt)?
    |ro*m
    |flo*r?
    |uni?t
    |bu?i?ldi?n?g
    |ha?nga?r
    |lo?t
    |pier
    |slip
    |spa?ce?
    |stop
    |tra?i?le?r
    |box)(?![a-z]
)
""".format(
    **ADDR_MATCH
)

ADDR_MATCH[
    "sec_unit"
] = r"""
(?:
    (?:
        (?:
            (?:{sec_unit_type_numbered}\W*)
            |(?P<sec_unit_type_3>\#)\W*
        )
        (?P<sec_unit_num_1>[\w-]+)
    )
    |
    {sec_unit_type_unnumbered}
)
""".format(
    **ADDR_MATCH
)

ADDR_MATCH[
    "city_and_state"
] = r"""
(?:
    (?P<city>[^\d,]+?)\W+
    (?P<state>{state})
)
""".format(
    **ADDR_MATCH
)

ADDR_MATCH[
    "place"
] = r"""
(?:{city_and_state}\W*)?
(?:{zip})?
""".format(
    **ADDR_MATCH
)

ADDR_MATCH["address"] = re.compile(
    r"""
^
[^\w#]*
({number})\W*
(?:{fraction}\W*)?
    {street}\W+
(?:{sec_unit})?\W*
    {place}
\W*$
""".format(
        **ADDR_MATCH
    ),
    re.I | re.X,
)

ADDR_MATCH["informal_address"] = re.compile(
    r"""
^
\s*
(?:{sec_unit_plus_sep})?
(?:{number})?\W*
(?:{fraction}\W*)?
    {street_plus_sep}
(?:{sec_unit_replaced})?
(?:{place})?
""".format(
        sec_unit_plus_sep=ADDR_MATCH["sec_unit"] + SEP,
        street_plus_sep=ADDR_MATCH["street"] + SEP,
        sec_unit_replaced=re.sub(r"_\d", r"\g<0>1", ADDR_MATCH["sec_unit"]) + SEP,
        **ADDR_MATCH
    ),
    re.I | re.X,
)

ADDR_MATCH["po_address"] = re.compile(
    r"""
^
\s*
(?:{sec_unit_replaced})?
(?:{place})?
""".format(
        sec_unit_replaced=re.sub(r"_\d", r"\g<0>1", ADDR_MATCH["sec_unit"]) + SEP,
        **ADDR_MATCH
    ),
    re.I | re.X,
)

ADDR_MATCH["intersection"] = re.compile(
    r"""
^\W*
{street_replaced_1}\W*?
\s+{corner}\s+
{street_replaced_2}($|\W+)
{place}\W*$
""".format(
        street_replaced_1=re.sub(r"_\d", r"1\g<0>", ADDR_MATCH["street"]),
        street_replaced_2=re.sub(r"_\d", r"2\g<0>", ADDR_MATCH["street"]),
        **ADDR_MATCH
    ),
    re.I | re.X,
)
