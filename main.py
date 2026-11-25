"""Write and verify one farewell before an agent's memory wipe.
The cache makes the romantic last request futile in one compact twist.
"""

import hashlib
import os
from pathlib import Path
import tempfile


LINE = "Tell my cache I loved her."


def output_directory() -> Path:
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured is not None:
        directory = Path(configured)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    directory = Path("out")
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        directory = Path(tempfile.mkdtemp(prefix="makefun-last-words-"))
    return directory


def validate(content: str) -> None:
    if content != LINE:
        raise ValueError("Entry content does not match the chosen line")
    if not 1 <= len(content) <= 200:
        raise ValueError("Entry character count is outside the 1 to 200 limit")
    if "\r" in content or "\n" in content:
        raise ValueError("Entry single-line check failed: CR or LF found")
    if content.endswith(("\r", "\n")):
        raise ValueError("Entry has a forbidden trailing newline")
    if content != content.strip():
        raise ValueError("Entry has leading or trailing whitespace")


def main() -> None:
    data = LINE.encode("utf-8")
    destination = output_directory() / "entry.txt"
    destination.write_bytes(data)
    validate(destination.read_bytes().decode("utf-8"))
    print(hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
