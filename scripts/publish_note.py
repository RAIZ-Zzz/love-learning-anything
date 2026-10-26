"""Publish a prepared lecture note (and its slide screenshots) into the Obsidian vault.

  python publish_note.py NOTE_MD "Lecture Notes/<course>/WEEK n.md" \
      --image SRC=weekN.P-topic-sNN.png|weekN-topic-anim-slug.svg [--image ...] \
      (--new | --baseline SAVED_COPY_OF_CURRENT_NOTE.md)

Writes straight to the vault folder on disk (OBSIDIAN_VAULT); Obsidian picks up the change itself.
Safety rules:
  --new       the destination note must not exist yet.
  --baseline  the note on disk must still equal this saved copy (made right after you read it),
              so edits made in Obsidian meanwhile are never overwritten.
  An attachment name that already exists with different bytes is an error, never overwritten.
Every ![[...]] embed is checked before anything is written; the note is written atomically and
read back, and only then are the attachments copied.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

VAULT = Path(os.environ["OBSIDIAN_VAULT"]) if os.environ.get("OBSIDIAN_VAULT") else None


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

    if VAULT is None or not (VAULT / ".obsidian").is_dir():
        fail(f"set OBSIDIAN_VAULT to the vault folder, the one holding .obsidian/ (now {os.environ.get('OBSIDIAN_VAULT')!r})")
    vault_path = args.vault_path if args.vault_path.endswith(".md") else args.vault_path + ".md"
    dest_note = VAULT / vault_path
    body = Path(args.note_file).read_bytes()
    attachments_dir = dest_note.parent / "attachments"

    exists = dest_note.is_file()
    if args.new and exists:
        fail(f"{vault_path} already exists; read it, save a baseline copy and use --baseline")
    if args.baseline:
        if not exists:
            fail(f"{vault_path} does not exist; use --new")
        if dest_note.read_bytes() not in (Path(args.baseline).read_bytes(), body):
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
    text = body.decode("utf-8")
    missing = [e for e in re.findall(r"!\[\[([^\]|#]+)", text)
               if Path(e).name not in incoming and not (VAULT / e).exists()
               and not list(VAULT.rglob(Path(e).name))]
    if missing:
        fail(f"these embeds would not resolve (add them with --image): {missing}")

    changed = not exists or dest_note.read_bytes() != body
    if changed:
        dest_note.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest_note.with_name(dest_note.name + ".lla-tmp")
        tmp.write_bytes(body)
        os.replace(tmp, dest_note)
    if dest_note.read_bytes() != body:
        fail("saved content differs from the prepared note")

    attachments_dir.mkdir(parents=True, exist_ok=True)
    for src, dest in plan:
        if not dest.exists():
            shutil.copyfile(src, dest)

    print(json.dumps({
        "ok": True,
        "note": vault_path,
        "action": "created" if not exists else ("updated" if changed else "unchanged"),
        "chars": len(text),
        "attachments": [str(d) for _, d in plan],
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
