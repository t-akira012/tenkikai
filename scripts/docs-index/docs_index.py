from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"


def document_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def readme_title(path: Path, directory_name: str) -> str:
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line
    return f"# {directory_name} 文書一覧"


def markdown_label(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


def generate_readme(directory: Path, check: bool = False) -> bool:
    readme = directory / "README.md"
    documents = sorted(
        (
            path
            for path in directory.glob("*.md")
            if path.name not in ("AGENTS.md", "README.md")
        ),
        key=lambda path: path.name.casefold(),
    )

    lines = [readme_title(readme, directory.name), ""]
    for document in documents:
        label = markdown_label(document_title(document))
        lines.append(f"- [{label}]({document.name})")
    content = "\n".join(lines).rstrip() + "\n"

    if readme.is_file() and readme.read_text(encoding="utf-8") == content:
        print(f"変更なし: {readme.relative_to(ROOT)}")
        return False

    if check:
        print(f"要更新: {readme.relative_to(ROOT)}")
        return True

    with readme.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
    print(f"更新: {readme.relative_to(ROOT)}")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate docs directory indexes")
    parser.add_argument(
        "--check",
        action="store_true",
        help="READMEを書き換えず、更新が必要なら失敗する",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directories = sorted(
        (path for path in DOCS.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )
    changed = 0
    for directory in directories:
        print(f"対象: {directory.relative_to(ROOT)}")
        if generate_readme(directory, check=args.check):
            changed += 1
    print(f"完了: {len(directories)}ディレクトリ、{changed}ファイル更新")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
