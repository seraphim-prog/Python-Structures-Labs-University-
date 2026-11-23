"""Перевірка інтерпретатора та встановлення Django і Flask."""

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
import sys


def check_package(module_name: str, distribution: str) -> bool:
    try:
        installed_version = version(distribution)
        import_module(module_name)
    except PackageNotFoundError:
        print(f"[УВАГА] {distribution} відсутній.")
        return False
    except ImportError as error:
        print(f"[УВАГА] {distribution} встановлено, але імпорт не вдався ({error}).")
        return False
    print(f"[OK] {distribution} {installed_version}")
    return True


def main() -> int:
    release = sys.version_info
    print(f"Python {release.major}.{release.minor}.{release.micro}")
    print(f"Інтерпретатор: {sys.executable}")
    in_venv = sys.prefix != sys.base_prefix
    print(f"Віртуальне середовище: {'активне для цього Python' if in_venv else 'не використовується'}")
    if release < (3, 10):
        print("[УВАГА] Потрібен Python 3.10 або новіший.")
        return 1

    packages = (("django", "Django"), ("flask", "Flask"))
    results = [check_package(module, name) for module, name in packages]
    installed = sum(results)
    print(f"Доступно фреймворків: {installed} з {len(packages)}")
    if not all(results):
        print("Команда встановлення: python -m pip install -r requirements.txt")
    return 0 if in_venv and all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
