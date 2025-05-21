import os
import logging
from flask import Flask

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "youtube-dl-secret-key")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Temp folder for storing downloads
TEMP_DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_downloads")
if not os.path.exists(TEMP_DOWNLOAD_FOLDER):
    os.makedirs(TEMP_DOWNLOAD_FOLDER)
app.config['TEMP_DOWNLOAD_FOLDER'] = TEMP_DOWNLOAD_FOLDER

logger.debug(f"Temp download folder: {TEMP_DOWNLOAD_FOLDER}")
