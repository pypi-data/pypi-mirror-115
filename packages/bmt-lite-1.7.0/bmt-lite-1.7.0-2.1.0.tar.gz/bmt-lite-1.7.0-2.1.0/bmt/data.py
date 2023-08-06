"""Biolink model data."""
import json
from typing import Dict, List, Optional

import importlib.resources as pkg_resources

from . import _data

with pkg_resources.open_text(_data, "all_classes.json") as stream:
    all_classes: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_elements.json") as stream:
    all_elements: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_slots.json") as stream:
    all_slots: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_types.json") as stream:
    all_types: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "ancestors.json") as stream:
    ancestors: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "descendants.json") as stream:
    descendants: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "children.json") as stream:
    children: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "parent.json") as stream:
    parent: Dict[str, Optional[str]] = json.load(stream)
with pkg_resources.open_text(_data, "element.json") as stream:
    element: Dict[str, Dict] = json.load(stream)
