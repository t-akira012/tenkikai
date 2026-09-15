from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIVIDER = ";" + "-" * 49

STATEDEF_PATTERN = re.compile(r"^\s*\[statedef\s+(-?\d+)\s*\]\s*$", re.IGNORECASE)
STATE_PATTERN = re.compile(r"^\s*\[state(?:\s+[^\]]*)?\]\s*$", re.IGNORECASE)
SECTION_PATTERN = re.compile(r"^\s*\[[^\]]+\]\s*$")
CANONICAL_STATEDEF_PATTERN = re.compile(r"^\[statedef\s+(-?\d+)\]$")
OPERATOR_WITH_SPACES_PATTERN = re.compile(
    r"[ \t]*(\*\*|&&|\|\||\^\^|:=|!=|>=|<=|[=<>+\-*/%&|^])[ \t]*"
)

DEFINITION_FILES = (
    "tenkikai.def",
    "binary/animation.air",
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


def read_lines(path: Path) -> list[str]:
    data = path.read_bytes()
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data.decode("latin-1").split("\n")


def encoded_lines(lines: list[str]) -> bytes:
    return ("\n".join(lines) + "\n").encode("latin-1")


def is_divider_comment(line: str) -> bool:
    stripped = line.lstrip(" \t")
    return stripped.startswith((";-", ";="))


def strip_comments(lines: list[str], keep_dividers: bool = True) -> list[str]:
    result: list[str] = []

    for source_line in lines:
        line = source_line.rstrip(" \t")
        stripped = line.lstrip(" \t")

        if stripped.startswith(";"):
            if keep_dividers and is_divider_comment(stripped):
                result.append(DIVIDER)
            continue

        comment_at = line.find(";")
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

        if inside_state and line:
            line = line.strip()
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


def remove_ascii_spaces(lines: list[str]) -> list[str]:
    return [line.replace(" ", "") for line in lines]


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
            result.append(line.replace(" ", ""))
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
            result.append(line.replace(" ", ""))

    return result


def ensure_state_spacing(lines: list[str]) -> list[str]:
    result: list[str] = []

    for line in lines:
        if (CANONICAL_STATEDEF_PATTERN.match(line) or line == "[state ]") and result and result[-1]:
            result.append("")
        result.append(line)

    return normalize_blank_lines(result)


def semantic_lines(lines: list[str], format_states: bool) -> list[str]:
    lines = strip_comments(lines, keep_dividers=False)
    if format_states:
        lines = canonicalize_states(lines)
    return [line for line in lines if line]


def transform_definition(lines: list[str], format_states: bool) -> list[str]:
    before = semantic_lines(lines, format_states)
    result = strip_comments(lines)
    if format_states:
        result = canonicalize_states(result)
    result = normalize_blank_lines(result)
    if format_states:
        result = ensure_state_spacing(result)
    after = semantic_lines(result, format_states)

    if before != after:
        raise RuntimeError("整形によって有効な定義が変化しました")

    return result


def statedef_number(line: str) -> int | None:
    match = CANONICAL_STATEDEF_PATTERN.match(line)
    if not match:
        return None
    return int(match.group(1))


def split_cns(lines: list[str]) -> tuple[list[str], list[str], list[str], list[str]]:
    header_indexes = [index for index, line in enumerate(lines) if statedef_number(line) is not None]
    if not header_indexes:
        raise RuntimeError("旧t.cnsにStateDefがありません")

    starts: list[int] = []
    for header_index in header_indexes:
        start_index = header_index
        while start_index > 0 and lines[start_index - 1] in ("", DIVIDER):
            start_index -= 1
        starts.append(start_index)

    constants = lines[: starts[0]]
    states: list[str] = []
    observers: list[str] = []
    helpers: list[str] = []

    for index, header_index in enumerate(header_indexes):
        finish_index = starts[index + 1] if index + 1 < len(starts) else len(lines)
        chunk = lines[starts[index] : finish_index]
        number = statedef_number(lines[header_index])

        if number in (-2, -3):
            observers.extend(chunk)
        elif number is not None and number >= 10_000:
            helpers.extend(chunk)
        elif number is not None and 0 <= number <= 9_999:
            states.extend(chunk)
        else:
            raise RuntimeError(f"分類できないStateDefです: {number}")

    return tuple(
        normalize_blank_lines(group)
        for group in (constants, states, observers, helpers)
    )


def remove_duplicate_common_states(
    common_lines: list[str], other_state_numbers: set[int]
) -> tuple[list[str], list[int]]:
    header_indexes = [
        index for index, line in enumerate(common_lines) if statedef_number(line) is not None
    ]
    if not header_indexes:
        raise RuntimeError("common1.cnsにStateDefがありません")

    starts: list[int] = []
    for header_index in header_indexes:
        start_index = header_index
        while start_index > 0 and common_lines[start_index - 1] in ("", DIVIDER):
            start_index -= 1
        starts.append(start_index)

    result = common_lines[: starts[0]]
    removed: list[int] = []

    for index, header_index in enumerate(header_indexes):
        finish_index = starts[index + 1] if index + 1 < len(starts) else len(common_lines)
        chunk = common_lines[starts[index] : finish_index]
        number = statedef_number(common_lines[header_index])

        if number in other_state_numbers:
            removed.append(number)
        else:
            result.extend(chunk)

    return normalize_blank_lines(result), removed


def update_def(lines: list[str]) -> list[str]:
    output: list[str] = []
    in_files = False

    for line in lines:
        if line.lower() == "[files]":
            in_files = True
            output.append("[Files]")
            continue

        if in_files and SECTION_PATTERN.match(line):
            in_files = False

        if in_files:
            key_match = re.match(r"^\s*([A-Za-z0-9.]+)\s*=\s*(.*?)\s*$", line)
            if key_match:
                key = key_match.group(1)
                value = key_match.group(2)
                key_lower = key.lower()

                if key_lower == "cmd":
                    output.append("cmd=cns/command.cmd")
                elif key_lower == "cns":
                    output.append("cns=cns/constants.cns")
                elif key_lower == "st":
                    output.extend(("st=cns/state.cns", "st1=cns/observ.cns", "st2=cns/helper.cns"))
                elif key_lower in ("st1", "st2"):
                    continue
                elif key_lower == "stcommon":
                    output.append("stcommon=cns/common1.cns")
                elif key_lower == "sprite":
                    output.append("sprite=binary/sprite.sff")
                elif key_lower == "anim":
                    output.append("anim=binary/animation.air")
                elif key_lower == "sound":
                    output.append("sound=binary/sound.snd")
                elif re.fullmatch(r"pal[1-6]", key_lower):
                    output.append(f"{key_lower}=binary/{key_lower}.act")
                else:
                    output.append(f"{key}={value}")
                continue

        output.append(line)

    return normalize_blank_lines(output)


class Reporter:
    def __init__(self) -> None:
        self.changed = 0

    def write_lines(self, path: Path, lines: list[str]) -> None:
        self.write_bytes(path, encoded_lines(lines))

    def write_bytes(self, path: Path, data: bytes) -> None:
        old_data = path.read_bytes() if path.exists() else None
        relative = path.relative_to(ROOT)

        if old_data == data:
            print(f"変更なし: {relative}")
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.changed += 1
        print(f"整形完了: {relative}")


def format_legacy_cns(reporter: Reporter) -> None:
    legacy_path = ROOT / "t.cns"
    if not legacy_path.exists():
        return

    print("対象: 旧t.cnsの分割")
    original = read_lines(legacy_path)
    transformed = transform_definition(original, format_states=True)
    constants, states, observers, helpers = split_cns(transformed)

    combined = constants + states + helpers + observers
    if semantic_lines(original, True) != semantic_lines(combined, True):
        raise RuntimeError("t.cnsの分割によって有効な定義が変化しました")

    reporter.write_lines(ROOT / "cns/constants.cns", constants)
    reporter.write_lines(ROOT / "cns/state.cns", states)
    reporter.write_lines(ROOT / "cns/observ.cns", observers)
    reporter.write_lines(ROOT / "cns/helper.cns", helpers)
    legacy_path.unlink()
    reporter.changed += 1
    print("削除完了: t.cns")


def format_definition(path: Path, format_states: bool, reporter: Reporter) -> None:
    if not path.exists():
        raise RuntimeError(f"対象ファイルがありません: {path.relative_to(ROOT)}")
    print(f"対象: {path.relative_to(ROOT)}")
    result = transform_definition(read_lines(path), format_states)
    reporter.write_lines(path, result)


def format_common_states(reporter: Reporter) -> None:
    path = ROOT / "cns/common1.cns"
    if not path.exists():
        raise RuntimeError("対象ファイルがありません: cns/common1.cns")

    print("対象: cns/common1.cns")
    result = transform_definition(read_lines(path), format_states=True)
    other_names = ("cns/command.cmd", "cns/state.cns", "cns/observ.cns", "cns/helper.cns")
    other_state_numbers = {
        number
        for name in other_names
        for line in read_lines(ROOT / name)
        if (number := statedef_number(line)) is not None
    }
    result, removed = remove_duplicate_common_states(result, other_state_numbers)

    for number in removed:
        print(f"重複削除: cns/common1.cns StateDef {number}")
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


def verify_result() -> None:
    for name in DEFINITION_FILES:
        path = ROOT / name
        data = path.read_bytes()
        if b"\r" in data:
            raise RuntimeError(f"CRが残っています: {name}")

        for number, raw_line in enumerate(data.decode("latin-1").split("\n"), start=1):
            if ";" in raw_line and raw_line != DIVIDER:
                raise RuntimeError(f"規約外コメントが残っています: {name}:{number}")

            if name in STATE_FORMAT_FILES and not SECTION_PATTERN.match(raw_line):
                type_match = re.match(r"^type=(.+)$", raw_line, re.IGNORECASE)
                if type_match and type_match.group(1) != type_match.group(1).lower():
                    raise RuntimeError(f"type値に大文字が残っています: {name}:{number}")

                if OPERATOR_WITH_SPACES_PATTERN.search(raw_line):
                    normalized = OPERATOR_WITH_SPACES_PATTERN.sub(r"\1", raw_line)
                    if normalized != raw_line:
                        raise RuntimeError(f"演算子の前後に空白が残っています: {name}:{number}")

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

    common_numbers = {
        number
        for line in read_lines(ROOT / "cns/common1.cns")
        if (number := statedef_number(line)) is not None
    }
    other_numbers = {
        number
        for name in ("cns/command.cmd", "cns/state.cns", "cns/observ.cns", "cns/helper.cns")
        for line in read_lines(ROOT / name)
        if (number := statedef_number(line)) is not None
    }
    duplicates = sorted(common_numbers & other_numbers)
    if duplicates:
        raise RuntimeError(f"cns/common1.cnsに重複StateDefがあります: {duplicates}")

    def_data = (ROOT / "tenkikai.def").read_text(encoding="ascii")
    required = (
        "cmd=cns/command.cmd",
        "cns=cns/constants.cns",
        "st=cns/state.cns",
        "st1=cns/observ.cns",
        "st2=cns/helper.cns",
        "stcommon=cns/common1.cns",
        "sprite=binary/sprite.sff",
        "anim=binary/animation.air",
        "sound=binary/sound.snd",
        "pal1=binary/pal1.act",
        "pal2=binary/pal2.act",
        "pal3=binary/pal3.act",
        "pal4=binary/pal4.act",
        "pal5=binary/pal5.act",
        "pal6=binary/pal6.act",
    )
    for line in required:
        if def_data.splitlines().count(line) != 1:
            raise RuntimeError(f"DEF参照が不正です: {line}")
        referenced_path = ROOT / line.split("=", 1)[1]
        if not referenced_path.is_file():
            raise RuntimeError(f"DEF参照先がありません: {referenced_path.relative_to(ROOT)}")

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

    print("検証完了: コメント、罫線、改行、StateDef配置、DEF参照")


def main() -> None:
    print("TENKIKAIフォーマッターを開始します")
    reporter = Reporter()

    format_legacy_cns(reporter)
    command_path = ROOT / "cns/command.cmd"
    print("対象: cns/command.cmd")
    command_lines = transform_definition(read_lines(command_path), format_states=True)
    command_lines = remove_ascii_spaces_from_command_definitions(command_lines)
    reporter.write_lines(command_path, command_lines)
    format_definition(ROOT / "binary/animation.air", format_states=False, reporter=reporter)
    format_definition(ROOT / "cns/state.cns", format_states=True, reporter=reporter)
    format_definition(ROOT / "cns/observ.cns", format_states=True, reporter=reporter)
    format_definition(ROOT / "cns/helper.cns", format_states=True, reporter=reporter)
    format_common_states(reporter)

    constants_path = ROOT / "cns/constants.cns"
    print("対象: cns/constants.cns")
    constants = transform_definition(read_lines(constants_path), format_states=True)
    reporter.write_lines(constants_path, remove_ascii_spaces(constants))

    def_path = ROOT / "tenkikai.def"
    print("対象: tenkikai.def")
    def_lines = transform_definition(read_lines(def_path), format_states=False)
    def_lines = update_def(def_lines)
    def_lines = remove_ascii_spaces_from_sections(def_lines, {"info"})
    reporter.write_lines(def_path, def_lines)

    print("対象: テキストファイルのLF統一")
    normalize_text_line_endings(reporter)
    verify_result()
    print(f"全処理完了: 変更ファイル数={reporter.changed}")


if __name__ == "__main__":
    main()
