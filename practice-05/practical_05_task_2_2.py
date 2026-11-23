"""Читання налаштувань та три базові перевірки Django через AST."""

import argparse
import ast
from pathlib import Path


DEFAULT_SETTINGS = Path(__file__).resolve().parent / "mysite" / "mysite" / "settings.py"


def read_assignments(path: Path) -> dict[str, ast.expr]:
    # Розбираємо текст, не імпортуючи й не виконуючи settings.py.
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    values = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    values[target.id] = statement.value
        if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            if statement.value is not None:
                values[statement.target.id] = statement.value
    return values


def literal(node):
    if node is not None:
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError):
            pass
    return None


def get_dict_entry(node, key):
    if isinstance(node, ast.Dict):
        for index, name in enumerate(node.keys):
            if literal(name) == key:
                return node.values[index]
    return None


def analyze_settings(values: dict[str, ast.expr]) -> dict:
    database = get_dict_entry(values.get("DATABASES"), "default")
    return {
        "DEBUG": literal(values.get("DEBUG")),
        "LANGUAGE_CODE": literal(values.get("LANGUAGE_CODE")),
        "TIME_ZONE": literal(values.get("TIME_ZONE")),
        "DATABASES": literal(get_dict_entry(database, "ENGINE")),
        "TEMPLATES": literal(values.get("TEMPLATES")) or [],
        "MIDDLEWARE": literal(values.get("MIDDLEWARE")) or [],
        "INSTALLED_APPS": literal(values.get("INSTALLED_APPS")) or [],
    }


def secret_source(node) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return "літерал у коді"
    if isinstance(node, ast.Subscript) and ast.unparse(node.value) == "os.environ":
        return "змінна середовища"
    if isinstance(node, ast.Call):
        name = ast.unparse(node.func)
        if name in ("os.environ.get", "os.getenv"):
            defaults = node.args[1:2] + [kw.value for kw in node.keywords if kw.arg == "default"]
            if any(secret_source(value) == "літерал у коді" for value in defaults):
                return "літерал у коді"
            return "змінна середовища"
        if name in ("get_random_secret_key", "secrets.token_urlsafe"):
            return "випадково генерується"
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        sources = [secret_source(option) for option in node.values]
        if "літерал у коді" in sources:
            return "літерал у коді"
        if "потребує перевірки" not in sources:
            return " або ".join(dict.fromkeys(sources))
    return "потребує перевірки"


def check_security(values: dict[str, ast.expr]) -> list[tuple[bool, str]]:
    debug = literal(values.get("DEBUG"))
    source = secret_source(values.get("SECRET_KEY"))
    hosts = literal(values.get("ALLOWED_HOSTS"))
    return [
        (debug is False, f"DEBUG = {debug} (True використовують для локальної розробки)."),
        (source not in ("літерал у коді", "потребує перевірки"), f"SECRET_KEY: {source}."),
        (isinstance(hosts, (list, tuple)) and bool(hosts), f"ALLOWED_HOSTS: {hosts}."),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_SETTINGS)
    args = parser.parse_args()
    try:
        values = read_assignments(args.path)
    except (OSError, SyntaxError) as error:
        print(f"Не вдалося прочитати {args.path.name}: {error}")
        return 1
    settings = analyze_settings(values)
    print("Налаштування Django · settings.py")
    for key in ("DEBUG", "LANGUAGE_CODE", "TIME_ZONE", "DATABASES"):
        print(f"{key}: {settings[key]}")
    for template in settings["TEMPLATES"]:
        print(f"TEMPLATES: {template.get('BACKEND')}, APP_DIRS = {template.get('APP_DIRS')}")
    print(f"MIDDLEWARE: {len(settings['MIDDLEWARE'])} компонентів")
    print(f"INSTALLED_APPS: {len(settings['INSTALLED_APPS'])} додатків")
    for app in settings["INSTALLED_APPS"]:
        print(f"  {app}")
    print("\nБазові правила")
    checks = check_security(values)
    for passed, message in checks:
        print(f"[{'OK' if passed else 'УВАГА'}] {message}")
    print(f"Попереджень: {sum(not passed for passed, _ in checks)} з {len(checks)} перевірок.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
