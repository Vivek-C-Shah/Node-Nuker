### NodeNuker

---

#### Introduction

Welcome to **NodeNuker**! The ultimate solution for developers tired of the gigantic black holes of memory (a.k.a. `node_modules`, `venv`, and build/cache folders) that clutter up their projects.

---

#### Why NodeNuker?

- **Saves Space**: Reclaim gigabytes of disk space by clearing out cruft from projects you haven't touched in a while.
- **Cross-platform**: Works the same on macOS and Windows.
- **Idle-aware**: Only targets projects that have actually gone stale, based on when their source files were last modified (build/cache folders themselves don't count).
- **Reviewable**: Shows you the full deletion plan, with size and idle time per folder, before anything happens. You can strike entries out before confirming.
- **Recoverable**: Deletes go to the OS Trash/Recycle Bin (via `send2trash`) instead of being wiped permanently, if the package is installed.

---

#### Setup

```bash
pip install -r requirements.txt
```

(`send2trash` is optional but strongly recommended — without it, deletions are permanent.)

---

#### How to Use

```bash
# Navigate to the root folder containing all your projects
cd /path/to/your/root/folder

# Run NodeNuker
python NodeNuker.py
```

Each run walks you through a short configuration step:

```
=== NodeNuker configuration (press Enter to keep the default) ===
Root folder to scan [.]:
Only nuke folders whose project hasn't been touched in this many days [30]:
Target folder names (comma-separated) [node_modules, venv, .venv, __pycache__, dist, build, .next, .turbo, target, .pytest_cache, .mypy_cache, .ruff_cache]:
```

Your answers are saved to `nuker_config.json` next to the script, and reused as the defaults next time (edit that file by hand any time too).

NodeNuker then scans, and shows you the full plan before touching anything:

```
=== Candidates for deletion ===
[  1] ./old-project/node_modules  (412.3MB, idle 96d)
[  2] ./archived-api/venv         (88.1MB, idle 210d)
[  3] ./archived-api/__pycache__  (1.2MB, idle 210d)

Total: 3 folders, 501.6MB

Enter numbers to EXCLUDE from deletion (comma-separated), Enter to delete all listed, or 'q' to abort.
>
```

Type numbers to exclude specific folders, press Enter to proceed with everything listed, or `q` to abort without deleting anything.

---

#### Notes

- "Idle" is measured by the newest file modification time anywhere in the project, ignoring the target folders themselves — so reinstalling `node_modules` doesn't reset the clock.
- Nested target folders (e.g. `node_modules` inside `node_modules`) aren't scanned separately; deleting the outer one removes them anyway.
- Config file (`nuker_config.json`) is gitignored since it's a personal, per-machine setting.

---

#### Jokes Corner

- **Why did the developer go broke?** Because they used up all their cache!
- **What's a developer's favorite type of music?** Algo-rhythm.
- **Why do programmers always mix up Christmas and Halloween?** Because Oct 31 == Dec 25.

---

Enjoy a cleaner, more organized workspace with **NodeNuker**. Say goodbye to the gigantic memory black holes, and hello to more free space for your creative projects!

Happy coding!
