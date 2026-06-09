import subprocess
from pathlib import Path


def open_presentation(file_path):
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            return {
                "success": False,
                "message": f"Presentation not found: {file_path}"
            }

        subprocess.Popen(f'explorer "{file_path}"', shell=True)

        return {
            "success": True,
            "message": f"Opened presentation: {file_path}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to open presentation: {error}"
        }