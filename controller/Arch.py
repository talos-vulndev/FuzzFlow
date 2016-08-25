from flask_restful import Resource, reqparse
from model.FuzzingArch import FuzzingArch
from app import app

db = app.config['db']

class ArchCtrl(Resource):
    def create(self, data):
        try:
            arch = FuzzingArch(data['name'])
            db.session.add(arch)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return arch.as_dict(), 201

    def read(self, id):
        arch = FuzzingArch.query.filter_by(id=id).first()
        if arch is None:
            return {"err": "not found"}, 404
        return arch.as_dict(), 200

    def update(self, id, data):
        arch = FuzzingArch.query.filter_by(id=id).first()
        if arch is None:
            return {"err": "not found"}, 404

        if data['name'] is not None:
            arch.name = data['name']

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return arch.as_dict(), 201

    def delete(self, id):
        arch = FuzzingArch.query.filter_by(id=id).first()
        if arch is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(arch)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        arches= FuzzingArch.query.offset(offset).limit(limit).all()
        arches = [arch.as_dict() for arch in arches]
        return arches, 200

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
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            return self.update(id, parser.parse_args())