from dobrodzieje.settings.base import *

# Override base.py settings here
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False