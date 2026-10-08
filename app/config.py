import os

# Secrets are injected through environment variables, never stored in code.
SECRET_KEY = os.environ.get("SECRET_KEY", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
