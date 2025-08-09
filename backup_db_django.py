import os
import zipfile
import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Backup SQLite DB (using .backup()) and optionally media folder into a zip file named with today's date and day name."

    def add_arguments(self, parser):
        parser.add_argument(
            '--include-media',
            action='store_true',
            help='Include media files in the backup zip.',
        )

    def handle(self, *args, **options):
        include_media = options['include_media']

        db_path = settings.DATABASES['default']['NAME']
        media_path = os.path.join(settings.BASE_DIR, 'media')
        backup_dir = os.path.join(settings.BASE_DIR, 'db_backups')
        os.makedirs(backup_dir, exist_ok=True)

        now = datetime.now()
        day_name = now.strftime('%a')  # Mon, Tue, etc.
        zip_name = f"backup_{now.strftime('%Y-%m-%d')}_{day_name}_{now.strftime('%H-%M-%S')}.zip"
        zip_path = os.path.join(backup_dir, zip_name)

        # Temporary backup DB filename (in the backup_dir)
        backup_db_filename = os.path.join(backup_dir, f"db_backup_{now.strftime('%Y-%m-%d_%H-%M-%S')}.sqlite3")

        if not os.path.exists(db_path):
            self.stderr.write(f"Error: Database file not found at {db_path}")
            return

        self.stdout.write('Creating SQLite backup using .backup()...')
        source_conn = sqlite3.connect(db_path)
        dest_conn = sqlite3.connect(backup_db_filename)
        with dest_conn:
            source_conn.backup(dest_conn, pages=0)
        dest_conn.close()
        source_conn.close()
        self.stdout.write(f'SQLite backup created at: {backup_db_filename}')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the backup DB file as db.sqlite3 inside the zip
            zipf.write(backup_db_filename, arcname='db.sqlite3')

            if include_media:
                if os.path.exists(media_path):
                    self.stdout.write(f'Adding media directory to zip: {media_path}')
                    for root, dirs, files in os.walk(media_path):
                        for file in files:
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_path, media_path)
                            zipf.write(abs_path, arcname=os.path.join('media', rel_path))
                else:
                    self.stderr.write('Warning: Media directory not found, skipping media backup.')

        # Remove the temporary SQLite backup file
        os.remove(backup_db_filename)

        self.stdout.write(self.style.SUCCESS(f'Backup zip created successfully: {zip_path}'))
