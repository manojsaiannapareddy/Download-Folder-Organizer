import shutil
from pathlib import Path
from datetime import datetime

download_folder = Path.home() / "Downloads"

# Exact folder names expected to exist in the Downloads directory.
EXISTING_FOLDERS = {
    "Images", "Documents", "Audio", "Videos",
    "Programs", "Games", "Music", "Torrents",
    "Others", "Last month", "Earlier this year",
    "A long time ago"
}

# Defines the file categories and their corresponding file extensions.
# For example, all files ending with '.jpg', '.jpeg', '.png', etc., will be moved to the 'Images' folder.
FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    "Audio": ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg'],
    "Programs": ['.exe', '.msi', '.dmg', '.pkg', '.deb'],
    "Torrents": ['.torrent'],
    "Music": ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']  # Example extension mapping
}

def safe_move(file: Path, target_dir: Path):
    """
    Moves a given file to the specified target directory.

    This function ensures that if a file with the same name already exists
    in the target directory, the moved file will be renamed to avoid overwriting.
    For example, if 'report.pdf' exists, the next 'report.pdf' will be named 'report (1).pdf'.

    Args:
        file (Path): The Path object representing the file to be moved.
        target_dir (Path): The Path object representing the destination directory.

    Returns:
        bool: True if the file was moved successfully, False otherwise (e.g., due to an error).
    """
    try:
        # Create the target directory if it doesn't exist. exist_ok=True prevents an error if the directory already exists.
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / file.name

        # Handle existing files by appending a counter until a unique name is found.
        counter = 1
        while target_path.exists():
            stem = file.stem  # Filename without the extension
            suffix = file.suffix  # File extension (e.g., '.pdf')
            new_name = f"{stem} ({counter}){suffix}" # Example: report (1).pdf
            target_path = target_dir / new_name
            counter += 1

        shutil.move(str(file), str(target_path))
        return True
    except Exception as e:
        print(f"Error moving {file.name}: {str(e)}") # Example error message: Error moving document.pdf: [Errno 13] Permission denied: '...'
        return False

def organize_files():
    """
    Organizes files in the download folder based on their file extensions.

    It iterates through all files in the download folder and attempts to move them
    into predefined category folders (e.g., 'Images', 'Documents'). Files with
    extensions not matching any category are moved to the 'Others' folder.
    It skips any existing folders in the download directory to avoid processing them as files.
    """
    # Iterate through each item in the download folder.
    for file in download_folder.iterdir():
        # Only process items that are files and are not in the list of existing folder names.
        if file.is_file() and file.name not in EXISTING_FOLDERS:
            moved = False

            # Check the file extension against the defined file categories.
            for category, extensions in FILE_CATEGORIES.items():
                # Convert the file extension to lowercase for case-insensitive matching.
                if file.suffix.lower() in extensions:
                    target_dir = download_folder / category
                    # Attempt to move the file to the corresponding category folder.
                    if safe_move(file, target_dir):
                        moved = True
                        break # Once moved, no need to check other categories.

            # If the file's extension doesn't match any defined category, move it to the 'Others' folder.
            if not moved:
                safe_move(file, download_folder / "Others")

if __name__ == "__main__":
    organize_files()
    print("Organization completed safely!") # Confirmation message after the script has run.