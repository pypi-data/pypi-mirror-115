import codecs
from pathlib import Path
from typing import Iterator, Optional

import yaml


def extract_limited(loc: Path, context: str) -> dict:
    result = {}

    with open(loc / "details.yaml", "r") as readfile:
        result = yaml.load(readfile, Loader=yaml.FullLoader)

    result |= {"local": loc.name, "context": context}

    if extracted := extract_htmls(loc):
        for extract in extracted:
            result.update(extract)

    if result.get("docket", None):
        if "," in result["docket"]:
            result["docket_serial"] = result["docket"].split(",")[0]
    else:
        result["docket"] = False
        result["docket_serial"] = False

    if not result.get("date_prom", None):
        result["date_prom"] = False

    if not result.get("phil", None):
        result["phil"] = False

    if not result.get("scra", None):
        result["scra"] = False

    if result.get("annex", None):
        result["annex"] = True

    if result.get("ponente", None):
        result["ponente"] = result["ponente"].title()

    if result.get("ponencia", None):
        result["ponencia"] = True

    if result.get("ruling", None):
        result["ruling"] = True

    if result.get("ruling_marker", None):
        result["ruling"] = True

    if result.get("ruling_offset", None):
        result["ruling"] = True

    return result


def extract_htmls(loc: Path) -> Optional[Iterator[dict]]:
    """If files are found in the path, extract the content

    Args:
        loc (Path): Folder location

    Returns:
        Optional[Iterator[dict]]: [description]

    Yields:
        Iterator[Optional[Iterator[dict]]]: [description]
    """
    labels = ["annex", "ponencia", "fallo"]
    for label in labels:
        location = loc / f"{label}.html"
        if location.exists():
            f = codecs.open(str(location), "r")
            yield {label: f.read()}


def define_data(loc: Path) -> dict:
    """Given a folder's path, open the `details.yaml` file
    This describes the different metadata for the case.

    The folder path may also contain `html` files such as:
    1. The ponencia
    2. The annex
    3. The fallo

    If html files exist, extract content and combine
    all such html files in a single dictionary.

    Combined this with the data from the detail.yaml.

    Args:
        loc (Path): Folder location

    Returns:
        dict: A  dictionary containing content of folder path submitted.
    """
    result = {}
    with open(loc / "details.yaml", "r") as readfile:
        result = yaml.load(readfile, Loader=yaml.FullLoader)

    if extracted := extract_htmls(loc):
        for extract in extracted:
            result.update(extract)

    return result
