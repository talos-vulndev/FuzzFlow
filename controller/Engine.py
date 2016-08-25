from flask_restful import Resource, reqparse
from model.FuzzingEngine import FuzzingEngine
from model.FuzzingPlatform import FuzzingPlatform
from model.FuzzingOption import FuzzingOption
from model.FuzzingArch import FuzzingArch

from app import app


db = app.config['db']


class EngineCtrl(Resource):
    def create(self, data):
        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is None:
            return {"err" : "invalid request"}, 400

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if platform is None:
            return {"err" : "invalid request"}, 400

        try:
            engine = FuzzingEngine(data['name'], data['path'], platform, arch)

            if data['options'] is not None:
                for option_id in data['options']:
                    options = FuzzingOption.query.filter_by(id=option_id).first()
                    if options is not None:
                        engine.options.append(options)

            db.session.add(engine)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        result = engine.as_dict()
        result['options'] = [option.as_dict() for option in engine.options]
        return result, 201


    def read(self, id):
        engine = FuzzingEngine.query.filter_by(id=id).first()
        if engine is None:
            return {"err": "not found"}, 404

        result = engine.as_dict()
        result['options'] = [option.as_dict() for option in engine.options]
        return result, 200

    def update(self, id, data):
        engine = FuzzingEngine.query.filter_by(id=id).first()
        if engine is None:
            return {"err": "not found"}, 404

        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is not None:
            engine.platform = platform

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if arch is not None:
            engine.arch = arch

        if data['name'] is not None:
            engine.name = data['name']

        if data['path'] is not None:
            engine.path = data['path']

        if data['options'] is not None:
            engine.options = []
            for option_id in data['options']:
                options = FuzzingOption.query.filter_by(id=option_id).first()
                if options is not None:
                    engine.options.append(options)

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        result = engine.as_dict()
        result['options'] = [option.as_dict() for option in engine.options]
        return result, 200

    def delete(self, id):
        engine = FuzzingEngine.query.filter_by(id=id).first()
        if engine is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(engine)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        engines = FuzzingEngine.query.offset(offset).limit(limit).all()
        result = [engine.as_dict() for engine in engines]
        for i in xrange(len(engines)):
            result[i]['options'] = engines[i].options
            result[i]['options'] = [option.as_dict() for option in result[i]['options']]

        return result, 200

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            else:
                return self.list()
        else:
            if args['delete'] == 1:
                return self.delete(id)
            else:
                return self.read(id)

    def post(self, id=None):
        parser = reqparse.RequestParser()
        if id is None:
            parser.add_argument('name', required=True, location='json')
            parser.add_argument('path', required=True, location='json')
            parser.add_argument('platform_id', required=True, location='json')
            parser.add_argument('arch_id', required=True, location='json')
            parser.add_argument('options', location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('path', location='json')
            parser.add_argument('platform_id', location='json')
            parser.add_argument('arch_id', location='json')
            parser.add_argument('options', location='json')
            return self.update(id, parser.parse_args())