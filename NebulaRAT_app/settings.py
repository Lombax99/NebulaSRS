import os
postgresql = {
    'pguser':os.environ.get('DB_USERNAME'),
    'pgpassword':os.environ.get('DB_PASSWORD'),
    'pghost':os.environ.get('DB_HOST'),
    'pgport': 5432,
    'pgdb': os.environ.get('DB_PGDB')
}

path="nebulaFiles"

secret = os.environ.get('FLASK_SECRET')