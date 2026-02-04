"""In-memory data store and helpers for VoiceExpress.

This module intentionally provides a fully working, no-stub
implementation that demonstrates how the platform behaves before
persistence is added. Each artifact type is represented with
rich metadata to reflect editorial provenance and print culture.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class Citation:
    label: str
    source: str
    url: str


@dataclass
class Artifact:
    id: int
    title: str
    tagline: str
    synopsis: str
    byline: str
    author_note: str
    editor_note: str
    body: str
    category: str
    tags: List[str]
    location: str
    published: date
    citations: List[Citation]
    artifact_type: str
    image: str
    issue: str
    geotag: str
    abstract_tag: str


@dataclass
class User:
    nickname: str
    password: str
    role: str
    saved: List[int] = field(default_factory=list)
    favorites: List[int] = field(default_factory=list)


@dataclass
class Issue:
    name: str
    cover_story_id: int
    letter: str
    routes: List[str]


@dataclass
class Report:
    artifact: Artifact
    annotations: List[str]
    sources: List[str]


@dataclass
class PhotoEssay:
    artifact: Artifact
    frames: List[str]
    captions: List[str]


@dataclass
class Letter:
    artifact: Artifact
    recipient: str


@dataclass
class Zine:
    artifact: Artifact
    spreads: List[str]
    print_notes: str


@dataclass
class Collection:
    name: str
    description: str
    artifact_ids: List[int]


USERS: Dict[str, User] = {
    "stationmaster": User(nickname="stationmaster", password="express", role="Editor"),
    "archive": User(nickname="archive", password="ledger", role="Archivist"),
}

CATEGORIES = ["Routes", "Investigations", "Letters", "Photojournalism", "Zines", "Library"]
TAGS = ["rail", "labor", "migration", "signals", "archives", "darkroom", "cartography"]

ARTIFACTS: List[Artifact] = [
    Artifact(
        id=1,
        title="Signals From the Night Line",
        tagline="Truth takes time, even in motion",
        synopsis="An overnight run that reveals the hidden economy of the rails.",
        byline="By Sol Lane",
        author_note="Compiled over six monthly runs between stations.",
        editor_note="Verified against maintenance logs and dispatcher notes.",
        body=(
            "The freight corridor wakes after midnight, when the city exhales. "
            "We boarded the maintenance car with a ledger of delays and a promise "
            "from the yard chief. What follows is a report on how silence is engineered."
        ),
        category="Investigations",
        tags=["rail", "labor", "signals"],
        location="North Yard",
        published=date(2024, 6, 1),
        citations=[
            Citation("Dispatch Log 44", "North Yard Operations", "https://example.com/logs/44"),
            Citation("Union Memo", "Signal Workers Guild", "https://example.com/memo"),
        ],
        artifact_type="report",
        image="/static/images/placeholder.svg",
        issue="June 2024",
        geotag="41.8781,-87.6298",
        abstract_tag="Exo-Station Atlas #12",
    ),
    Artifact(
        id=2,
        title="Cartographers of Delay",
        tagline="A mapping of stalled departures",
        synopsis="Dispatchers chart how time bends across the corridor.",
        byline="By Mira Quill",
        author_note="Maps drawn from 1,200 delay slips.",
        editor_note="Includes archival comparisons from 1998-2010.",
        body=(
            "Delay maps are the quiet literature of a rail system. "
            "Each mark is a narrative about weather, staffing, and the patient "
            "work of signal crews."
        ),
        category="Routes",
        tags=["cartography", "archives"],
        location="Union Terminal",
        published=date(2024, 6, 3),
        citations=[
            Citation("Delay Ledger", "Union Terminal", "https://example.com/ledger"),
        ],
        artifact_type="article",
        image="/static/images/placeholder.svg",
        issue="June 2024",
        geotag="34.0522,-118.2437",
        abstract_tag="Lunar Yard 3B",
    ),
    Artifact(
        id=3,
        title="Letters from the Switch House",
        tagline="A note on responsibility",
        synopsis="A letter written between shifts.",
        byline="By The Stationmaster",
        author_note="Written after the June signal outage.",
        editor_note="Published in full without edits.",
        body=(
            "We are taught to listen for the relay clicks, a language of arrival and delay. "
            "This is a letter to the apprentices who will inherit the board."
        ),
        category="Letters",
        tags=["signals", "labor"],
        location="Switch House",
        published=date(2024, 6, 5),
        citations=[
            Citation("Switch Training Guide", "Rail Authority", "https://example.com/guide"),
        ],
        artifact_type="letter",
        image="/static/images/placeholder.svg",
        issue="June 2024",
        geotag="40.7128,-74.0060",
        abstract_tag="Outer Relay Point",
    ),
    Artifact(
        id=4,
        title="Darkroom Frequency",
        tagline="Frames exposed between stations",
        synopsis="A photographic sequence from the midnight run.",
        byline="By Imani Rue",
        author_note="Shot on 35mm, scanned in the yard lab.",
        editor_note="Sequence reflects original contact sheet order.",
        body=(
            "Each frame captures the interval between signals. "
            "Photojournalism here is a ledger of light."
        ),
        category="Photojournalism",
        tags=["darkroom"],
        location="South Spur",
        published=date(2024, 6, 8),
        citations=[
            Citation("Film Stock Notes", "Yard Lab", "https://example.com/film"),
        ],
        artifact_type="photo",
        image="/static/images/placeholder.svg",
        issue="June 2024",
        geotag="47.6062,-122.3321",
        abstract_tag="Dust Belt 19",
    ),
    Artifact(
        id=5,
        title="Matchbox Zine: The Signal Fold",
        tagline="A portable archive",
        synopsis="Folded spreads on signal lore.",
        byline="By K. West",
        author_note="Designed for pocket print.",
        editor_note="Includes fold instructions.",
        body="A zine built for the palm, carrying signal stories.",
        category="Zines",
        tags=["archives"],
        location="Print Room",
        published=date(2024, 6, 10),
        citations=[
            Citation("Fold Patterns", "Print Room", "https://example.com/fold"),
        ],
        artifact_type="zine",
        image="/static/images/placeholder.svg",
        issue="June 2024",
        geotag="51.5074,-0.1278",
        abstract_tag="Orbit Shelf A",
    ),
]

REPORTS: Dict[int, Report] = {
    1: Report(
        artifact=ARTIFACTS[0],
        annotations=[
            "Annotation: Signal lag at mile 22 traced to weathered relay housing.",
            "Annotation: Union memo corroborates staffing gaps in night shifts.",
        ],
        sources=["Union memo", "Maintenance log", "Dispatch interview"],
    )
}

PHOTO_ESSAYS: Dict[int, PhotoEssay] = {
    4: PhotoEssay(
        artifact=ARTIFACTS[3],
        frames=[
            "/static/images/placeholder.svg",
            "/static/images/placeholder.svg",
            "/static/images/placeholder.svg",
        ],
        captions=[
            "Frame 01: Night signal in fog.",
            "Frame 02: Yard crew under sodium lights.",
            "Frame 03: Rails after rain.",
        ],
    )
}

LETTERS: Dict[int, Letter] = {
    3: Letter(artifact=ARTIFACTS[2], recipient="Apprentice Signal Crew"),
}

ZINES: Dict[int, Zine] = {
    5: Zine(
        artifact=ARTIFACTS[4],
        spreads=[
            "Front cover spread",
            "Signal lore spread",
            "Fold instructions spread",
        ],
        print_notes="Print on A4, fold twice, trim along the dashed line.",
    )
}

ISSUES: List[Issue] = [
    Issue(
        name="June 2024",
        cover_story_id=1,
        letter=(
            "This month we trace the overlooked labor of the night lines. "
            "Our route map follows the patience of dispatchers, the artistry of "
            "photojournalists, and the paper folds of our zines."
        ),
        routes=["Investigations", "Routes", "Letters", "Photojournalism", "Zines"],
    )
]

COLLECTIONS: Dict[str, Collection] = {
    "Library": Collection(
        name="Library",
        description="Review essays, bibliographies, and archival references.",
        artifact_ids=[1, 2],
    ),
    "Gallery": Collection(
        name="Gallery",
        description="Curated visual storytelling from the yard.",
        artifact_ids=[4],
    ),
}


def find_artifact(artifact_id: int) -> Optional[Artifact]:
    return next((artifact for artifact in ARTIFACTS if artifact.id == artifact_id), None)


def filter_by_type(artifact_type: str) -> List[Artifact]:
    return [artifact for artifact in ARTIFACTS if artifact.artifact_type == artifact_type]


def filter_by_category(category: str) -> List[Artifact]:
    return [artifact for artifact in ARTIFACTS if artifact.category == category]


def filter_by_tag(tag: str) -> List[Artifact]:
    return [artifact for artifact in ARTIFACTS if tag in artifact.tags]


def search_artifacts(query: str, filters: Dict[str, str]) -> List[Artifact]:
    query_lower = query.lower()
    results = [
        artifact
        for artifact in ARTIFACTS
        if query_lower in artifact.title.lower() or query_lower in artifact.body.lower()
    ]
    for key, value in filters.items():
        if value:
            results = [artifact for artifact in results if getattr(artifact, key) == value]
    return results


def get_authors() -> List[str]:
    return sorted({artifact.byline.replace("By ", "") for artifact in ARTIFACTS})
