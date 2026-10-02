#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright 2026 Tom F.
"""Fit a release's CHANGELOG section into a GitHub release body.

GitHub refuses a release body longer than 125,000 characters (HTTP 422,
"body is too long"). A section within LIMIT is left as it is. A longer one
is replaced, in place, by its introduction (the text before its first
`### ` heading) followed by a link to the full section.

Usage: release-notes-fit.py NOTES_FILE FULL_NOTES_URL
"""

from __future__ import annotations

import sys
from pathlib import Path

# GitHub's limit is 125,000; the margin covers the appended link paragraph.
LIMIT = 124_000


def fit(notes: str, url: str) -> str:
    if len(notes) <= LIMIT:
        return notes
    intro = notes.split("\n### ", 1)[0].rstrip()
    link = (
        "\n\n---\n\n"
        f"The full notes for this release are longer than GitHub allows in a "
        f"release description ({len(notes):,} characters). They are in "
        f"[`CHANGELOG.md` at this tag]({url}).\n"
    )
    if len(intro) + len(link) > LIMIT:
        intro = intro[: LIMIT - len(link)].rsplit("\n", 1)[0]
    return intro + link


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    notes = path.read_text(encoding="utf-8")
    fitted = fit(notes, sys.argv[2])
    if fitted != notes:
        print(
            f"::warning::Release notes are {len(notes):,} characters, over "
            f"GitHub's limit; posting the introduction ({len(fitted):,}) and "
            "a link to the full section."
        )
        path.write_text(fitted, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
