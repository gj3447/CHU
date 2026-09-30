import gzip
import hashlib
import io
import json
import subprocess
import tarfile
import zipfile

import pytest

from chu_dev import ROOT, matches_version
from download_tool import extract_verified


def test_cross_engine_comparison_normalizes_dates_but_preserves_values_and_multiplicity():
    from check_cli_tools import bindings
    def result(value, datatype="http://www.w3.org/2001/XMLSchema#dateTime", count=1):
        return {"results": {"bindings": [{"date": {"type": "literal", "value": value,
                                                  "datatype": datatype}}] * count}}
    expected = bindings(result("2026-09-30T00:00:00+00:00"))
    assert expected == bindings(result("2026-09-30T00:00:00Z"))
    assert expected != bindings(result("2026-09-30T00:00:01Z"))
    assert expected != bindings(result("2026-09-30T00:00:00Z", count=2))
    assert expected != bindings(result("2026-09-30T00:00:00+00:00", datatype="urn:other:datatype"))


@pytest.mark.parametrize("kind", ["raw", "gzip", "zip", "tar.gz"])
def test_download_formats_select_exact_member_and_check_digest(kind):
    binary = b"pinned binary bytes"
    stream = io.BytesIO()
    if kind == "raw":
        data = binary
    elif kind == "gzip":
        data = gzip.compress(binary)
    elif kind == "zip":
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("unrelated", b"wrong tool")
            archive.writestr("release/tool", binary)
        data = stream.getvalue()
    else:
        with tarfile.open(fileobj=stream, mode="w:gz") as archive:
            member = tarfile.TarInfo("release/tool")
            member.size = len(binary)
            archive.addfile(member, io.BytesIO(binary))
        data = stream.getvalue()
    spec = {"format": kind, "member": "release/tool", "sha256": hashlib.sha256(data).hexdigest()}
    assert extract_verified(data, spec) == binary
    with pytest.raises(ValueError, match="checksum"):
        extract_verified(data + b"tampered", spec)


@pytest.mark.parametrize("kind", ["zip", "tar.gz"])
def test_download_rejects_symlinks(kind):
    stream = io.BytesIO()
    if kind == "zip":
        with zipfile.ZipFile(stream, "w") as archive:
            member = zipfile.ZipInfo("tool")
            member.create_system = 3
            member.external_attr = 0o120777 << 16
            archive.writestr(member, "../../outside")
    else:
        with tarfile.open(fileobj=stream, mode="w:gz") as archive:
            member = tarfile.TarInfo("tool")
            member.type = tarfile.SYMTYPE
            member.linkname = "../../outside"
            archive.addfile(member)
    data = stream.getvalue()
    with pytest.raises(ValueError, match="regular"):
        extract_verified(data, {"format": kind, "member": "tool", "sha256": hashlib.sha256(data).hexdigest()})


def test_version_probes_accept_v_prefix_but_reject_partial_tokens():
    assert matches_version("v1.5.6 (Variegata)", "1.5.6")
    assert matches_version("jq-1.8.2", "1.8.2")
    assert not matches_version("v1.5.60", "1.5.6")
    assert not matches_version("11.5.6", "1.5.6")


def test_tool_wrapper_forwards_json_and_failure_without_shell(tmp_path):
    command = [str(ROOT / "chu"), "tool", "jq", "--"]
    result = subprocess.run([*command, "-n", "--arg", "literal", "$(touch sentinel); `id`", "$literal"],
                            cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0
    assert json.loads(result.stdout) == "$(touch sentinel); `id`"
    failure = subprocess.run([*command, "-n", "-e", "false"], cwd=tmp_path,
                             capture_output=True, text=True, timeout=60)
    assert failure.returncode == 1 and json.loads(failure.stdout) is False
