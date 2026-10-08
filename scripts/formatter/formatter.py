from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
DIVIDER = ";" + "-" * 49

STATEDEF_PATTERN = re.compile(r"^\s*\[statedef\s+(-?\d+)\s*\]\s*$", re.IGNORECASE)
STATE_PATTERN = re.compile(r"^\s*\[state(?:\s+[^\]]*)?\]\s*$", re.IGNORECASE)
SECTION_PATTERN = re.compile(r"^\s*\[[^\]]+\]\s*$")
CANONICAL_STATEDEF_PATTERN = re.compile(r"^\[statedef\s+(-?\d+)\]$")
DOCUMENT_STATEDEF_PATTERN = re.compile(r"^### StateDef -?\d+: .+$")
TRIGGER_PATTERN = re.compile(r"^\s*trigger(?:all|\d+)\s*=", re.IGNORECASE)
COMMAND_PATTERN = re.compile(r"\bcommand\b", re.IGNORECASE)
OPERATOR_WITH_SPACES_PATTERN = re.compile(
    r"[ \t]*(\*\*|&&|\|\||\^\^|:=|!=|>=|<=|[=<>+\-*/%&|^])[ \t]*"
)

DEFINITION_FILES = (
    "tenkikai.def",
    "cns/anim.air",
    "cns/command.cmd",
    "cns/constants.cns",
    "cns/common1.cns",
    "cns/state.cns",
    "cns/observ.cns",
    "cns/helper.cns",
)
STATE_FORMAT_FILES = {
    "cns/command.cmd",
    "cns/common1.cns",
    "cns/state.cns",
    "cns/observ.cns",
    "cns/helper.cns",
}
SCREENBOUND_LOCATIONS = {
    ("cns/observ.cns", -2),
    ("cns/helper.cns", 99000),
}
STATE_CONTROLLER_TYPES = frozenset({
    "afterimage",
    "afterimagetime",
    "allpalfx",
    "angleadd",
    "angledraw",
    "anglemul",
    "angleset",
    "appendtoclipboard",
    "assertspecial",
    "attackdist",
    "attackmulset",
    "bgpalfx",
    "bindtoparent",
    "bindtoroot",
    "bindtotarget",
    "changeanim",
    "changeanim2",
    "changestate",
    "clearclipboard",
    "ctrlset",
    "defencemulset",
    "destroyself",
    "displaytoclipboard",
    "envcolor",
    "envshake",
    "explod",
    "explodbindtime",
    "fallenvshake",
    "forcefeedback",
    "gamemakeanim",
    "gravity",
    "helper",
    "hitadd",
    "hitby",
    "hitdef",
    "hitfalldamage",
    "hitfallset",
    "hitfallvel",
    "hitoverride",
    "hitvelset",
    "lifeadd",
    "lifeset",
    "makedust",
    "modifyexplod",
    "movehitreset",
    "nothitby",
    "null",
    "offset",
    "palfx",
    "parentvaradd",
    "parentvarset",
    "pause",
    "playerpush",
    "playsnd",
    "posadd",
    "posfreeze",
    "posset",
    "poweradd",
    "powerset",
    "projectile",
    "removeexplod",
    "reversaldef",
    "screenbound",
    "selfstate",
    "sprpriority",
    "statetypeset",
    "stopsnd",
    "superpause",
    "targetbind",
    "targetdrop",
    "targetfacing",
    "targetlifeadd",
    "targetpoweradd",
    "targetstate",
    "targetveladd",
    "targetvelset",
    "trans",
    "turn",
    "varadd",
    "varrandom",
    "varrangeset",
    "varset",
    "veladd",
    "velmul",
    "velset",
    "width",
})


def read_lines(path: Path) -> list[str]:
    data = path.read_bytes()
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data.decode("latin-1").split("\n")


def encoded_lines(lines: list[str]) -> bytes:
    return ("\n".join(lines) + "\n").encode("latin-1")


def is_divider_comment(line: str) -> bool:
    stripped = line.lstrip(" \t")
    return stripped.startswith((";-", ";="))


