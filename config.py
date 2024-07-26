import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
PUG_DIR = os.path.join(TEMPLATES_DIR, 'pug')
HTML_DIR = os.path.join(TEMPLATES_DIR, 'html')
DATABASE_FOLDER_PATH = os.path.join(BASE_DIR, 'app', 'data')
DATABASE_PATH = os.path.join(DATABASE_FOLDER_PATH, 'data.db')
