"""Find the paid apps a person owns, so they know what to re-download on Linux.

Only names, versions and publishers are read (from the installed-apps list). PenguinPort
never reads product keys, serial numbers, licence files or account details.
"""
from __future__ import annotations

import re

# Well-known paid Windows software. Matched against the installed app's name.
PAID_APPS = [
    r"^microsoft (office|365)", r"^microsoft (word|excel|powerpoint|outlook|visio|project)\b",
    r"^adobe (photoshop|illustrator|premiere|after effects|indesign|lightroom|acrobat(?! reader))",
    r"^adobe creative cloud", r"^coreldraw", r"^corel (paintshop|videostudio)",
    r"^affinity (photo|designer|publisher)", r"^autodesk", r"^autocad", r"^sketchup",
    r"^ableton live", r"^fl studio", r"^cubase", r"^bitwig", r"^reaper",
    r"^camtasia", r"^snagit", r"^winrar", r"^nero", r"^vmware workstation",
    r"^parallels", r"^jetbrains|^(pycharm|intellij idea|webstorm|rider)\b",
    r"^sublime text", r"^beyond compare", r"^total commander", r"^directory opus",
    r"^quicken", r"^turbotax", r"^cyberlink", r"^capture one", r"^dxo",
    r"^topaz", r"^luminar", r"^clip studio paint", r"^rebelle", r"^1password",
    r"^malwarebytes premium", r"^(norton|mcafee|kaspersky|bitdefender|eset)\b",
]
_PAID = re.compile("|".join(f"(?:{p})" for p in PAID_APPS), re.IGNORECASE)


def is_paid(name: str) -> bool:
    return bool(_PAID.search(name.strip()))


def owned_paid_apps(apps: list[dict]) -> list[dict]:
    """Return the paid apps from a scanned app list, as name/version/publisher only."""
    owned = {}
    for app in apps:
        name = str(app.get("name", "")).strip()
        if name and is_paid(name) and name.lower() not in owned:
            owned[name.lower()] = {"name": name,
                                   "version": str(app.get("version", "")).strip(),
                                   "publisher": str(app.get("publisher", "")).strip()}
    return sorted(owned.values(), key=lambda a: a["name"].lower())


def describe(app: dict) -> str:
    """'Adobe Photoshop 2025 (version 26)' or just the name when no version is known."""
    return f"{app['name']} (version {app['version']})" if app.get("version") else app["name"]