def unquoted_character_index(line: str, character: str) -> int:
    quoted = False
    escaped = False

    for index, value in enumerate(line):
        if escaped:
            escaped = False
            continue
        if value == "\\" and quoted:
            escaped = True
            continue
        if value == '"':
            quoted = not quoted
            continue
        if value == character and not quoted:
            return index

    return -1


def strip_comments(lines: list[str], keep_dividers: bool = True) -> list[str]:
    result: list[str] = []

    for source_line in lines:
        line = source_line.rstrip(" \t")
        stripped = line.lstrip(" \t")

        if stripped.startswith(";;"):
            result.append(stripped)
            continue

        if stripped.startswith(";"):
            if keep_dividers and is_divider_comment(stripped):
                result.append(DIVIDER)
            continue

        comment_at = unquoted_character_index(line, ";")
        if comment_at >= 0:
            line = line[:comment_at].rstrip(" \t")

        result.append(line)

    return result


def canonicalize_states(lines: list[str]) -> list[str]:
    result: list[str] = []
    inside_state = False

    for source_line in lines:
        line = source_line
        statedef_match = STATEDEF_PATTERN.match(line)

        if statedef_match:
            inside_state = True
            result.append(f"[statedef {statedef_match.group(1)}]")
            continue

        if STATE_PATTERN.match(line):
            inside_state = True
            result.append("[state ]")
            continue

        if SECTION_PATTERN.match(line):
            inside_state = False
            result.append(line.strip())
            continue

        if line.lstrip(" \t").startswith(";;"):
            result.append(line.strip())
            continue

        if inside_state and line:
            line = line.strip()
            quoted_value = "=" in line and line.split("=", 1)[1].lstrip().startswith('"')
            if quoted_value:
                key, value = line.split("=", 1)
                line = f"{key.strip()}={value.lstrip()}"
            else:
                line = OPERATOR_WITH_SPACES_PATTERN.sub(r"\1", line)
                type_match = re.match(r"^type=(.+)$", line, re.IGNORECASE)
                if type_match:
                    line = f"type={type_match.group(1).lower()}"

        result.append(line)

    return result


def normalize_blank_lines(lines: list[str]) -> list[str]:
    result: list[str] = []

    for line in lines:
        if line:
            result.append(line.rstrip(" \t"))
        elif result and result[-1]:
            result.append("")

    while result and not result[-1]:
        result.pop()

    return result


def remove_ascii_spaces_outside_quotes(line: str) -> str:
    result: list[str] = []
    quoted = False
    escaped = False

    for value in line:
        if escaped:
            result.append(value)
            escaped = False
            continue
        if value == "\\" and quoted:
            result.append(value)
            escaped = True
            continue
        if value == '"':
            result.append(value)
            quoted = not quoted
            continue
        if value != " " or quoted:
            result.append(value)

    return "".join(result)


def remove_ascii_spaces(lines: list[str]) -> list[str]:
    return [remove_ascii_spaces_outside_quotes(line) for line in lines]


def remove_ascii_spaces_from_sections(
    lines: list[str], section_names: set[str]
) -> list[str]:
    result: list[str] = []
    compact = False

    for line in lines:
        if SECTION_PATTERN.match(line):
            compact = line.strip()[1:-1].lower() in section_names
            result.append(line.strip())
        elif compact:
            result.append(remove_ascii_spaces_outside_quotes(line))
        else:
            result.append(line)

    return result


def remove_ascii_spaces_from_command_definitions(lines: list[str]) -> list[str]:
    result: list[str] = []
    inside_state = False

    for line in lines:
        if CANONICAL_STATEDEF_PATTERN.match(line):
            inside_state = True

        if inside_state:
            result.append(line)
        else:
            result.append(remove_ascii_spaces_outside_quotes(line))

    return result


def ensure_state_spacing(lines: list[str]) -> list[str]:
    result: list[str] = []

    for line in lines:
        if (CANONICAL_STATEDEF_PATTERN.match(line) or line == "[state ]") and result and result[-1]:
            result.append("")
        result.append(line)

    return normalize_blank_lines(result)


def transform_definition(lines: list[str], format_states: bool) -> list[str]:
    result = strip_comments(lines)
    if format_states:
        result = canonicalize_states(result)
    result = normalize_blank_lines(result)
    if format_states:
        result = ensure_state_spacing(result)
    return result


