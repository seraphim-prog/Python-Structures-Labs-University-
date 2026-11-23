"""Фіксація та перевірка точного набору залежностей двох середовищ."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
BOOTSTRAP = {"pip", "setuptools", "wheel", "distribute"}
PIN = re.compile(r"([a-zA-Z0-9_.-]+)==([^\s;#]+)")


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def env_python(name: str) -> Path:
    relative = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    return ROOT / name / relative


def get_installed_packages(executable: str | Path = sys.executable) -> list[dict]:
    result = subprocess.run(
        [str(executable), "-m", "pip", "list", "--format=json"],
        capture_output=True, encoding="utf-8", check=True,
    )
    packages = json.loads(result.stdout)
    return [pkg for pkg in packages if normalize(pkg["name"]) not in BOOTSTRAP]


def generate_requirements(packages: list[dict], filename: Path) -> None:
    ordered = sorted(packages, key=lambda package: normalize(package["name"]))
    pins = [f'{package["name"]}=={package["version"]}' for package in ordered]
    filename.write_text("\n".join(pins) + "\n", encoding="utf-8")


def read_requirements(filename: Path) -> dict[str, str]:
    pins = {}
    for number, raw in enumerate(filename.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN.fullmatch(line)
        if not match:
            raise ValueError(f"Рядок {number}: очікувався запис назва==версія.")
        name, release = match.groups()
        key = normalize(name)
        if key in pins:
            raise ValueError(f"Рядок {number}: повтор пакета {name}.")
        pins[key] = release
    return pins


def verify_requirements(filename: Path, executable: Path = Path(sys.executable)) -> bool:
    expected = read_requirements(filename)
    installed = {
        normalize(pkg["name"]): pkg["version"] for pkg in get_installed_packages(executable)
    }
    differences = [
        (name, expected.get(name, "відсутній"), installed.get(name, "відсутній"))
        for name in sorted(expected.keys() | installed.keys())
        if expected.get(name) != installed.get(name)
    ]
    print(f"{executable.parent.parent.name}: {len(installed)} пакетів")
    for name, locked, found in differences:
        print(f"  {name}: зафіксовано {locked}, встановлено {found}")
    return not differences


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requirements", type=Path, default=ROOT / "requirements.txt")
    parser.add_argument("--generate", action="store_true", help="Записати версії з поточного Python.")
    options = parser.parse_args()
    filename = options.requirements
    try:
        if options.generate:
            packages = get_installed_packages()
            generate_requirements(packages, filename)
            print(f"Створено {filename.name}: {len(packages)} точних версій.")
            return 0
        if not filename.is_file():
            print(f"Файл {filename.name} не знайдено. Створи його в першому середовищі.")
            return 1

        print(f"Поточний інтерпретатор: {sys.executable}")
        print(f"Зафіксовано версій у {filename.name}: {len(read_requirements(filename))}")
        matches = []
        for name in ("venv", "venv2"):
            interpreter = env_python(name)
            if not interpreter.is_file():
                print(f"Середовище {name} відсутнє. Створи його командою python -m venv {name}.")
                return 1
            matches.append(verify_requirements(filename, interpreter))
        identical = all(matches)
        if identical:
            print("[OK] venv і venv2 відтворюють той самий набір пакетів і версій.")
        else:
            print("[УВАГА] Знайдено розбіжності з requirements.txt.")
        return 0 if identical else 1
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Помилка перевірки середовища: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
