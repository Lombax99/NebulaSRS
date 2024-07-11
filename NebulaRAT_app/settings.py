import os
postgresql = {
    'pguser':os.environ.get('DB_USERNAME'),
    'pgpassword':os.environ.get('DB_PASSWORD'),
    'pghost':os.environ.get('DB_HOST'),
    'pgport': 5432,
    'pgdb': os.environ.get('DB_PGDB')
}

path="nebulaFiles"

# Path to the scripts
nebulaCert_path = os.path.join("nebulaScripts", "nebula-cert")       # ./nebula-cert print -path somecert.crt    to see certificate

# output directory path
outputDir = "nebulaFiles"

secret = os.environ.get('FLASK_SECRET')