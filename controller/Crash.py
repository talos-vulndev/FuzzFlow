from flask_restful import Resource, reqparse
from model.FuzzingJob import FuzzingJob
from model.FuzzingCrash import FuzzingCrash
from app import app


db = app.config['db']


class CrashCtrl(Resource):
    def create(self, data):
        job = FuzzingJob.query.filter_by(id=data['job_id']).first()
        if job is None:
            return {"err": "invalid request"}, 400

        try:
            crash = FuzzingCrash(job, data['repro_file'])

            if data['dump_file'] is not None:
                crash.dump_file = data['dump_file']

            if data['dbg_file'] is not None:
                crash.dbg_file = data['dbg_file']

            db.session.add(crash)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return crash.as_dict(), 201


    def read(self, id):
        bucket = FuzzingCrash.query.filter_by(id=id).first()
        if bucket is None:
            return {"err": "not found"}, 404
        return bucket.as_dict(), 200

    def update(self, id, data):
        crash = FuzzingCrash.query.filter_by(id=id).first()
        if crash is None:
            return {"err": "not found"}, 404


        job = FuzzingJob.query.filter_by(id=data['job_id']).first()
        if job is not None:
            crash.job = job

        if data['repro_file'] is not None:
            crash.repro_file= data['dump_file']

        if data['dump_file'] is not None:
            crash.dump_file = data['dump_file']

        if data['dbg_file'] is not None:
            crash.dbg_file = data['dbg_file']
        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return crash.as_dict(), 201


    def delete(self, id):
        crash = FuzzingCrash.query.filter_by(id=id).first()
        if crash is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(crash)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=20):
        crashes = FuzzingCrash.query.offset(offset).limit(limit).all()
        crashes = [c.as_dict() for c in crashes ]
        return crashes, 200

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
            if id is None:
                parser.add_argument('job_id', required=True, location='json')
                parser.add_argument('repro_file', required=True, location='json')
                parser.add_argument('dump_file', location='json')
                parser.add_argument('dbg_file', location='json')
                return self.create(parser.parse_args())
            else:
                parser.add_argument('note', location='json')
                parser.add_argument('repro_file', location='json')
                parser.add_argument('dump_file', location='json')
                parser.add_argument('dbg_file', location='json')
                return self.update(id, parser.parse_args())