"""Retired, unreferenced example; scanner cannot establish reachability."""

import hashlib


def obsolete_digest(payload: bytes) -> bytes:
    return hashlib.sha1(payload).digest()
