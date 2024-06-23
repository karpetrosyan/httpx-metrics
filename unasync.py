#!venv/bin/python
import os
import re
import sys

SUBS = [
    ("async def", "def"),
    ("await ", ""),
    ("Async([A-Z][A-Za-z0-9_]*)", r"\2"),
    ("aclose", "close"),
    ("handle_async_request", "handle_request"),
    ("_async.metrics", "_sync.metrics"),
]
COMPILED_SUBS = [
    (re.compile(r"(^|\b)" + regex + r"($|\b)"), repl) for regex, repl in SUBS
]

USED_SUBS = set()


def unasync_line(line):
    for index, (regex, repl) in enumerate(COMPILED_SUBS):
        old_line = line
        line = re.sub(regex, repl, line)
        if index not in USED_SUBS:
            if line != old_line:
                USED_SUBS.add(index)
    return line


def unasync_file(in_path, out_path):
    with open(in_path) as in_file:
        with open(out_path, "w", newline="") as out_file:
            for line in in_file.readlines():
                line = unasync_line(line)
                out_file.write(line)


def unasync_file_check(in_path, out_path):
    with open(in_path) as in_file:
        with open(out_path) as out_file:
            for in_line, out_line in zip(in_file.readlines(), out_file.readlines()):
                expected = unasync_line(in_line)
                if out_line != expected:
                    print(f"unasync mismatch between {in_path!r} and {out_path!r}")
                    print(f"Async code:         {in_line!r}")
                    print(f"Expected sync code: {expected!r}")
                    print(f"Actual sync code:   {out_line!r}")
                    sys.exit(1)


def unasync_dir(in_dir, out_dir, check_only=False):
    for dirpath, dirnames, filenames in os.walk(in_dir):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            rel_dir = os.path.relpath(dirpath, in_dir)
            in_path = os.path.normpath(os.path.join(in_dir, rel_dir, filename))
            out_path = os.path.normpath(os.path.join(out_dir, rel_dir, filename))
            print(in_path, "->", out_path)
            if check_only:
                unasync_file_check(in_path, out_path)
            else:
                unasync_file(in_path, out_path)


def main():
    check_only = "--check" in sys.argv
    unasync_dir("httpx_metrics/_async", "httpx_metrics/_sync", check_only=check_only)
    unasync_dir("tests/_async", "tests/_sync", check_only=check_only)
    unasync_file("httpx_metrics/async_metrics.py", "httpx_metrics/sync_metrics.py")

    if len(USED_SUBS) != len(SUBS):
        unused_subs = [SUBS[i] for i in range(len(SUBS)) if i not in USED_SUBS]

        from pprint import pprint

        print("This SUBS was not used")
        pprint(unused_subs)
        exit(1)


if __name__ == "__main__":
    main()
