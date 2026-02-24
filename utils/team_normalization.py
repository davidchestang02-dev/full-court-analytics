# utils/team_normalization.py

NORMALIZATION_MAP = {
    "N.C. State": "NC State",
    "N.C. St.": "NC State",
    "North Carolina State": "NC State",
    "UNC": "North Carolina",
    "N. Carolina": "North Carolina",
    "UConn": "Connecticut",
    "Saint Mary's (CA)": "Saint Marys",
    "St. Mary's (CA)": "Saint Marys",
    # Add more as you encounter them
}

def normalize_team_name(name: str) -> str:
    """
    Normalize team names across different data sources so merges are stable.
    """
    if not isinstance(name, str):
        return ""

    name = name.strip()

    if name in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[name]

    # Light generic cleanup
    name = name.replace("St.", "State")
    name = name.replace("&amp;", "&")

    return name
