import os
import zipfile
import sqlite3
import tempfile
from datetime import datetime
import argparse

def backup_sqlite(db_path, backup_dir, media_dir=None):
    os.makedirs(backup_dir, exist_ok=True)

    now = datetime.now()
    day_name = now.strftime('%a')  # Mon, Tue, etc.
    zip_name = f"backup_{now.strftime('%Y-%m-%d')}_{day_name}_{now.strftime('%H-%M-%S')}.zip"
    zip_path = os.path.join(backup_dir, zip_name)

    # Create temp file for SQLite backup
    with tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False) as tmpfile:
        tmp_backup_path = tmpfile.name

    # Safe SQLite backup using .backup()
    source_conn = sqlite3.connect(db_path)
    dest_conn = sqlite3.connect(tmp_backup_path)
    with dest_conn:
        source_conn.backup(dest_conn, pages=0)
    dest_conn.close()
    source_conn.close()

    print(f"SQLite backup created at: {tmp_backup_path}")

    # Create ZIP file and add backup DB
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(tmp_backup_path, arcname='db.sqlite3')

        # Optionally add media folder (or any folder)
        if media_dir:
            if os.path.exists(media_dir):
                print(f"Adding media folder to zip: {media_dir}")
                for root, dirs, files in os.walk(media_dir):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        rel_path = os.path.relpath(abs_path, media_dir)
                        zipf.write(abs_path, arcname=os.path.join('media', rel_path))
            else:
                print(f"Warning: Media directory '{media_dir}' not found. Skipping.")

    # Remove temp backup DB
    os.remove(tmp_backup_path)

    print(f"Backup zip created successfully: {zip_path}")

def main():
    parser = argparse.ArgumentParser(description="Backup SQLite DB with optional media folder.")
    parser.add_argument('db_path', help="Path to the SQLite database file.")
    parser.add_argument('--media', help="Path to media folder (optional).")
    parser.add_argument('--backup-dir', default='db_backups', help="Backup output directory.")
    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"Error: Database file '{args.db_path}' does not exist.")
        return

    backup_sqlite(args.db_path, args.backup_dir, args.media)

if __name__ == "__main__":
    main()
