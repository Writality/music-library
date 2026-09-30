#!/usr/bin/env python3
"""Update and validate generated fields in the music manifest."""

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
REQUIRED = {
    "title",
    "artist",
    "sourceUrl",
    "license",
    "licenseUrl",
    "attribution",
    "changes",
}


def main(check=False):
    data = json.loads(MANIFEST.read_text())
    files = set()
    ids = set()

    for track in data["tracks"]:
        track_id = track.get("id")
        file = track.get("file")

        if type(track_id) is not int or track_id <= 0 or track_id in ids:
            raise ValueError(f"Invalid or duplicate track id: {track_id}")

        if (
            not isinstance(file, str)
            or not file.startswith("tracks/")
            or not file.endswith(".mp3")
            or ".." in Path(file).parts
            or file in files
        ):
            raise ValueError(f"Invalid or duplicate track file: {file}")

        missing = [
            key for key in REQUIRED
            if not isinstance(track.get(key), str) or not track[key].strip()
        ]
        if missing:
            raise ValueError(f"Missing metadata for {file}: {', '.join(missing)}")

        path = ROOT / file
        if not path.is_file():
            raise ValueError(f"Missing audio file: {file}")

        ids.add(track_id)
        files.add(file)

        duration = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        digest = hashlib.sha256()
        with path.open("rb") as audio:
            for chunk in iter(lambda: audio.read(1024 * 1024), b""):
                digest.update(chunk)

        track.update(
            duration=round(float(duration)),
            sizeBytes=path.stat().st_size,
            sha256=digest.hexdigest(),
        )

    actual_files = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "tracks").rglob("*.mp3")
    }

    if files != actual_files:
        raise ValueError(
            f"Manifest/audio mismatch: "
            f"unlisted={sorted(actual_files - files)}, "
            f"missing={sorted(files - actual_files)}"
        )

    collection_ids = set()
    collection_names = set()

    for collection in data["collections"]:
        name = collection.get("id")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or name in collection_names
        ):
            raise ValueError(f"Invalid or duplicate collection id: {name}")
        collection_names.add(name)

        if "image" not in collection:
            raise ValueError(f"Missing image field for collection {name}")
        image = collection["image"]
        if image is not None:
            if (
                not isinstance(image, str)
                or Path(image).parent.as_posix() != f"images/{name}"
                or Path(image).suffix.lower()
                not in {".png", ".jpg", ".jpeg", ".webp", ".avif"}
                or not (ROOT / image).is_file()
            ):
                raise ValueError(f"Invalid or missing image for collection {name}: {image}")

        credit_keys = ("imageAttribution", "imageCreatorUrl", "imageSourceUrl")
        if any(key not in collection for key in credit_keys):
            raise ValueError(f"Missing image credit fields for collection {name}")
        credits = [collection[key] for key in credit_keys]
        if image is None and any(value is not None for value in credits):
            raise ValueError(f"Image credit without image for collection {name}")
        if image is not None and (
            not isinstance(credits[0], str)
            or not credits[0].strip()
            or any(
                not isinstance(url, str) or not url.startswith("https://")
                for url in credits[1:]
            )
        ):
            raise ValueError(f"Incomplete image credit for collection {name}")

        track_ids = collection["tracks"]

        if len(track_ids) != len(set(track_ids)):
            raise ValueError(f"Duplicate tracks in collection {collection['id']}")

        if not set(track_ids) <= ids:
            raise ValueError(f"Unknown tracks in collection {collection['id']}")

        collection_ids.update(track_ids)

    if ids != collection_ids:
        raise ValueError("Every track must appear in a collection")

    original = MANIFEST.read_text()
    updated = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if updated == original:
        print(f"Manifest verified for {len(files)} tracks")
        return

    if check:
        raise ValueError(
            "manifest.json needs updating; "
            "run python3 scripts/update_manifest.py"
        )

    data["generatedAt"] = datetime.now(timezone.utc).date().isoformat()
    MANIFEST.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )

    print(f"Updated manifest for {len(files)} tracks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    main(parser.parse_args().check)
