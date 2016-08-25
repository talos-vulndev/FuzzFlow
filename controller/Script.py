from flask_restful import Resource, reqparse
from model.FuzzingScript import FuzzingScript
from app import app

db = app.config['db']

class ScriptCtrl(Resource):
    def create(self, data):
        try:
            if data['visible'] is not None:
                script = FuzzingScript(data['name'], data['script'], data['visible'])
            else:
                script = FuzzingScript(data['name'], data['script'])
            db.session.add(script)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return script.as_dict(), 201

    def read(self, id):
        script = FuzzingScript.query.filter_by(id=id).first()
        if script is None:
            return {"err": "not found"}, 404
        return script.as_dict(), 200

    def update(self, id, data):
        script = FuzzingScript.query.filter_by(id=id).first()
        if script is None:
            return {"err": "not found"}, 404

        if data['name'] is not None:
            script.name = data['name']

        if data['script'] is not None:
            script.script = data['script']

        if data['visible'] is not None:
            script.visible = data['visible']

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return script.as_dict(), 201

    def delete(self, id):
        script = FuzzingScript.query.filter_by(id=id).first()
        if script is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(script)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        scripts = FuzzingScript.query.offset(offset).limit(limit).all()
        scripts = [s.as_dict() for s in scripts]
        return scripts, 200

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
            parser.add_argument('script', required=True, location='json')
            parser.add_argument('visible', type=int, location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('script', location='json')
            parser.add_argument('visible', type=int, location='json')
            return self.update(id, parser.parse_args())