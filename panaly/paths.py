"""Generated paths, with read-only reuse of the original resources cache."""

from dataclasses import dataclass
from pathlib import Path

from panaly.models import Proceeding


def legacy_source_name(proceeding: Proceeding) -> str:
    conference, year, track = proceeding.conference, proceeding.year, proceeding.track
    if conference in {"acl", "coling", "emnlp"}:
        volume = "findings" if track.startswith("find") else "main"
        return f"{year}.{conference}.{volume}{proceeding.suffix}"
    if conference == "nips":
        volume = f".{track}" if track else ""
        return f"{year}.nips{volume}.htm"
    return f"{year}.{conference}{proceeding.suffix}"


def legacy_title_name(proceeding: Proceeding) -> str:
    track = "" if proceeding.conference == "naacl" else proceeding.track
    return f"title_{proceeding.conference}{str(proceeding.year)[2:]}{track}.txt"


@dataclass(frozen=True)
class Paths:
    data_dir: Path = Path("data")
    output_dir: Path = Path("outputs")
    legacy_dir: Path = Path("resources")

    def raw_path(self, proceeding: Proceeding) -> Path:
        return (
            self.data_dir / "raw" / proceeding.conference / f"{proceeding.key}{proceeding.suffix}"
        )

    def titles_path(self, proceeding: Proceeding) -> Path:
        return self.data_dir / "processed" / proceeding.conference / f"{proceeding.key}.txt"

    def source_path(self, proceeding: Proceeding) -> Path:
        current = self.raw_path(proceeding)
        legacy = self.legacy_dir / legacy_source_name(proceeding)
        return current if current.exists() or not legacy.exists() else legacy

    def readable_titles_path(self, proceeding: Proceeding) -> Path:
        current = self.titles_path(proceeding)
        legacy = self.legacy_dir / legacy_title_name(proceeding)
        return current if current.exists() or not legacy.exists() else legacy
