"""Дерева вихідних файлів та порівняння структури Django і Flask."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent
IGNORED_NAMES = {"__pycache__", "venv", "venv2", "instance", "Thumbs.db"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".sqlite3", ".db"}


def walk_tree(path: Path, prefix: str = ""):
    # Спільний обхід для дерева й статистики з однаковими правилами відбору.
    entries = sorted(
        (entry for entry in path.iterdir()
         if not entry.is_symlink()
         and not entry.name.startswith(".")
         and entry.name not in IGNORED_NAMES
         and not entry.name.startswith("db.sqlite3-")
         and entry.suffix not in IGNORED_SUFFIXES),
        key=lambda entry: (not entry.is_dir(), entry.name.casefold(), entry.name),
    )
    for index, entry in enumerate(entries):
        last = index == len(entries) - 1
        folder = entry.is_dir()
        suffix = "/" if folder else ""
        yield entry, prefix + ("└── " if last else "├── ") + entry.name + suffix
        if folder:
            yield from walk_tree(entry, prefix + ("    " if last else "│   "))


def scan_directory(path: Path, prefix: str = "") -> list[str]:
    return [branch for _, branch in walk_tree(path, prefix)]


def analyze_project(path: Path) -> dict:
    stats = {"py_files": 0, "html_files": 0, "css_files": 0, "total_size": 0, "directories": []}
    keys = {".py": "py_files", ".html": "html_files", ".css": "css_files"}
    for entry, _ in walk_tree(path):
        if entry.is_dir():
            stats["directories"].append(entry.relative_to(path).as_posix())
        elif entry.is_file():
            stats["total_size"] += entry.stat().st_size
            if entry.suffix in keys:
                stats[keys[entry.suffix]] += 1
    return stats


def compare_projects(django_path: Path, flask_path: Path) -> None:
    for framework, path in (("Django", django_path), ("Flask", flask_path)):
        print(f"{framework} · {path.name}/")
        print("\n".join(scan_directory(path)))
        print()

    django = analyze_project(django_path)
    flask = analyze_project(flask_path)
    rows = [
        ("Файли .py", django["py_files"], flask["py_files"]),
        ("Файли .html", django["html_files"], flask["html_files"]),
        ("Файли .css", django["css_files"], flask["css_files"]),
        ("Каталоги", len(django["directories"]), len(flask["directories"])),
        ("Розмір, байт", django["total_size"], flask["total_size"]),
    ]
    print(f"{'Характеристика':<19} | {'Django':>8} | {'Flask':>8}")
    print("-" * 41)
    for label, first, second in rows:
        print(f"{label:<19} | {first:>8} | {second:>8}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--django", type=Path, default=ROOT / "mysite")
    parser.add_argument("--flask", type=Path, default=ROOT / "myflaskapp")
    options = parser.parse_args()
    for path in (options.django, options.flask):
        if not path.is_dir():
            print(f"Каталог {path} не знайдено.")
            return 1
    try:
        compare_projects(options.django, options.flask)
    except OSError as error:
        print(f"Не вдалося прочитати структуру: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