def statedef_number(line: str) -> int | None:
    match = CANONICAL_STATEDEF_PATTERN.match(line)
    if not match:
        return None
    return int(match.group(1))


def verify_command_trigger_scope(name: str, lines: list[str]) -> None:
    current_statedef: int | None = None
    current_controller = "State Controller外"

    for line_number, line in enumerate(lines, start=1):
        statedef_match = STATEDEF_PATTERN.match(line)
        if statedef_match:
            current_statedef = int(statedef_match.group(1))
            current_controller = "State Controller外"
            continue

        if SECTION_PATTERN.match(line) and not STATE_PATTERN.match(line):
            current_statedef = None
            current_controller = "State Controller外"
            continue

        if STATE_PATTERN.match(line):
            current_controller = "type未定義"
            continue

        type_match = re.match(r"^\s*type\s*=\s*(.+?)\s*$", line, re.IGNORECASE)
        if type_match:
            current_controller = type_match.group(1).lower()
            continue

        executable = line.split(";", 1)[0]
        if not TRIGGER_PATTERN.match(executable):
            continue

        expression = executable.split("=", 1)[1]
        if not COMMAND_PATTERN.search(expression):
            continue

        if (
            name == "cns/command.cmd"
            and current_statedef == -1
            and current_controller == "varset"
        ):
            continue

        if current_statedef is None:
            state_context = "StateDef外"
        else:
            state_context = f"StateDef {current_statedef}"
        raise RuntimeError(
            "command Triggerの配置が不正です: "
            f"{name}:{line_number} ({state_context}, {current_controller})"
        )


def verify_command_trigger_locations() -> None:
    for name in sorted(STATE_FORMAT_FILES):
        verify_command_trigger_scope(name, read_lines(ROOT / name))


def verify_state_controller_types_in_lines(name: str, lines: list[str]) -> None:
    inside_controller = False

    for line_number, source_line in enumerate(lines, start=1):
        line = source_line
        comment_at = unquoted_character_index(line, ";")
        if comment_at >= 0:
            line = line[:comment_at]
        line = line.strip()

        if STATE_PATTERN.match(line):
            inside_controller = True
            continue

        if SECTION_PATTERN.match(line):
            inside_controller = False
            continue

        if not inside_controller:
            continue

        type_match = re.match(r"^type\s*=\s*(.+?)\s*$", line, re.IGNORECASE)
        if not type_match:
            continue

        controller_type = type_match.group(1).lower()
        if controller_type not in STATE_CONTROLLER_TYPES:
            raise RuntimeError(
                "存在しないState Controllerです: "
                f"{name}:{line_number} ({type_match.group(1)})"
            )


def verify_state_controller_types() -> None:
    for name in sorted(STATE_FORMAT_FILES):
        verify_state_controller_types_in_lines(name, read_lines(ROOT / name))


def screenbound_locations_in_lines(name: str, lines: list[str]) -> list[tuple[str, int | None, int]]:
    current_statedef: int | None = None
    inside_controller = False
    locations: list[tuple[str, int | None, int]] = []

    for line_number, source_line in enumerate(lines, start=1):
        line = source_line
        comment_at = unquoted_character_index(line, ";")
        if comment_at >= 0:
            line = line[:comment_at]
        line = line.strip()

        statedef_match = STATEDEF_PATTERN.match(line)
        if statedef_match:
            current_statedef = int(statedef_match.group(1))
            inside_controller = False
            continue

        if STATE_PATTERN.match(line):
            inside_controller = True
            continue

        if SECTION_PATTERN.match(line):
            current_statedef = None
            inside_controller = False
            continue

        if not inside_controller:
            continue

        type_match = re.match(r"^type\s*=\s*(.+?)\s*$", line, re.IGNORECASE)
        if type_match and type_match.group(1).lower() == "screenbound":
            locations.append((name, current_statedef, line_number))

    return locations


