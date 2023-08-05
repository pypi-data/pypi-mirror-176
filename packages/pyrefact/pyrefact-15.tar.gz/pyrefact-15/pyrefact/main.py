#!/usr/bin/env python3
import argparse
import ast
import collections
import os
import sys
from pathlib import Path
from typing import Collection, Iterable, Sequence

from . import abstractions, completion, fixes, parsing


def _parse_args(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help="Paths to refactor", type=Path, nargs="+", default=())
    parser.add_argument(
        "--preserve",
        help="Paths to preserve names in",
        type=Path,
        nargs="+",
        default=(),
    )
    return parser.parse_args(args)


def run_pyrefact(filename: Path, preserve: Collection[str] = frozenset()) -> int:
    """Fix a file.

    Args:
        filename (Path): File to fix

    Returns:
        int: 0 if successful
    """
    with open(filename, "r", encoding="utf-8") as stream:
        initial_content = content = stream.read()

    if not parsing.is_valid_python(content):
        content = completion.autocomplete(content)

    content = fixes.fix_rmspace(content)

    if not parsing.is_valid_python(content):
        print("Result is not valid python.")
        return 0

    content = fixes.delete_unreachable_code(content)
    content = fixes.undefine_unused_variables(content, preserve=preserve)
    content = fixes.delete_pointless_statements(content)
    content = fixes.delete_unused_functions_and_classes(content, preserve=preserve)

    if tuple(sys.version_info) >= (3, 9):
        content = fixes.replace_with_sets(content)
        content = fixes.remove_redundant_chained_calls(content)
        content = fixes.move_imports_to_toplevel(content)
        content = abstractions.create_abstractions(content)

    content = fixes.align_variable_names_with_convention(content, preserve=preserve)

    content = fixes.fix_black(content)
    content = fixes.fix_isort(content, line_length=10_000)
    content = fixes.define_undefined_variables(content)
    content = fixes.remove_unused_imports(content)
    content = fixes.fix_isort(content)
    content = fixes.fix_black(content)
    content = fixes.fix_rmspace(content)

    if content != initial_content and (
        parsing.is_valid_python(content) or not parsing.is_valid_python(initial_content)
    ):
        with open(filename, "w", encoding="utf-8") as stream:
            stream.write(content)

    return 0


def _iter_python_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from path.rglob("*.py")
        else:
            raise FileNotFoundError(f"Not found: {path}")


def _namespace_name(filename: Path) -> str:
    filename = Path(filename).absolute()
    return str(filename).replace(os.path.sep, ".")


def main(args: Sequence[str]) -> int:
    """Parse command-line arguments and run pyrefact on provided files.

    Args:
        args (Sequence[str]): sys.argv[1:]

    Returns:
        int: 0 if successful.

    """
    args = _parse_args(args)

    return_code = 0
    count = 0
    used_names = collections.defaultdict(set)
    for filename in _iter_python_files(args.preserve):
        with open(filename, "r", encoding="utf-8") as stream:
            content = stream.read()
        ast_root = ast.parse(content)
        imported_names = parsing.get_imported_names(ast_root)
        for node in ast.walk(ast_root):
            if isinstance(node, ast.Name) and node.id in imported_names:
                used_names[_namespace_name(filename)].add(node.id)
            elif (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in imported_names
            ):
                used_names[_namespace_name(filename)].add(node.attr)
                used_names[_namespace_name(filename)].add(node.value.id)

    for filename in _iter_python_files(args.paths):
        count += 1
        preserve = set()
        for name, variables in used_names.items():
            if name != _namespace_name(filename):
                preserve.update(variables)
        code = run_pyrefact(filename, preserve=frozenset(preserve))
        if code != 0:
            print(f"pyrefact failed for filename {filename}")
            return_code = max(return_code, code)

    if count == 0:
        print("No files provided")
        return 1

    return return_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
