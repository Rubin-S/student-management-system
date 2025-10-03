# backup.py
import shutil
from datetime import datetime
from pathlib import Path

# --- Configuration ---
SOURCE_DB_PATH = Path("sis.db")
BACKUP_DIR = Path("backups")

def create_backup():
    """Copies the source database to the backup directory with a timestamp."""

    # 1. Ensure the source database exists
    if not SOURCE_DB_PATH.exists():
        print(f"Error: Source database not found at '{SOURCE_DB_PATH}'")
        return

    # 2. Ensure the backup directory exists
    BACKUP_DIR.mkdir(exist_ok=True)

    # 3. Create a timestamped filename for the backup
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{SOURCE_DB_PATH.stem}-backup-{timestamp}{SOURCE_DB_PATH.suffix}"
    destination_path = BACKUP_DIR / backup_filename

    # 4. Copy the file
    try:
        shutil.copyfile(SOURCE_DB_PATH, destination_path)
        print(f"✅ Backup successful! Created: {destination_path}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")

if __name__ == "__main__":
    create_backup()