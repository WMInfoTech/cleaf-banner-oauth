from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, redirect, jsonify
from flask_cas import login_required, CAS
import oracledb
import uuid
import base64
import datetime

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.config['SESSION_COOKIE_NAME'] = 'wm_path_login'
app.config['CAS_ATTRIBUTES_SESSION_KEY'] = 'WM_SSO_ATTRS'
cas = CAS(app)

config = Config()

def getpool():
    pool = oracledb.SessionPool(user=config.db_username, password=config.db_password,
                                   dsn=config.db_dsn,
                                   min=1, max=1, increment=1, encoding="UTF-8")
    return pool

@app.route("/", methods=('GET',))
@login_required
def index():
    if 'student' not in cas.attributes['cas:eduPersonAffiliation'] and config.students_only is True:
        return jsonify({"status": 404, "message": "Students only"}), 404
    pool = getpool()
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("SELECT gobumap_pidm FROM gobumap WHERE gobumap_udc_id = :gobumap_udc_id", {'gobumap_udc_id': cas.attributes["cas:UDC_IDENTIFIER"]})
    row = cursor.fetchone()
    lv_pidm = row[0]
    lv_token = base64.b64encode(str(uuid.uuid4()).encode("UTF-8")).decode("UTF-8")
    lv_code = base64.b64encode(str(uuid.uuid4()).encode("UTF-8")).decode("UTF-8")
    lv_expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=config.ttl_seconds)

    cursor.execute("""INSERT INTO CLEAF.cl_access_token
        (ct_pidm
        ,ct_token
        ,ct_code
        ,ct_expire_date
        ,ct_create_date
        ,ct_external_id)
    VALUES
        (:lv_pidm
        ,:lv_token
        ,:lv_code
        ,:lv_expire_date
        ,SYSDATE
        ,null)""", {"lv_pidm": lv_pidm, "lv_token": lv_token, "lv_code": lv_code, "lv_expire_date": lv_expiration_date})
    connection.commit()

    return redirect("{}?code={}".format(config.cl_redirect_url, lv_code))

@app.route("/healthcheck/ping/", methods=('GET',))
def ping():
    published_version = {"PUBLISHED_VERSION": config.published_version}
    return jsonify({"status": 200, "message": published_version}), 200
