from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config, time, traceback, os, uuid

app = Flask(__name__, static_folder='static', static_url_path='')

logFile = "log-" + time.strftime("%Y-%m-%d-%H.%M.%S") + ".log"


"""
    Setup DB Models
"""
app.config['db'] = db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI


from model.FuzzingArch import FuzzingArch
from model.FuzzingPlatform import FuzzingPlatform
from model.FuzzingEngine import FuzzingEngine
from model.FuzzingHost import FuzzingHost
#from model.FuzzingConfig import FuzzingConfig
from model.FuzzingTarget import FuzzingTarget
from model.FuzzingJobState import FuzzingJobState
from model.FuzzingJobOption import FuzzingJobOption
from model.FuzzingJob import FuzzingJob
from model.FuzzingOptionType import FuzzingOptionType
from model.FuzzingOption import FuzzingOption
from model.FuzzingCrash import FuzzingCrash
from model.CallbackScript import CallbackScript
from model.FuzzingScript import FuzzingScript

db.drop_all()
db.create_all()
import seed
db.session.commit()

"""
@app.before_first_request
def create_db():
    None
"""


"""
    Setup Routes
"""
from controller.Hello import HelloCtrl
from controller.Update import UpdateCtrl
from controller.Job import JobCtrl
from controller.Engine import EngineCtrl
from controller.Arch import ArchCtrl
from controller.Platform import PlatformCtrl
from controller.Log import LogCtrl
from controller.Host import HostCtrl
from controller.Script import ScriptCtrl
from controller.Target import TargetCtrl
from controller.Crash import CrashCtrl
from controller.Status import StatusCtrl
#from controller.Config import ConfigCtrl
from controller.Option import OptionCtrl


api = Api(app)
api.add_resource(HelloCtrl, '/')
api.add_resource(UpdateCtrl, '/api/update/<string:hash>')
api.add_resource(JobCtrl, '/api/job', '/api/job/<string:id>')
api.add_resource(EngineCtrl, '/api/engine', '/api/engine/<string:id>')
api.add_resource(ArchCtrl, '/api/arch', '/api/arch/<string:id>')
api.add_resource(PlatformCtrl, '/api/platform', '/api/platform/<string:id>')
api.add_resource(HostCtrl, '/api/host', '/api/host/<string:id>')
api.add_resource(ScriptCtrl, '/api/script', '/api/script/<string:id>')
api.add_resource(TargetCtrl, '/api/target', '/api/target/<string:id>')
# api.add_resource(CrashBucketCtrl, '/api/bucket', '/api/bucket/<string:id>')
api.add_resource(CrashCtrl, '/api/crash', '/api/crash/<string:id>')
#api.add_resource(ConfigCtrl, '/api/config', '/api/config/<string:id>')
api.add_resource(OptionCtrl, '/api/option', '/api/option/<string:id>')
api.add_resource(LogCtrl, '/api/log')
api.add_resource(StatusCtrl, '/api/status')


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    message = time.strftime("%Y-%m-%d-%H.%M.%S") + ": \n" + traceback.format_exc() + "\n\n"
    with open(logFile, 'a') as f:
        f.write(message)
    rv = {}
    rv['message'] = message
    response = jsonify(rv)
    response.status_code = 500
    return response


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return json.dumps({"err": "invalid request"}), 400

    u_file = request.files['file']
    if u_file.filename == '':
        return json.dumps({"err": "invalid request"}), 400

    path = os.path.join(config.UPLOAD_FOLDER, str(uuid.uuid4()))

    u_file.save(path)
    return json.dumps({"upload_path": path}), 200
