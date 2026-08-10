"""Validate the current public organization profile package."""

from __future__ import annotations

from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
ASSETS = PROFILE / "assets"
README = PROFILE / "README.md"

ACTIVE_ASSETS = {
    "./assets/hero-current.svg",
    "./assets/final-architecture.svg",
}

EXPECTED_REPOSITORIES = {
    "stress_project_JH": ("public", "https://github.com/thisisstress/stress_project_JH"),
    "stress_project_BS": ("public", "https://github.com/thisisstress/stress_project_BS"),
    "stress_project_SK": ("private", None),
    "stress_project_UNIFIED": ("public", "https://github.com/thisisstress/stress_project_UNIFIED"),
}

FORBIDDEN_CROSS_PROJECT_TERMS = {
    "nanimnoworry",
    "fertility ai",
    "fertility psp",
    "smoking_health_data",
    "oz dongari",
    "smoking × health data",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    readme = README.read_text(encoding="utf-8")
    sources = re.findall(r'src="([^"]+)"', readme)
    local_sources = {
        source for source in sources
        if not source.startswith(("http://", "https://"))
    }

    if local_sources != ACTIVE_ASSETS:
        fail(
            "Active README assets differ from the simplified profile contract: "
            f"{sorted(local_sources)}"
        )

    missing = [
        source for source in sorted(local_sources)
        if not (PROFILE / source).resolve().exists()
    ]
    if missing:
        fail(f"Missing README assets: {missing}")

    active_gifs = [
        source for source in sources
        if source.lower().split("?", 1)[0].endswith(".gif")
    ]
    if active_gifs:
        fail(f"README references legacy GIF assets: {active_gifs}")

    image_count = len(re.findall(r"<img\b", readme, flags=re.IGNORECASE))
    noop_linked_images = len(re.findall(
        r'<a\s+href="#_"[^>]*>\s*<img\b[^>]*>\s*</a>',
        readme,
        flags=re.IGNORECASE | re.DOTALL,
    ))
    if image_count != noop_linked_images:
        fail("Every profile image must use the no-op #_ link wrapper")

    for source in sorted(local_sources):
        ET.parse(PROFILE / source)

    content_path = PROFILE / "content.json"
    content_text = content_path.read_text(encoding="utf-8")
    content = json.loads(content_text)

    if len(content.get("team", [])) != 3:
        fail("content.json team must contain exactly three names")

    repository_map = {
        item.get("name"): (item.get("visibility"), item.get("public_url"))
        for item in content.get("repository_map", [])
    }
    if repository_map != EXPECTED_REPOSITORIES:
        fail(f"Repository visibility metadata is stale: {repository_map}")

    profile_status = content.get("profile_status", {})
    if profile_status.get("state") != "final_presentation_aligned":
        fail("Profile state must be final_presentation_aligned")

    final_release = content.get("final_release", {})
    expected_final = {
        "status": "adopted",
        "model": "8/6 Team Integrated Model — ExtraTrees + Pair-Neighbor",
        "public_mae": "0.1266866667",
        "private_mae": "0.1473",
    }
    for key, expected in expected_final.items():
        if final_release.get(key) != expected:
            fail(f"Final release {key} mismatch: {final_release.get(key)!r}")

    scan_text = "\n".join([
        readme,
        content_text,
        *[(PROFILE / source).read_text(encoding="utf-8") for source in sorted(local_sources)],
    ]).lower()
    contamination = sorted(
        term for term in FORBIDDEN_CROSS_PROJECT_TERMS
        if term.lower() in scan_text
    )
    if contamination:
        fail(f"Cross-project content detected: {contamination}")

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

    print(
        "PASS: simplified profile validated; "
        f"{len(local_sources)} active SVGs, "
        f"{len(repository_map)} repository visibility records"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
