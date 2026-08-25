#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    ROOT / ".editorconfig",
    ROOT / "codeStyles" / "codeStyleConfig.xml",
    ROOT / "codeStyles" / "ORESoftware.xml",
    ROOT / "inspection" / "ORESoftware.xml",
    ROOT / "inspectionProfiles" / "profiles_settings.xml",
    ROOT / "editor.xml",
)
SENSITIVE = re.compile(
    r"(?i)(access[_-]?token|api[_-]?key|client[_-]?secret|private[_-]?key|password)\s*[=:]\s*[^$<{\s]"
)


def fail(message: str) -> None:
    raise SystemExit(message)


for required in REQUIRED:
    if not required.is_file():
        fail(f"missing required settings file: {required.relative_to(ROOT)}")

xml_files = sorted(path for path in ROOT.rglob("*.xml") if ".git" not in path.parts)
if len(xml_files) < 5:
    fail("expected at least five XML settings surfaces")

for path in xml_files:
    source = path.read_text(encoding="utf-8")
    try:
        ET.fromstring(source)
    except ET.ParseError as error:
        fail(f"invalid XML in {path.relative_to(ROOT)}: {error}")
    if SENSITIVE.search(source):
        fail(f"possible credential material in {path.relative_to(ROOT)}")

scheme = ET.parse(ROOT / "codeStyles" / "ORESoftware.xml").getroot()
if scheme.attrib.get("name") != "ORESoftware":
    fail("code style scheme name must remain ORESoftware")

profile = ET.parse(ROOT / "inspection" / "ORESoftware.xml").getroot()
tools = profile.findall(".//inspection_tool")
if len(tools) < 5 or any(tool.attrib.get("enabled") != "true" for tool in tools):
    fail("inspection profile must keep the required enabled tools")

editorconfig = (ROOT / ".editorconfig").read_text(encoding="utf-8")
for contract in ("root = true", "end_of_line = lf", "insert_final_newline = true"):
    if contract not in editorconfig:
        fail(f"missing EditorConfig contract: {contract}")

print(f"validated {len(xml_files)} XML settings files and .editorconfig")
