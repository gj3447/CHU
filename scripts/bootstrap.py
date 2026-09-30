#!/usr/bin/env python3
"""Install CHU's pinned local environment using existing uv/rustup/elan managers."""
import argparse
import json
import shutil
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def lean_is_installed(toolchain):
    result = subprocess.run(["elan", "toolchain", "list"], cwd=ROOT,
                            text=True, capture_output=True, check=True, timeout=30)
    return toolchain in {line.split()[0] for line in result.stdout.splitlines() if line.strip()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print exact setup argv without installation")
    args = parser.parse_args()
    rust = tomllib.loads((ROOT / "rust-toolchain.toml").read_text())["toolchain"]
    lean = (ROOT / "lean-toolchain").read_text().strip()
    commands = [["uv", "sync", "--locked"],
                ["rustup", "toolchain", "install", rust["channel"], "--profile", rust["profile"],
                 "--no-self-update", "--component", ",".join(rust["components"]),
                 "--target", ",".join(rust["targets"])],
                ["elan", "toolchain", "install", lean]]
    missing = [x[0] for x in commands if not shutil.which(x[0])]
    if missing and not args.dry_run:
        parser.error("Missing managers: " + ", ".join(missing) + "; see docs/DEVELOPMENT.md")
    for command in commands:
        print(command, flush=True)
        if not args.dry_run:
            if command[0] == "elan" and lean_is_installed(lean):
                print(f"Already installed: {lean}", flush=True)
                continue
            subprocess.run(command, cwd=ROOT, check=True, timeout=600)
    manifest = json.loads((ROOT / "dev/downloads.json").read_text())
    for name, spec in manifest.items():
        if isinstance(spec, dict) and spec.get("bootstrap", False):
            if args.dry_run:
                print(["python3", "scripts/download_tool.py", name])
            else:
                from download_tool import install
                install(name)


if __name__ == "__main__":
    main()
