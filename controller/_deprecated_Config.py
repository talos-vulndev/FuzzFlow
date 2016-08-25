from flask_restful import Resource, reqparse
#from model.FuzzingConfig import FuzzingConfig
from model.FuzzingPlatform import FuzzingPlatform
from model.FuzzingArch import FuzzingArch
from model.FuzzingHost import FuzzingHost
from model.FuzzingEngine import FuzzingEngine
from model.FuzzingTarget import FuzzingTarget
from controller.Job import JobManager
from app import app

db = app.config['db']


class ConfigCtrl(Resource):
    def create(self, data):
        host = FuzzingHost.query.filter_by(id=data['host_id']).first()
        if host is None:
            return {"err": "invalid request"}, 400

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if arch is None:
            return {"err": "invalid request"}, 400

        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is None:
            return {"err": "invalid request"}, 400

        try:
            config = FuzzingConfig(host, arch, platform)
            if data['engines'] is not None:
                for engine_id in data['engines']:
                    engine = FuzzingEngine.query.filter_by(id=engine_id).first()
                    if engine is not None:
                        config.engines.append(engine)

            if data['targets'] is not None:
                for target_id in data['targets']:
                    target = FuzzingTarget.query.filter_by(id=target_id).first()
                    if target is not None:
                        config.targets.append(target)

            db.session.add(config)
            db.session.commit()

        except Exception as e:
            return {"err" : "invalid request"}, 400

        result = config.as_dict()
        result['engines'] = [engine.as_dict() for engine in config.engines.all()]
        result['targets'] = [target.as_dict() for target in config.targets.all()]
        return result, 201

    def read(self, id, by=None):
        if by == 'host':
            config = FuzzingConfig.query.filter_by(host_id=id).first()
        else:
            config = FuzzingConfig.query.filter_by(id=id).first()
        if config is None:
            return {"err": "not found"}, 404

        result = config.as_dict()
        result['engines'] = [engine.as_dict() for engine in config.engines.all()]
        result['targets'] = [target.as_dict() for target in config.targets.all()]
        return result, 200

    def update(self, id, data):
        config = FuzzingConfig.query.filter_by(id=id).first()
        if config is None:
            return {"err": "not found"}, 404

        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is not None:
            config.platform = platform

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if arch is not None:
            config.arch = arch

        host = FuzzingHost.query.filter_by(id=data['host_id']).first()
        if host is not None:
            config.host = host

        if data['engines'] is not None:
            config.engines = []
            for engine_id in data['engines']:
                engine = FuzzingEngine.query.filter_by(id=engine_id).first()
                if engine is not None:
                    config.engines.append(engine)

        if data['targets'] is not None:
            config.targets = []
            for target_id in data['targets']:
                target = FuzzingTarget.query.filter_by(id=target_id).first()
                if target is not None:
                    config.targets.append(target)

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        result = config.as_dict()
        result['engines'] = [engine.as_dict() for engine in config.engines.all()]
        result['targets'] = [target.as_dict() for target in config.targets.all()]
        return result, 201

    def delete(self, id):
        config = FuzzingConfig.query.filter_by(id=id).first()
        if config is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(config)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        configs = FuzzingConfig.query.offset(offset).limit(limit).all()
        configs = [conf.as_dict() for conf in configs]
        JobManager.assign_jobs()
        return configs, 200

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        parser.add_argument('host', type=int)

        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            else:
                return self.list()
        else:
            if args['delete'] == 1:
                return self.delete(id)
            elif args['host'] == 1:
                return self.read(id, 'host')
            else:
                return self.read(id)

    def post(self, id=None):
        parser = reqparse.RequestParser()
        if id is None:
            parser.add_argument('host_id', required=True, location='json')
            parser.add_argument('arch_id', required=True, location='json')
            parser.add_argument('platform_id', required=True, location='json')
            parser.add_argument('engines', location='json')
            parser.add_argument('targets', location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('host_id', location='json')
            parser.add_argument('arch_id', location='json')
            parser.add_argument('platform_id', location='json')
            parser.add_argument('engines', location='json')
            parser.add_argument('targets', location='json')
            return self.update(id, parser.parse_args())