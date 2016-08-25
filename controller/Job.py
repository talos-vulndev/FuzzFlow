from flask_restful import Resource, reqparse

from model import FuzzingJobOption
from model.FuzzingJobOption import FuzzingJobOption
from model.FuzzingJob import FuzzingJob
from model.FuzzingOption import FuzzingOption
from model.FuzzingJobState import FuzzingJobState
from model.FuzzingEngine import FuzzingEngine
from model.FuzzingTarget import FuzzingTarget
from model.FuzzingHost import FuzzingHost
from app import app
import traceback

db = app.config['db']

class JobCtrl(Resource):
    def create(self, data):
        try:
            job_state= FuzzingJobState.query.filter_by(id=data['state_id']).first()
            if job_state is None:
                return {"err": "invalid request"}, 400

            engine = FuzzingEngine.query.filter_by(id=data['engine_id']).first()
            if engine is None:
                return {"err": "invalid request"}, 400

            target = FuzzingTarget.query.filter_by(id=data['target_id']).first()
            if target is None:
                return {"err": "invalid request"}, 400


            job = FuzzingJob(data['name'], job_state, engine, target)

            host = FuzzingHost.query.filter_by(id=data['host_id']).first()
            if host is not None:
                job.host = host

            db.session.add(job)
            if data['options'] is not None:
                for o in data['options']:
                    option = FuzzingOption.query.filter_by(id=o['id']).first()
                    job_opt = FuzzingJobOption(job, option, o['value'])
                    try:
                        db.session.add(job_opt)

                    except Exception as e:
                        return {"err": "invalid request", "e" : e.message, 'x': 1}, 400

            if data['output'] is not None:
                job.output = data['output']

            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request", "e" : e.message}, 400

        options = FuzzingJobOption.query.filter_by(job_id=job.id).all()
        result = job.as_dict()
        result['options'] = [opt.as_dict() for opt in options]
        JobManager.assign_jobs()
        return result, 201

    def read(self, id, by):
        if by == 'host':
            job = FuzzingJob.query.filter_by(host_id=id).first()
        else:
            job = FuzzingJob.query.filter_by(id=id).first()
        if job is None:
            return {"err": "not found"}, 404
        options = FuzzingJobOption.query.filter_by(job_id=job.id).all()
        result = job.as_dict()
        result['options'] = [opt.as_dict() for opt in options]
        JobManager.assign_jobs()
        return result, 200

    def update(self, id, data):
        job = FuzzingJob.query.filter_by(id=id).first()
        if job is None:
            return {"err": "not found"}, 404

        if data['name'] is not None:
            job.name = data['name']

        if data['output'] is not None:
            job.output = data['output']

        job_state = FuzzingJobState.query.filter_by(id=data['state_id']).first()
        if job_state is not None:
            job.state = job_state

        engine = FuzzingEngine.query.filter_by(id=data['engine_id']).first()
        if engine is not None:
            job.engine = engine

        target = FuzzingTarget.query.filter_by(id=data['target_id']).first()
        if target is not None:
            job.target = target

        host = FuzzingHost.query.filter_by(id=data['host_id']).first()
        if host is not None:
            job.host = host

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        JobManager.assign_jobs()
        return job.as_dict(), 201

    def delete(self, id):
        job = FuzzingJob.query.filter_by(id=id).first()
        if job is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(job)
            options = FuzzingJobOption.query.filter_by(job_id=id).all()
            for opt in options:
                db.session.delete(opt)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        JobManager.assign_jobs()
        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        jobs = FuzzingJob.query.offset(offset).limit(limit).all()
        result = [job.as_dict() for job in jobs]
        for i in xrange(len(jobs)):
            options = FuzzingJobOption.query.filter_by(job_id=jobs[i].id).all()
            result[i]['options'] = [option.as_dict() for option in options]

        JobManager.assign_jobs()
        return result, 200

    def state(self, offset=0, limit=10000):
        states = FuzzingJobState.query.offset(offset).limit(limit).all()
        states = [job.as_dict() for job in states]
        JobManager.assign_jobs()
        return states , 200

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        parser.add_argument('state', type=int)
        parser.add_argument('host', type=int)
        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            elif args['state'] == 1:
                return self.state()
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
            parser.add_argument('name', required=True, location='json')
            parser.add_argument('state_id', required=True, location='json')
            parser.add_argument('engine_id', required=True, location='json')
            parser.add_argument('target_id', required=True, location='json')
            parser.add_argument('options', type=list, location='json')
            parser.add_argument('host_id', location='json')
            parser.add_argument('output', location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('state_id', location='json')
            parser.add_argument('engine_id', location='json')
            parser.add_argument('target_id', location='json')
            parser.add_argument('options', type=list, location='json')
            parser.add_argument('host_id', location='json')
            parser.add_argument('output', location='json')
            return self.update(id, parser.parse_args())


class JobManager():
    @staticmethod
    def assign_jobs():
        jobs = FuzzingJob.query.all()
        hosts = FuzzingHost.query.all()
        for job in jobs:
            state_name = job.state.name
            if state_name == 'Queued':
                for host in hosts:
                    if len(host.jobs) == 0 \
                            and host.platform_id == job.engine.platform_id \
                            and host.arch_id == job.engine.arch_id \
                            and host.platform_id == job.target.platform_id \
                            and host.arch_id == job.target.arch_id:
                        job.host = host
                        job.state = FuzzingJobState.query.filter_by(name='Allocated').first()
                        db.session.commit()

            elif state_name == 'Failed':
                job.host = None
                db.session.commit()

