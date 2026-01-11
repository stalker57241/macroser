from pathlib import Path


include_folders: list[str] = ["."]

def find_file(filename: str) -> Path:
    for folder in include_folders:
        p = Path(f"{folder}/{filename}")
        print(p)
        if p.exists():
            return p
    raise ValueError("Header not found")

def include_folder(path: str):
    global include_folders
    include_folders.append(path.rstrip("/"))
