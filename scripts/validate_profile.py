"""Validate the final public organization profile package."""

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

    # The final profile intentionally uses vector animation only. Historical
    # GIF files may remain in profile/assets for provenance, but README must
    # not actively reference them.
    active_gifs = [
        source for source in local_sources
        if source.lower().split("?", 1)[0].endswith(".gif")
    ]
    if active_gifs:
        fail(f"README still references legacy GIF assets: {active_gifs}")

    required_vector_assets = {
        "./assets/hero-current.svg",
        "./assets/final-architecture.svg",
        "./assets/final-workflow.svg",
        "./assets/final-principles.svg",
        "./assets/final-team.svg",
        "./assets/final-repositories.svg",
        "./assets/final-status.svg",
        "./assets/final-footer.svg",
    }
    missing_required = sorted(required_vector_assets - set(local_sources))
    if missing_required:
        fail(f"README is missing final vector assets: {missing_required}")

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

    # GitHub may turn an unwrapped README image into a direct link to the
    # underlying file. Every profile image therefore has an explicit,
    # meaningful destination.
    without_linked_images = re.sub(
        r"<a\b[^>]*>.*?<img\b[^>]*>.*?</a>",
        "",
        readme,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if re.search(r"<img\b", without_linked_images, flags=re.IGNORECASE):
        fail("Every README image must be wrapped in an explicit link")

    asset_link_targets = re.findall(
        r'href="([^"]*(?:assets/|\.(?:gif|png|svg)(?:\?[^"]*)?$)[^"]*)"',
        readme,
        flags=re.IGNORECASE,
    )
    if asset_link_targets:
        fail(
            "README images must not link to raw asset files: "
            f"{asset_link_targets}"
        )

    for marker in [
        "<!-- CURRENT-RESULT:START -->",
        "<!-- CURRENT-RESULT:END -->",
    ]:
        if readme.count(marker) != 1:
            fail(f"README marker must appear exactly once: {marker}")

    stale_readme_phrases = [
        "final publication pending",
        "research in progress · current result",
        "current result snapshot: 2026-08-07",
        "brand-footer.gif",
        "experiment-status.gif",
        "repository-map.gif",
        "team-network.gif",
        "principles.gif",
        "pipeline.gif",
        "baseline-architecture.gif",
    ]
    lower_readme = readme.lower()
    stale_hits = [
        phrase for phrase in stale_readme_phrases
        if phrase.lower() in lower_readme
    ]
    if stale_hits:
        fail(f"README contains stale profile text/assets: {stale_hits}")

    svg_paths = sorted(ASSETS.glob("*.svg"))
    for path in svg_paths:
        ET.parse(path)

    # Legacy GIFs are archival rather than active profile dependencies. Keep
    # validating any that remain so repository corruption is still detected,
    # but do not require a fixed historical count.
    gif_paths = sorted(ASSETS.glob("*.gif"))
    for path in gif_paths:
        image = Image.open(path)
        frame_count = sum(1 for _ in ImageSequence.Iterator(image))
        if frame_count < 2:
            fail(f"Animation has fewer than two frames: {path.name}")
        image.seek(frame_count - 1)
        image.load()
        if image.width > 1000:
            fail(f"Legacy GIF exceeds 1000px width: {path.name}")
        if path.stat().st_size > 2 * 1024 * 1024:
            fail(f"Legacy GIF exceeds 2MB: {path.name}")

    content = json.loads(
        (PROFILE / "content.json").read_text(encoding="utf-8")
    )
    if len(content.get("team", [])) != 3:
        fail("content.json team must contain exactly three names")
    if len(content.get("repository_map", [])) != 4:
        fail("content.json repository_map must contain four items")
    if not content.get("experiment_status", {}).get("items"):
        fail("content.json experiment_status.items must not be empty")

    profile_status = content.get("profile_status", {})
    if profile_status.get("state") not in {
        "research_in_progress",
        "research_complete",
        "final_presentation_aligned",
    }:
        fail(
            "content.json profile_status.state must be a supported profile state"
        )
    if not profile_status.get("as_of"):
        fail("content.json profile_status.as_of must not be empty")

    final_release = content.get("final_release", {})
    if final_release.get("status") not in {"pending", "published", "adopted"}:
        fail(
            "content.json final_release.status must be pending, published, or adopted"
        )
    if final_release.get("status") in {"published", "adopted"}:
        for key in ["model", "public_mae", "updated_at"]:
            if not final_release.get(key):
                fail(
                    "Final release is missing required field: "
                    f"{key}"
                )

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
        "contents: read",
        "python scripts/validate_profile.py",
    ]:
        if required not in workflow:
            fail(f"Workflow is missing: {required}")

    active_vector_count = sum(
        1 for source in local_sources
        if source.lower().split("?", 1)[0].endswith(".svg")
    )
    print(
        "PASS: "
        f"{len(local_sources)} README assets, "
        f"{len(anchors)} anchors, "
        f"{active_vector_count} active SVG references, "
        f"{len(svg_paths)} SVG files, "
        f"{len(gif_paths)} archival GIFs"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
