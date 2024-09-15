import argparse as ap
import sys
from collections.abc import Sequence
from pathlib import Path

__version__: str = "0.1.0"
DEFAULT_PATH: Path = Path(".")


def preview_entry(entry: Path, entry_prefix: str, prefix: str, lines: list[str], sort_entries: bool):
	if entry.is_file():
		lines.append("%s%s" % (entry_prefix, entry.name))
		return

	lines.append("%s%s/" % (entry_prefix, entry.name))
	lines += preview_tree(entry, prefix, sort_entries)


def preview_tree(path: Path, prefix: str = "", sort_entries: bool = False, lines: list[str] | None = None) -> list[str]:
	if lines is None:
		lines = []

	entries = [key for key in path.iterdir()]
	if sort_entries:
		entries = sorted(entries)

	if not entries:
		return lines

	first_entries, last_entry = entries[:-1], entries[-1]

	for entry in first_entries:
		preview_entry(entry, "├─ ", "│  ", lines, sort_entries)
	preview_entry(last_entry, "└─ ", "   ", lines, sort_entries)

	for idx, line in enumerate(lines):
		lines[idx] = prefix + line

	return lines


def tree(path: Path, sort_entries: bool = False) -> list[str]:
	lines: list[str] = []
	preview_entry(path, "", "", lines, sort_entries)
	return lines


def init_parser() -> ap.ArgumentParser:
	parser = ap.ArgumentParser()
	parser.add_argument("-v", "--version", help="print script version", action="store_true")
	parser.add_argument("-s", "--sort", help="sort tree entries", action="store_true")
	parser.add_argument(
		"path",
		help=f"path to preview as a tree structure (defaults to '{DEFAULT_PATH}')",
		nargs="?",
		type=Path,
		default=DEFAULT_PATH,
	)
	return parser


def main(args: Sequence[str] | None) -> int:
	parser = init_parser()
	ns = parser.parse_args(args)
	if ns.version:
		print(__version__)
		return 0

	path: Path = ns.path
	lines = tree(path, ns.sort)
	view = "\n".join(lines)
	print(view)
	return 0


if __name__ == "__main__":
	exit(main(sys.argv[1:]))