def verify_screenbound_locations_in_files(files: dict[str, list[str]]) -> None:
    counts = {location: 0 for location in SCREENBOUND_LOCATIONS}

    for name, lines in files.items():
        for file_name, statedef, line_number in screenbound_locations_in_lines(name, lines):
            location = (file_name, statedef)
            if location not in SCREENBOUND_LOCATIONS:
                raise RuntimeError(
                    "ScreenBoundの配置が不正です: "
                    f"{file_name}:{line_number} (StateDef {statedef})"
                )
            counts[location] += 1

    for file_name, statedef in sorted(SCREENBOUND_LOCATIONS):
        count = counts[(file_name, statedef)]
        if count != 1:
            raise RuntimeError(
                "ScreenBoundは指定位置に1件だけ必要です: "
                f"{file_name} (StateDef {statedef}, 検出数={count})"
            )


def verify_screenbound_locations() -> None:
    files = {
        name: read_lines(ROOT / name)
        for name in sorted(STATE_FORMAT_FILES)
    }
    verify_screenbound_locations_in_files(files)


class Reporter:
    def __init__(self, check: bool = False) -> None:
        self.changed = 0
        self.check = check

    def write_lines(self, path: Path, lines: list[str]) -> None:
        self.write_bytes(path, encoded_lines(lines))

    def write_bytes(self, path: Path, data: bytes) -> None:
        old_data = path.read_bytes() if path.exists() else None
        relative = path.relative_to(ROOT)

        if old_data == data:
            print(f"変更なし: {relative}")
            return

        if self.check:
            self.changed += 1
            print(f"要整形: {relative}")
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.changed += 1
        print(f"整形完了: {relative}")

def format_definition(path: Path, format_states: bool, reporter: Reporter) -> None:
    if not path.exists():
        raise RuntimeError(f"対象ファイルがありません: {path.relative_to(ROOT)}")
    print(f"対象: {path.relative_to(ROOT)}")
    result = transform_definition(read_lines(path), format_states)
    reporter.write_lines(path, result)

def normalize_text_line_endings(reporter: Reporter) -> None:
    paths = {
        ROOT / ".gitattributes",
        ROOT / ".gitignore",
        ROOT / "AGENTS.md",
        ROOT / "Makefile",
        ROOT / "README.md",
    }
    paths.update((ROOT / "docs").rglob("*.md"))
    paths.update((ROOT / "scripts").glob("*.py"))

    for path in sorted(paths):
        if not path.exists():
            continue
        data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        reporter.write_bytes(path, data)


def verify_state_document_headings() -> None:
    documents = (
        "docs/state/default.md",
        "docs/state/attack.md",
        "docs/state/superattack.md",
        "docs/state/observ.md",
        "docs/state/helper.md",
        "docs/state/stcommon.md",
        "docs/state/explod-list.md",
    )
    for name in documents:
        has_behavior = False
        for number, line in enumerate(read_lines(ROOT / name), start=1):
            if line.startswith("## "):
                has_behavior = not line.startswith("## StateDef ")
                if not has_behavior:
                    raise RuntimeError(f"StateDefをH2に置けません: {name}:{number}")
            elif line.startswith("### StateDef "):
                if not has_behavior or not DOCUMENT_STATEDEF_PATTERN.match(line):
                    raise RuntimeError(f"StateDef見出しの階層が不正です: {name}:{number}")
    print("検証完了: ステート文書のH2/H3階層")


