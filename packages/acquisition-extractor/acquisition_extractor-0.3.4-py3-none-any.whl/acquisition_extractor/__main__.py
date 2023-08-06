import re
from pathlib import Path
from typing import Generator, Iterator, Optional

from sqlite_utils import Database

from .decisions import define_data, extract_limited
from .statute_parts.title import ALLOWED_CATEGORIES
from .statutes import data_from_folder


def define_statute(parent: Path, child: Path, context: str) -> Optional[dict]:
    """

    Args:
        parent (Path): The parent path
        child (Path): The path to the statute
        context (str): The kind of statute

    Returns:
        Optional[dict]: [description]
    """
    # Is the folder digit-like, e.g. 209 or 209-A or 12-34-SC
    if not re.search(r"(^\d+-[A-C]$)|(^\d+$)|[a-zA-Z0-9-]+", child.name):
        print(f"Not digit-like: {child}")
        return None

    print(f"Processing: {child}")
    if data := data_from_folder(parent, context, child.name):
        return data
    else:
        print(f"Missing data: {child}")
        return None


def decode_statutes(parent: Path, context: str) -> Optional[Iterator[dict]]:
    """Given a parent directory `parent` with a subfolder `context`, generate statute-like data from entries of the subfolder, or the grandchildren of the parent directory.

    # TODO: make a `previously processed parameter` to check whether the subfolder already exists in the database;

    Args:
        parent (Path): The parent local directory, e.g. rawlaw
        context (str): Possible options include "ra", "eo", "pd", "ca", "bp", "act", "const"

    Returns:
        Optional[Iterator[dict]]: [description]

    Yields:
        Iterator[Optional[Iterator[dict]]]: [description]
    """
    if context not in ALLOWED_CATEGORIES:
        return None

    folder = parent / "statutes"
    if not folder.exists():
        return None

    subfolder = folder / context
    if not subfolder.exists():
        return None

    for child in subfolder.glob("*"):
        yield define_statute(folder, child, context)


def decode_decisions(loc: Path, context: str) -> Optional[Iterator[dict]]:
    """Given a parent directory "location" with a subfolder named "context",
    generate decision-like data from entries of the subfolder, or the grandchildren of the parent directory.

    Args:
        loc (Path): The parent local directory
        context (str): Either "legacy" or "sc"

    Returns:
        Optional[Iterator[dict]]: [description]

    Yields:
        Iterator[Optional[Iterator[dict]]]: [description]
    """
    if context not in ["legacy", "sc"]:
        return None

    folder = loc / "decisions" / context
    if not folder.exists():
        return None

    locations = folder.glob("*")
    for location in locations:
        yield define_data(location)


def extract_limited_data(locations: Generator, context: str) -> Iterator[dict]:
    for location in locations:
        yield extract_limited(location, context)


def get_db(loc: Path) -> Database:
    return Database(loc / f"decisions_index.db")


def context_in_decisions_exists(loc: Path, context: str) -> Optional[Path]:
    subcontext = loc / "decisions" / context
    return subcontext if subcontext.exists() else None


def index_decisions(loc: Path, context: str):
    db = get_db(loc)
    target = context_in_decisions_exists(loc, context)
    if not db or not target:
        raise Exception
    db.enable_wal()
    extracts = extract_limited_data(target.glob("*"), context)
    db["decisions"].insert_all(
        extracts,
        pk="local",
        column_order=(
            "context",
            "local",
            "docket_serial",
            "date_prom",
            "phil",
            "scra",
            "case_title",
        ),
        not_null=("phil", "scra", "docket", "docket_serial", "date_prom"),
        alter=True,
        ignore=True,
    )
    db.create_view(
        "no_dockets",
        """--sql
        select * from decisions where docket = 0 or docket_serial = 0;
        """,
        replace=True,
    )
    db.create_view(
        "no_dates",
        """ --sql
        select * from decisions where date_prom = 0;
        """,
        replace=True,
    )
    db.create_view(
        "no_reports",
        """ --sql
        select * from decisions where phil = 0 and scra = 0;
        """,
        replace=True,
    )
    db.enable_counts()


def index_all_decisions(loc: Path):
    for context in ["sc", "legacy"]:
        print(f"{context=} processing")
        index_decisions(loc, context)
