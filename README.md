### NodeNuker

---

#### Introduction

Welcome to **NodeNuker**! The ultimate solution for developers tired of the gigantic black holes of memory (a.k.a. `node_modules` and `venv` folders) that clutter up their projects. If you've ever felt like these folders are larger than actual black holes, this script is your new best friend.

---

#### Why NodeNuker?

As a developer, managing disk space is a perpetual struggle. With every project, those `node_modules` and `venv` folders grow and grow, consuming precious space. Here's why **NodeNuker** is a must-have:

- **Saves Space**: Instantly reclaim gigabytes of disk space by removing unnecessary folders.
- **Cleans Up Projects**: Keep your project directories clean and organized.
- **Effortless**: Automate the tedious task of manually deleting these folders.

---

#### How to Use

Using **NodeNuker** is as easy as 1-2-3!

1. **Download the Script**: Save the script to a file named `NodeNuker.py`.
2. **Navigate to the Root Folder**: Open your terminal and navigate to the root directory where all your projects are stored.
3. **Run the Script**: Execute the script by running `python NodeNuker.py`.

```bash
# Navigate to the root folder containing all your projects
cd /path/to/your/root/folder

# Run NodeNuker
python NodeNuker.py
```

**NodeNuker** will then go through each subdirectory and nuke those pesky `node_modules` and `venv` folders into oblivion!

---

#### The Code

Here's a sneak peek at the magic behind **NodeNuker**:

```python
import os
import shutil

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder_path}")
    except Exception as e:
        print(f"Failed to delete {folder_path}. Reason: {e}")

def find_and_delete(target_folders):
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name in target_folders:
                folder_path = os.path.join(root, dir_name)
                delete_folder(folder_path)

if __name__ == "__main__":
    target_folders = ['node_modules', 'venv']
    find_and_delete(target_folders)
```

---

#### Jokes Corner

- **Why did the developer go broke?** Because they used up all their cache!
- **What's a developer's favorite type of music?** Algo-rhythm.
- **Why do programmers always mix up Christmas and Halloween?** Because Oct 31 == Dec 25.

---

Enjoy a cleaner, more organized workspace with **NodeNuker**. Say goodbye to the gigantic memory black holes, and hello to more free space for your creative projects!

Happy coding!
