#!/usr/bin/env python3
"""NodeNuker: reclaim disk space by trashing stale node_modules/venv/build folders."""

import json
import os
import shutil
import time
from pathlib import Path

try:
    from send2trash import send2trash
except ImportError:
    send2trash = None

CONFIG_PATH = Path(__file__).resolve().parent / "nuker_config.json"

DEFAULT_TARGET_FOLDERS = [
    "node_modules", "venv", ".venv", "__pycache__",
    "dist", "build", ".next", ".turbo", "target",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
]
DEFAULT_DAYS_THRESHOLD = 30
DEFAULT_ROOT = "."


def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


def prompt_str(text, default):
    raw = input(f"{text} [{default}]: ").strip()
    return raw if raw else default


def prompt_int(text, default):
    while True:
        raw = input(f"{text} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def prompt_list(text, default_list):
    default_str = ", ".join(default_list)
    raw = input(f"{text} [{default_str}]: ").strip()
    if not raw:
        return default_list
    return [item.strip() for item in raw.split(",") if item.strip()]


def gather_settings():
    saved = load_config()
    print("=== NodeNuker configuration (press Enter to keep the default) ===")
    root = prompt_str("Root folder to scan", saved.get("root", DEFAULT_ROOT))
    days = prompt_int(
        "Only nuke folders whose project hasn't been touched in this many days",
        saved.get("days_threshold", DEFAULT_DAYS_THRESHOLD),
    )
    targets = prompt_list(
        "Target folder names (comma-separated)",
        saved.get("target_folders", DEFAULT_TARGET_FOLDERS),
    )
    config = {"root": root, "days_threshold": days, "target_folders": targets}
    save_config(config)
    return config


def resolve_path(path):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def human_size(num_bytes):
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"


def dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for name in filenames:
            fp = os.path.join(dirpath, name)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def most_recent_mtime(project_dir, target_folders):
    """Newest mtime among files under project_dir, skipping target_folders subtrees.

    This is what actually decides "idle" - the target folders themselves are
    excluded so that stale build artifacts don't make a project look active.
    """
    newest = os.path.getmtime(project_dir)
    for dirpath, dirnames, filenames in os.walk(project_dir):
        dirnames[:] = [d for d in dirnames if d not in target_folders]
        for name in filenames:
            fp = os.path.join(dirpath, name)
            try:
                mtime = os.path.getmtime(fp)
            except OSError:
                continue
            if mtime > newest:
                newest = mtime
    return newest


def find_candidates(root, target_folders):
    """Find every directory matching target_folders under root."""
    candidates = []
    root = resolve_path(root)
    for dirpath, dirnames, _ in os.walk(root):
        matched = [d for d in dirnames if d in target_folders]
        for name in matched:
            candidates.append({
                "project_dir": dirpath,
                "folder_name": name,
                "folder_path": os.path.join(dirpath, name),
            })
        # Don't descend into matched folders (e.g. nested node_modules) -
        # deleting the outer match removes them anyway.
        dirnames[:] = [d for d in dirnames if d not in matched]
    return candidates


def build_plan(candidates, days_threshold, target_folders):
    plan = []
    cutoff = time.time() - days_threshold * 86400
    for c in candidates:
        last_active = most_recent_mtime(c["project_dir"], target_folders)
        if last_active <= cutoff:
            plan.append({
                **c,
                "age_days": (time.time() - last_active) / 86400,
                "size": dir_size(c["folder_path"]),
            })
    plan.sort(key=lambda p: -p["size"])
    return plan


def review_plan(plan):
    if not plan:
        print("\nNothing matched your criteria. Nothing to do.")
        return []
    print("\n=== Candidates for deletion ===")
    for i, p in enumerate(plan, 1):
        print(f"[{i:>3}] {p['folder_path']}  ({human_size(p['size'])}, idle {p['age_days']:.0f}d)")
    print(f"\nTotal: {len(plan)} folders, {human_size(sum(p['size'] for p in plan))}")
    print("\nEnter numbers to EXCLUDE from deletion (comma-separated), Enter to delete all listed, or 'q' to abort.")
    raw = input("> ").strip()
    if raw.lower() == "q":
        return []
    if not raw:
        return plan
    try:
        exclude = {int(x.strip()) for x in raw.split(",") if x.strip()}
    except ValueError:
        print("Invalid input, aborting to be safe.")
        return []
    return [p for i, p in enumerate(plan, 1) if i not in exclude]


def _force_remove(func, path, exc_info):
    try:
        os.chmod(path, 0o700)
        func(path)
    except Exception:
        pass


def delete_folder(folder_path):
    if send2trash is not None:
        try:
            send2trash(folder_path)
            print(f"Trashed: {folder_path}")
            return
        except Exception as e:
            print(f"Failed to trash {folder_path} ({e}), falling back to permanent delete...")
    try:
        shutil.rmtree(folder_path, onerror=_force_remove)
        print(f"Deleted: {folder_path}")
    except Exception as e:
        print(f"Failed to delete {folder_path}. Reason: {e}")


def main():
    if send2trash is None:
        print("Note: 'send2trash' isn't installed, deletions will be PERMANENT.")
        print("Install it for recoverable deletes: pip install send2trash\n")

    config = gather_settings()
    print(f"\nScanning {resolve_path(config['root'])} ...")
    candidates = find_candidates(config["root"], config["target_folders"])
    plan = build_plan(candidates, config["days_threshold"], config["target_folders"])
    approved = review_plan(plan)
    if not approved:
        print("Nothing deleted.")
        return

    print(f"\nDeleting {len(approved)} folders...")
    for p in approved:
        delete_folder(p["folder_path"])


if __name__ == "__main__":
    main()