def verify_result() -> None:
    for name in DEFINITION_FILES:
        path = ROOT / name
        data = path.read_bytes()
        if b"\r" in data:
            raise RuntimeError(f"CRが残っています: {name}")

        for number, raw_line in enumerate(data.decode("latin-1").split("\n"), start=1):
            if raw_line.lstrip(" \t").startswith(";;"):
                continue

            if ";" in raw_line and raw_line != DIVIDER:
                raise RuntimeError(f"規約外コメントが残っています: {name}:{number}")

            if name in STATE_FORMAT_FILES and not SECTION_PATTERN.match(raw_line):
                quoted_value = "=" in raw_line and raw_line.split("=", 1)[1].lstrip().startswith('"')
                if quoted_value:
                    continue

                type_match = re.match(r"^type=(.+)$", raw_line, re.IGNORECASE)
                if type_match and type_match.group(1) != type_match.group(1).lower():
                    raise RuntimeError(f"type値に大文字が残っています: {name}:{number}")

                if OPERATOR_WITH_SPACES_PATTERN.search(raw_line):
                    normalized = OPERATOR_WITH_SPACES_PATTERN.sub(r"\1", raw_line)
                    if normalized != raw_line:
                        raise RuntimeError(f"演算子の前後に空白が残っています: {name}:{number}")

    verify_state_controller_types()
    verify_command_trigger_locations()
    verify_screenbound_locations()

    expected = {
        "cns/state.cns": lambda number: 0 <= number <= 9_999,
        "cns/observ.cns": lambda number: number in (-2, -3),
        "cns/helper.cns": lambda number: number >= 10_000,
    }
    for name, valid_number in expected.items():
        for line in read_lines(ROOT / name):
            number = statedef_number(line)
            if number is not None and not valid_number(number):
                raise RuntimeError(f"StateDefの配置が不正です: {name}:{number}")

    def_data = (ROOT / "tenkikai.def").read_text(encoding="ascii")

    inside_command_state = False
    for number, line in enumerate(read_lines(ROOT / "cns/command.cmd"), start=1):
        if CANONICAL_STATEDEF_PATTERN.match(line):
            inside_command_state = True
        elif not inside_command_state and " " in line:
            raise RuntimeError(f"CMD定義に半角スペースが残っています: cns/command.cmd:{number}")

    if " " in (ROOT / "cns/constants.cns").read_text(encoding="ascii"):
        raise RuntimeError("cns/constants.cnsに半角スペースが残っています")

    in_info = False
    for number, line in enumerate(def_data.splitlines(), start=1):
        if SECTION_PATTERN.match(line):
            in_info = line.lower() == "[info]"
        elif in_info and " " in line:
            raise RuntimeError(f"[Info]に半角スペースが残っています: tenkikai.def:{number}")

    verify_state_document_headings()
    print("検証完了: コメント、罫線、改行、StateDef配置、State Controller名、command Trigger配置、ScreenBound配置")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TENKIKAI definition formatter")
    parser.add_argument(
        "--check",
        action="store_true",
        help="ファイルを書き換えず、要整形ファイルがあれば失敗する",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("TENKIKAIフォーマッターを開始します")
    print("事前検証: State Controller名、command Trigger配置、ScreenBound配置")
    verify_state_controller_types()
    verify_command_trigger_locations()
    verify_screenbound_locations()
    reporter = Reporter(check=args.check)

    command_path = ROOT / "cns/command.cmd"
    print("対象: cns/command.cmd")
    command_lines = transform_definition(read_lines(command_path), format_states=True)
    command_lines = remove_ascii_spaces_from_command_definitions(command_lines)
    reporter.write_lines(command_path, command_lines)
    format_definition(ROOT / "cns/anim.air", format_states=False, reporter=reporter)
    format_definition(ROOT / "cns/state.cns", format_states=True, reporter=reporter)
    format_definition(ROOT / "cns/observ.cns", format_states=True, reporter=reporter)
    format_definition(ROOT / "cns/helper.cns", format_states=True, reporter=reporter)
    format_definition(ROOT / "cns/common1.cns", format_states=True, reporter=reporter)

    constants_path = ROOT / "cns/constants.cns"
    print("対象: cns/constants.cns")
    constants = transform_definition(read_lines(constants_path), format_states=True)
    reporter.write_lines(constants_path, remove_ascii_spaces(constants))

    def_path = ROOT / "tenkikai.def"
    print("対象: tenkikai.def")
    def_lines = transform_definition(read_lines(def_path), format_states=False)
    def_lines = remove_ascii_spaces_from_sections(def_lines, {"info"})
    reporter.write_lines(def_path, def_lines)

    print("対象: テキストファイルのLF統一")
    normalize_text_line_endings(reporter)
    verify_result()
    if args.check and reporter.changed:
        raise RuntimeError(f"要整形ファイルがあります: {reporter.changed}件")
    print(f"全処理完了: 変更ファイル数={reporter.changed}")


if __name__ == "__main__":
    main()
