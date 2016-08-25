from flask_restful import Resource, reqparse
from model.FuzzingOptionType import FuzzingOptionType
from model.FuzzingOption import FuzzingOption
from app import app

db = app.config['db']


class OptionCtrl(Resource):
    def create(self, data):
        try:
            option_type = FuzzingOptionType.query.filter_by(id=data['option_type_id']).first()
            if option_type is None:
                return {"err": "invalid request"}, 400
            opt = FuzzingOption(data['name'], option_type)
            db.session.add(opt)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return opt.as_dict(), 201

    def read(self, id):
        opt = FuzzingOption.query.filter_by(id=id).first()
        if opt is None:
            return {"err": "not found"}, 404
        return opt.as_dict(), 200

    def update(self, id, data):
        opt = FuzzingOption.query.filter_by(id=id).first()
        if opt is None:
            return {"err": "not found"}, 404

        if data['name'] is not None:
            opt.name = data['name']

        option_type = FuzzingOptionType.query.filter_by(id=data['option_type_id']).first()
        if option_type is not None:
            opt.type = option_type

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return opt.as_dict(), 201

    def delete(self, id):
        opt = FuzzingOption.query.filter_by(id=id).first()
        if opt is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(opt)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        opts = FuzzingOption.query.offset(offset).limit(limit).all()
        opts = [arch.as_dict() for arch in opts]
        return opts , 200

    def type(self):
        types = FuzzingOptionType.query.all()
        types = [arch.as_dict() for arch in types]
        return types, 200

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('type', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            elif args['type'] == 1:
                return self.type()
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
            parser.add_argument('option_type_id', required=True, location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('option_type_id', location='json')
            return self.update(id, parser.parse_args())