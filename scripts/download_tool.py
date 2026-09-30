#!/usr/bin/env python3
"""Download one official, checksum-pinned Linux x86_64 tool into .chu/tools."""
import argparse
import gzip
import hashlib
import io
import json
import platform
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parents[1]


def extract_verified(data, spec):
    if hashlib.sha256(data).hexdigest() != spec["sha256"]:
        raise ValueError("Download checksum mismatch")
    kind = spec.get("format", "tar.gz")
    if kind == "raw":
        return data
    if kind == "gzip":
        return gzip.decompress(data)
    if kind == "zip":
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            member = archive.getinfo(spec["member"])
            if member.is_dir() or (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Tool must be a regular archive member")
            return archive.read(member)
    if kind != "tar.gz":
        raise ValueError(f"Unsupported archive format: {kind}")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        member = archive.getmember(spec["member"])
        if not member.isfile():
            raise ValueError("Tool must be a regular archive member")
        return archive.extractfile(member).read()


def install(name):
    lock = json.loads((ROOT / "dev/downloads.json").read_text())
    if f"{platform.system()}-{platform.machine()}" != lock["platform"]:
        raise RuntimeError("Pinned binary bootstrap currently supports Linux x86_64 only")
    spec = lock[name]
    cache = ROOT / ".chu/downloads" / spec["sha256"]
    if cache.exists():
        data = cache.read_bytes()
    else:
        with urllib.request.urlopen(spec["url"], timeout=60) as response:
            data = response.read()
    binary = extract_verified(data, spec)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(data)
    output = ROOT / ".chu/tools" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temp:
        temporary = Path(temp.name)
        try:
            temp.write(binary)
            temp.flush()
            temporary.chmod(0o755)
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
    print(f"Verified {name} {spec['version']}: {output}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    manifest = json.loads((ROOT / "dev/downloads.json").read_text())
    parser.add_argument("tool", choices=[k for k, v in manifest.items() if isinstance(v, dict)])
    install(parser.parse_args().tool)
