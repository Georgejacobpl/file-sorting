import os
import shutil
import logging

# Configure logging to track what the script does
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Dictionary mapping categories to file extensions
EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".svg"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".rtf"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".json", ".xml"],
    "Others": []  # Default category for unknown extensions
}

def create_folders(directory_path, categories):
    """Creates category folders if they don't exist."""
    for category in categories:
        folder_path = os.path.join(directory_path, category)
        os.makedirs(folder_path, exist_ok=True)  # exist_ok=True prevents errors if folder exists
        logger.info(f"Created folder: {category}")

def get_category(extension):
    """Returns the category for a given file extension."""
    for category, ext_list in EXTENSIONS.items():
        if extension.lower() in ext_list:
            return category
    return "Others"  # Return 'Others' if extension not found

def organize_files(directory_path):
    """Main function to organize files in the given directory."""
    try:
        # Get all items in the directory
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():  # Process only files, ignore folders
                    file_path = entry.path
                    file_extension = os.path.splitext(file_path)[1]  # Get the file extension
                    category = get_category(file_extension)

                    # Define the destination path
                    dest_dir = os.path.join(directory_path, category)
                    dest_path = os.path.join(dest_dir, entry.name)

                    # Move the file
                    shutil.move(file_path, dest_path)
                    logger.info(f"Moved: {entry.name} -> {category}/")

        logger.info("File organization complete!")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    target_directory = input("Enter the path of the directory to organize: ").strip()

    if os.path.isdir(target_directory):
        create_folders(target_directory, EXTENSIONS.keys())
        organize_files(target_directory)
    else:
        logger.error("The provided path is not a valid directory.")