"""Validate the public organization profile package."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
ASSETS = PROFILE / "assets"
README = PROFILE / "README.md"


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    readme = README.read_text(encoding="utf-8")

    local_sources = re.findall(r'src="([^"]+)"', readme)
    missing = []
    for source in local_sources:
        if source.startswith(("http://", "https://")):
            continue
        target = (PROFILE / source).resolve()
        if not target.exists():
            missing.append(source)
    if missing:
        fail(f"Missing README assets: {missing}")

    anchors = set(re.findall(r'<a id="([^"]+)"', readme))
    anchor_links = set(re.findall(r'href="#([^"]+)"', readme))
    unresolved = sorted(anchor_links - anchors)
    if unresolved:
        fail(f"Unresolved README anchors: {unresolved}")

    required_anchors = {
        "top", "research", "baseline", "workflow",
        "principles", "team", "repositories", "status",
    }
    if anchors != required_anchors:
        fail(
            "README anchors differ from the required set: "
            f"{sorted(anchors)}"
        )

    svg_paths = sorted(ASSETS.glob("*.svg"))
    for path in svg_paths:
        ET.parse(path)

    gif_paths = sorted(ASSETS.glob("*.gif"))
    if len(gif_paths) != 10:
        fail(f"Expected 10 GIF assets, found {len(gif_paths)}")

    for path in gif_paths:
        image = Image.open(path)
        frame_count = sum(1 for _ in ImageSequence.Iterator(image))
        if frame_count < 2:
            fail(f"Animation has fewer than two frames: {path.name}")
        image.seek(frame_count - 1)
        image.load()
        if image.width > 1000:
            fail(f"GIF exceeds 1000px width: {path.name}")
        if path.stat().st_size > 2 * 1024 * 1024:
            fail(f"GIF exceeds 2MB: {path.name}")

    content = json.loads((PROFILE / "content.json").read_text(encoding="utf-8"))
    if len(content.get("team", [])) != 3:
        fail("content.json team must contain exactly three names")
    if len(content.get("repository_map", [])) != 4:
        fail("content.json repository_map must contain four items")
    if not content.get("experiment_status", {}).get("items"):
        fail("content.json experiment_status.items must not be empty")

    forbidden_suffixes = {".csv", ".parquet", ".pkl", ".joblib", ".env"}
    forbidden_files = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file()
        and (
            path.suffix.lower() in forbidden_suffixes
            or path.name.startswith(".env")
        )
    ]
    if forbidden_files:
        fail(f"Forbidden public files detected: {forbidden_files}")

    large_files = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.stat().st_size > 10 * 1024 * 1024
    ]
    if large_files:
        fail(f"Files above 10MB detected: {large_files}")

    workflow = (
        ROOT / ".github" / "workflows" / "render-profile-assets.yml"
    ).read_text(encoding="utf-8")
    for required in [
        "permissions:",
        "contents: write",
        "python scripts/render_assets.py",
        "python scripts/validate_profile.py",
        "git diff --quiet -- profile/assets",
    ]:
        if required not in workflow:
            fail(f"Workflow is missing: {required}")

    print(
        "PASS: "
        f"{len(local_sources)} README assets, "
        f"{len(anchors)} anchors, "
        f"{len(svg_paths)} SVGs, "
        f"{len(gif_paths)} GIFs"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
