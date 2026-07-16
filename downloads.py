"""The local package download cache: `var/downloads/release/{version}/{build}/{distro}/`.

Exists as its own module because both release.py (writes the layout, including a
KERNEL_SIDECAR_SUFFIX sidecar per package) and csp.py (reads it back to batch-discover what's
ready to upload) need it, and neither should depend on the other -- this is the neutral,
shared piece that keeps that boundary intact.
"""

import os
from typing import Optional

# qdocse's installers refuse to install on a kernel they weren't built for, so
# release.ReleaseServer.download_package() writes the exact compiled-for kernel version
# alongside each downloaded package in a sidecar file using this suffix; discover_local_packages()
# reads it back.
KERNEL_SIDECAR_SUFFIX = ".kernel"


def latest_local_build(local_dir: str, version: str) -> Optional[str]:
    """The newest build already downloaded under local_dir/{version}/, or None if nothing is.

    "Newest" uses the same ordering as release.ReleaseServer.list_builds(): numeric build
    names sort numerically, non-numeric ones (e.g. 'test1') after them alphabetically, and
    the last one wins. Note this is "latest among what's been downloaded", not "latest on
    the release server" -- a stale cache resolves to a stale build.
    """
    version_dir = os.path.join(local_dir, version)
    if not os.path.isdir(version_dir):
        return None
    builds = [b for b in os.listdir(version_dir) if os.path.isdir(os.path.join(version_dir, b))]
    builds.sort(key=lambda b: (0, int(b)) if b.isdigit() else (1, b))
    return builds[-1] if builds else None


def discover_local_packages(
    local_dir: str,
    version: Optional[str] = None,
    build: Optional[str] = None,
    distro: Optional[str] = None,
) -> list:
    """Finds package files already downloaded under local_dir/{version}/{build}/{distro}/
    (the layout release.ReleaseServer.download_package() uses), optionally filtered by
    version/build/distro.

    Each entry's "kernel_version", if present, comes from the KERNEL_SIDECAR_SUFFIX sidecar
    file written alongside the package. Sidecar files themselves are skipped, not treated
    as packages.
    """
    entries = []
    if not os.path.isdir(local_dir):
        return entries
    for v in sorted(os.listdir(local_dir)):
        if version is not None and v != version:
            continue
        v_dir = os.path.join(local_dir, v)
        if not os.path.isdir(v_dir):
            continue
        for b in sorted(os.listdir(v_dir)):
            if build is not None and b != build:
                continue
            b_dir = os.path.join(v_dir, b)
            if not os.path.isdir(b_dir):
                continue
            for d in sorted(os.listdir(b_dir)):
                if distro is not None and d != distro:
                    continue
                d_dir = os.path.join(b_dir, d)
                if not os.path.isdir(d_dir):
                    continue
                for filename in sorted(os.listdir(d_dir)):
                    if filename.endswith(KERNEL_SIDECAR_SUFFIX):
                        continue
                    local_path = os.path.join(d_dir, filename)
                    if not os.path.isfile(local_path):
                        continue
                    entry = {"version": v, "build": b, "distro": d, "local_path": local_path}
                    kernel_sidecar = local_path + KERNEL_SIDECAR_SUFFIX
                    if os.path.isfile(kernel_sidecar):
                        with open(kernel_sidecar) as f:
                            entry["kernel_version"] = f.read().strip()
                    entries.append(entry)
    return entries
