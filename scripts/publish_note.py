"""Publish a prepared lecture note (and its slide screenshots) into the Obsidian vault.

  python publish_note.py NOTE_MD "Lecture Notes/<course>/WEEK n.md" \
      --image SRC=weekN.P-topic-sNN.png|weekN-topic-anim-slug.svg [--image ...] \
      (--new | --baseline SAVED_COPY_OF_CURRENT_NOTE.md)

Safety rules:
  --new       the destination note must not exist yet.
  --baseline  the live note must still equal this saved copy (made right after you read it),
              so edits made in Obsidian meanwhile are never overwritten.
  An attachment name that already exists with different bytes is an error, never overwritten.
  OBSIDIAN_VAULT must be the vault open in Obsidian; a read error other than 404 aborts.
Every ![[...]] embed is checked before anything is written; afterwards the note is read back
through cli-anything-obsidian, and only then are the attachments copied.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VAULT = Path(os.environ["OBSIDIAN_VAULT"]) if os.environ.get("OBSIDIAN_VAULT") else None


def cli(*args):
    # The CLI talks to whichever vault Obsidian has open; main() checks that it is VAULT.
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    run = subprocess.run(["cli-anything-obsidian", "--json", *args],
                         capture_output=True, text=True, encoding="utf-8", env=env)
    try:
        data = json.loads(run.stdout) if run.stdout.strip() else {}
    except json.JSONDecodeError:
        data = {"error": run.stdout.strip() or run.stderr.strip()}
    if run.returncode != 0 and "error" not in data:
        data["error"] = run.stderr.strip() or f"exit {run.returncode}"
    return data


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fail(message):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("note_file")
    parser.add_argument("vault_path")
    parser.add_argument("--image", action="append", default=[], help="SRC=ATTACHMENT_NAME")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--new", action="store_true")
    mode.add_argument("--baseline")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if VAULT is None or not VAULT.is_dir():
        fail(f"set OBSIDIAN_VAULT to the vault folder (now {os.environ.get('OBSIDIAN_VAULT')!r})")
    vault_path = args.vault_path if args.vault_path.endswith(".md") else args.vault_path + ".md"
    body = Path(args.note_file).read_text(encoding="utf-8")
    attachments_dir = VAULT / Path(vault_path).parent / "attachments"

    # Attachments are copied on disk, the note goes through Obsidian: both must be the same vault.
    listing = cli("vault", "list")
    if listing.get("error"):
        fail(f"cannot reach Obsidian: {listing['error']}")
    on_disk = {p.name for p in VAULT.iterdir()}
    if not {f.rstrip("/") for f in listing.get("files", [])} <= on_disk:
        fail(f"the vault open in Obsidian is not OBSIDIAN_VAULT={VAULT}")

    current = cli("vault", "read", vault_path)
    if current.get("error") and "error 404" not in current["error"]:
        fail(f"cannot read {vault_path}: {current['error']}")  # never mistake an error for "absent"
    exists = "content" in current
    if args.new and exists:
        fail(f"{vault_path} already exists; read it, save a baseline copy and use --baseline")
    if args.baseline:
        if not exists:
            fail(f"{vault_path} does not exist; use --new")
        lf = lambda s: s.replace("\r\n", "\n")  # read_text() already turns CRLF into LF
        if lf(current["content"]) not in (lf(Path(args.baseline).read_text(encoding="utf-8")), lf(body)):
            fail(f"{vault_path} changed since the baseline was saved; re-read and merge first")

    plan = []
    for item in args.image:
        src, _, name = item.partition("=")
        if not name or not Path(src).is_file():
            fail(f"bad --image {item!r}")
        dest = attachments_dir / name
        if dest.exists() and digest(dest) != digest(src):
            fail(f"different attachment already exists: {dest}")
        plan.append((src, dest))
    incoming = {dest.name for _, dest in plan}
    missing = [e for e in re.findall(r"!\[\[([^\]|#]+)", body)
               if Path(e).name not in incoming and not (VAULT / e).exists()
               and not list(VAULT.rglob(Path(e).name))]
    if missing:
        fail(f"these embeds would not resolve (add them with --image): {missing}")

    if not exists:
        result = cli("vault", "create", vault_path, "--file", args.note_file)
    elif current["content"] != body:
        result = cli("vault", "update", vault_path, "--file", args.note_file)
    else:
        result = {}
    if result.get("error"):
        fail(f"write failed: {result['error']}")

    after = cli("vault", "read", vault_path)
    if after.get("content") != body:
        fail("saved content differs from the prepared note")

    attachments_dir.mkdir(parents=True, exist_ok=True)
    for src, dest in plan:
        if not dest.exists():
            shutil.copyfile(src, dest)

    print(json.dumps({
        "ok": True,
        "note": vault_path,
        "action": "created" if not exists else ("updated" if current["content"] != body else "unchanged"),
        "chars": len(body),
        "attachments": [str(d) for _, d in plan],
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
