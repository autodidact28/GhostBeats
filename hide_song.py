#!/usr/bin/env python3
"""
Usage:
  python3 hide_song_v4.py /full/path/to/song.mp3

What it does:
 - Ensures you're inside a git repo
 - Creates songs/<songname>.txt (appends small lines so git can commit)
 - Splits the mp3 (base64) into chunks and commits each chunk with message:
     SONG:<songname>:CHUNK:<index>:<base64_chunk>
 - Minimal console output: progress every 5% + final success/error
"""
import sys
import os
import base64
import subprocess
from pathlib import Path

CHUNK_SIZE = 4000   # safe default for commit-message size
PROGRESS_STEP_PERCENT = 5

def run_checked(cmd, hide_output=True):
    if hide_output:
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        return subprocess.run(cmd)

def ensure_git_repo():
    rc = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if rc.returncode != 0 or rc.stdout.strip() != "true":
        raise SystemExit("ERROR: Current folder is not a git repository. Run `git init` first or cd to repo root.")

def commit_song_file(song_path: Path):
    if not song_path.exists():
        raise SystemExit(f"ERROR: File not found: {song_path}")

    song_name = song_path.stem
    songs_dir = Path("songs")
    songs_dir.mkdir(exist_ok=True)
    target_txt = songs_dir / f"{song_name}.txt"

    # Read and encode
    try:
        raw = song_path.read_bytes()
    except Exception as e:
        raise SystemExit(f"ERROR: Unable to read file: {e}")

    b64 = base64.b64encode(raw).decode()
    chunks = [b64[i:i+CHUNK_SIZE] for i in range(0, len(b64), CHUNK_SIZE)]
    total = len(chunks)
    if total == 0:
        raise SystemExit("ERROR: File appears empty after encoding.")

    # Print initial message
    print(f"🎵 Hiding '{song_name}' across {total} commits...")

    last_shown = -1
    for i, chunk in enumerate(chunks):
        # write small change so git can commit
        try:
            with target_txt.open("a") as f:
                f.write(f"{song_name} part {i}\n")
        except Exception as e:
            raise SystemExit(f"ERROR: Cannot write to {target_txt}: {e}")

        # git add & commit (quiet)
        rc_add = run_checked(["git", "add", str(target_txt)])
        if rc_add.returncode != 0:
            raise SystemExit("ERROR: `git add` failed. Are you in a git repo and have permissions?")

        commit_message = f"SONG:{song_name}:CHUNK:{i}:{chunk}"
        rc_commit = run_checked(["git", "commit", "-m", commit_message])
        if rc_commit.returncode != 0:
            raise SystemExit(f"ERROR: `git commit` failed at chunk {i}. Check git config (user.name/user.email) and repository state.")

        # Progress reporting every PROGRESS_STEP_PERCENT
        percent = int(((i + 1) / total) * 100)
        # only print at multiples of PROGRESS_STEP_PERCENT and avoid repeats
        if percent // PROGRESS_STEP_PERCENT != last_shown // PROGRESS_STEP_PERCENT:
            last_shown = percent
            if percent < 100:
                sys.stdout.write(f"\r🔄 Progress: {percent}%")
                sys.stdout.flush()

    # finish line
    sys.stdout.write("\r")
    print(f"✅ Done — '{song_name}' hidden successfully! Commits: {total}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 hide_song_v4.py /path/to/song.mp3")
        sys.exit(1)

    try:
        ensure_git_repo()
        song = Path(sys.argv[1])
        commit_song_file(song)
    except SystemExit as e:
        # user-friendly error output
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Unhandled error: {e}")
        sys.exit(1)
