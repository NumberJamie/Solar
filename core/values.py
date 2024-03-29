from pathlib import Path

PROJECT_PATH: Path = Path(__file__).resolve().parent.parent

MEDIA_URL: str = '/media'
MEDIA_DIR: str = f'{PROJECT_PATH}/media'

STATIC_URL: str = '/static'
STATIC_DIR: str = f'{PROJECT_PATH}/static'

TEMPLATES: str = f'{PROJECT_PATH}/templates'
DB_FILE: str = f'{PROJECT_PATH}/db.sqlite3'
