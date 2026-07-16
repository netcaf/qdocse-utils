"""
Subprocess wrapper around the lic-codec binary.

Binary resolution order:
  1. QDOCSE_CODEC_BIN environment variable
  2. lic-codec, next to this file  (pre-built artifact committed to the repo)
  3. lic-codec on PATH
"""

import dataclasses
import enum
import os
import subprocess
import tempfile
from pathlib import Path

__all__ = ["LicKind", "LicInfo", "encode", "encode_to_file"]

_DEFAULT_DURATION: int = 2_678_400       # 31 days in seconds
_DEFAULT_MODE:     int = 5
_DEFAULT_MAGIC:    int = 0xbdbdffffdbdb0001

_KIND_CMD = {1: "activation", 2: "elevation", 3: "renewal"}


class LicKind(enum.IntEnum):
    ACTIVATION = 1
    ELEVATION  = 2
    RENEWAL    = 3


@dataclasses.dataclass
class LicInfo:
    kind:       LicKind
    qid:        int
    foot_print: str
    duration:   int = _DEFAULT_DURATION
    mode:       int = _DEFAULT_MODE
    magic:      int = _DEFAULT_MAGIC


def _binary() -> str:
    if override := os.environ.get("QDOCSE_CODEC_BIN"):
        return override
    bundled = Path(__file__).parent / "lic-codec"
    if bundled.exists():
        return str(bundled)
    import shutil
    found = shutil.which("lic-codec")
    if found:
        return found
    raise FileNotFoundError(
        "lic-codec binary not found. "
        "Place it in helpers/lic-codec, set QDOCSE_CODEC_BIN, or add it to PATH."
    )


def encode(info: LicInfo) -> bytes:
    """Encode a LicInfo into an encrypted .dat payload."""
    kind = _KIND_CMD[int(info.kind)]
    tmp = tempfile.NamedTemporaryFile(suffix=".dat", delete=False)
    tmp.close()
    try:
        proc = subprocess.run(
            [
                _binary(), kind, "encode",
                "--qid",       str(info.qid),
                "--footprint", info.foot_print,
                "--mode",      str(info.mode),
                "--duration",  str(info.duration),
                "--magic",     str(info.magic),
                "--out",       tmp.name,
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"lic-codec {kind} encode failed: "
                f"{(proc.stderr or proc.stdout).strip()}"
            )
        with open(tmp.name, "rb") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


def encode_to_file(info: LicInfo, path: str) -> None:
    """Encode a LicInfo and write directly to a file."""
    kind = _KIND_CMD[int(info.kind)]
    proc = subprocess.run(
        [
            _binary(), kind, "encode",
            "--qid",       str(info.qid),
            "--footprint", info.foot_print,
            "--mode",      str(info.mode),
            "--duration",  str(info.duration),
            "--magic",     str(info.magic),
            "--out",       path,
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"lic-codec {kind} encode failed: "
            f"{(proc.stderr or proc.stdout).strip()}"
        )
