from flask_restful import Resource, reqparse
from model.FuzzingTarget import FuzzingTarget
from model.FuzzingArch import FuzzingArch
from model.FuzzingPlatform import FuzzingPlatform
#from model.FuzzingConfig import FuzzingConfig
from app import app


db = app.config['db']


class TargetCtrl(Resource):
    def create(self, data):
        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is None:
            return {"err": "invalid request"}, 400

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if platform is None:
            return {"err": "invalid request"}, 400

        try:
            target = FuzzingTarget(data['name'], data['path'], platform, arch)
            if data['visible'] is not None:
                target.visible = data['visible']

            db.session.add(target)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return target.as_dict(), 201

    def read(self, id):
        target = FuzzingTarget.query.filter_by(id=id).first()
        if target is None:
            return {"err": "not found"}, 404
        return target.as_dict(), 200

    def update(self, id, data):
        target = FuzzingTarget.query.filter_by(id=id).first()
        if target is None:
            return {"err": "not found"}, 404

        if data['name'] is not None:
            target.name = data['name']

        if data['path'] is not None:
            target.path = data['path']

        if data['visible'] is not None:
            target.visible = data['visible']

        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is not None:
            target.platform = platform

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if arch is not None:
            target.arch = arch

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return target.as_dict(), 201

    def delete(self, id):
        target = FuzzingTarget.query.filter_by(id=id).first()
        if target is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(target)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        targets = FuzzingTarget.query.offset(offset).limit(limit).all()
        targets = [t.as_dict() for t in targets]
        return targets, 200

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
            parser.add_argument('visible', type=int, location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('path', location='json')
            parser.add_argument('visible', type=int, location='json')
            parser.add_argument('platform_id', location='json')
            parser.add_argument('arch_id', location='json')
            return self.update(id, parser.parse_args())

