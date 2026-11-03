from pathlib import Path

PAGES = Path("src/modules/ROOT/pages")
NAV_FILE = Path("src/modules/ROOT/nav.adoc")
SECTIONS = ["UCAiug", "61850ug", "CIMug", "OpenFMBug"]


def label_from_name(name: str) -> str:
    return name.replace("_", " ").replace("-", " ")


def xref_target(page: Path) -> str:
    # Keep ".adoc" in the xref target.
    return page.relative_to(PAGES).as_posix()


def write_folder(folder: Path, depth: int, lines: list[str]) -> None:
    landing = folder / f"{folder.name}.adoc"

    if landing.is_file():
        lines.append(
            f'{"*" * depth} xref:{xref_target(landing)}'
            f'[{label_from_name(folder.name)}]'
        )
        child_depth = depth + 1
    else:
        lines.append(f'{"*" * depth} {label_from_name(folder.name)}')
        child_depth = depth + 1

    # Include .adoc files directly in this folder, except its landing page.
    for page in sorted(folder.glob("*.adoc"), key=lambda p: p.name.casefold()):
        if page == landing:
            continue
        lines.append(
            f'{"*" * child_depth} xref:{xref_target(page)}'
            f'[{label_from_name(page.stem)}]'
        )

    # Recurse into subfolders.
    for subfolder in sorted(
        (p for p in folder.iterdir() if p.is_dir()),
        key=lambda p: p.name.casefold(),
    ):
        write_folder(subfolder, child_depth, lines)


def main() -> None:
    lines = ["* xref:index.adoc[UCAiug]"]

    for section in SECTIONS:
        folder = PAGES / section
        if folder.is_dir():
            write_folder(folder, depth=2, lines=lines)

    NAV_FILE.parent.mkdir(parents=True, exist_ok=True)
    NAV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {NAV_FILE}")


if __name__ == "__main__":
    main()
