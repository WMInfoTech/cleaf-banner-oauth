import os


class Config():
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_dsn = os.getenv('DB_DSN')
    cl_redirect_url = os.getenv('CL_REDIRECT_URL')
    ttl_seconds = int(os.getenv('CL_TTL_SECONDS'))
    published_version = os.getenv('PUBLISHED_VERSION')


    if os.path.isfile(db_password):
        with open(db_password, 'r') as password_file:
            db_password = password_file.read().rstrip()

    CAS_SERVER = 'https://cas.wm.edu'
    CAS_AFTER_LOGIN = 'index'
    CAS_LOGIN_ROUTE = '/cas/login'
    CAS_VALIDATE_ROUTE = '/cas/p3/serviceValidate'
    DEBUG = False

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    if os.path.isfile(SECRET_KEY):
        with open(SECRET_KEY, 'r') as SECRET_KEY_file:
            SECRET_KEY = SECRET_KEY_file.read().rstrip()
