# Simple SQLite DB Backup Scripts

This repository provides two Python scripts for backing up your SQLite database:
- **backup_db.py**: For general Python/SQLite projects.
- **backup_db_django.py**: For Django projects, provided as a management command template (you can rename it when adding to your project).

---

## Table of Contents

- [General Standalone Script (`backup_db.py`)](#general-standalone-script-backup_dbpy)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Example](#example)
  - [Troubleshooting](#troubleshooting)
- [Django Management Command (`backup_db_django.py` → custom name)](#django-management-command-backup_db_djangopy--custom-name)
  - [Integrating into Your Django Project](#integrating-into-your-django-project)
  - [Renaming the Command](#renaming-the-command)
  - [Running the Backup Command](#running-the-backup-command)
  - [Customization & Options](#customization--options)
  - [Example Workflow](#example-workflow)
  - [Troubleshooting](#troubleshooting-django)
- [Script Selection Guide](#script-selection-guide)
- [License & Author](#license--author)

---

## General Standalone Script (`backup_db.py`)

### Features

- Safe backup of a SQLite database using Python’s standard library.
- Optionally include a media folder in the backup.
- Creates a timestamped ZIP archive.
- Simple CLI usage.

### Requirements

- Python 3.6 or newer.
- No external dependencies.

### Usage

1. **Clone the repository:**

    ```sh
    git clone https://github.com/legeRise/simple-db-backup-script.git
    cd simple-db-backup-script
    ```

2. **Run the backup script:**

    - Backup just the database:

        ```sh
        python backup_db.py /path/to/your/database.sqlite3
        ```

    - Backup database and media folder:

        ```sh
        python backup_db.py /path/to/your/database.sqlite3 --media /path/to/media_folder
        ```

    - Specify a custom backup directory:

        ```sh
        python backup_db.py /path/to/your/database.sqlite3 --backup-dir /path/to/backups
        ```

### Example

```sh
python backup_db.py mydb.sqlite3 --media ./media
```
Creates a ZIP file in `db_backups/` containing your database and all media files.

### Troubleshooting

- **Database not found:** Check your database path.
- **Media folder missing:** The script warns and skips if the folder does not exist.
- **Permissions:** Make sure you have access to the files/folders.

---

## Django Management Command (`backup_db_django.py` → custom name)

This script is provided as `backup_db_django.py` in this repository. When adding it to your Django project, you can rename it to any command name you prefer (e.g., `db_backup.py`). The command name will match the filename you choose.

### Integrating into Your Django Project

1. **Copy the Script:**
   - Copy `backup_db_django.py` from this repo into your Django app at:
     `your_app/management/commands/<your_command_name>.py`
     (Create the folders if they do not exist.)

    ```
    your_project/
        your_app/
            management/
                commands/
                    db_backup.py  # or any name you prefer
    ```

2. **Rename the Script (Recommended):**
   - Rename `backup_db_django.py` to something meaningful for your project, e.g., `db_backup.py` or `database_backup.py`.
   - The management command name will match the filename you use.

3. **Adjust the Script (if needed):**
   - Ensure the script correctly references your database and media folder. By default, it uses Django settings.

### Renaming the Command

- If you name the file `db_backup.py`, run:
  ```sh
  python manage.py db_backup
  ```
- If you name it `database_backup.py`, run:
  ```sh
  python manage.py database_backup
  ```

### Running the Backup Command

From your Django project root, run:

```sh
python manage.py <your_command_name>
```

- This will back up your SQLite database and your media folder into a ZIP file.
- By default, the backup ZIP will be created in `db_backups/`.

### Customization & Options

- Pass options as defined in the script:
  ```sh
  python manage.py <your_command_name> --help
  ```

### Example Workflow

1. **Copy `backup_db_django.py` to your app's management/commands directory.**
2. **Rename it to your desired command name (e.g., `db_backup.py`).**
3. **Run:**
    ```sh
    python manage.py db_backup
    ```
4. **Find your backup ZIP in `db_backups/`.**

### Troubleshooting (Django)

- **App not found:** Confirm you placed the script in an installed app.
- **Database/media folder path issues:** Adjust script to match your project’s settings.
- **Permissions:** Run with appropriate access.

---

## Script Selection Guide

| Use case                          | Script to use            | How to run                                      |
|------------------------------------|--------------------------|-------------------------------------------------|
| General Python/SQLite project      | `backup_db.py`           | `python backup_db.py <db_path> [options]`        |
| Django project                     | `<your_command_name>.py` | `python manage.py <your_command_name> [options]` |

---

## License & Author

- **License:** MIT
- **Author:** [legeRise](https://github.com/legeRise)

---

**Tip:**
- For standalone use, stick with `backup_db.py`.
- For Django, copy `backup_db_django.py` as a management command and rename it as you wish for easy backups via `manage.py`.
