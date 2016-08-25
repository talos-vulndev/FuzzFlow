from datetime import datetime
from flask_restful import Resource, reqparse
from model.FuzzingHost import FuzzingHost
from model.FuzzingArch import FuzzingArch
from model.FuzzingPlatform import FuzzingPlatform
from controller.Job import JobManager
from app import app


db = app.config['db']


class HostCtrl(Resource):
    def create(self, data):
        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is None:
            return {"err" : "invalid request"}, 400

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if platform is None:
            return {"err" : "invalid request"}, 400

        try:
            host = FuzzingHost(data['name'], data['mac'], data['ip'], platform, arch)
            db.session.add(host)
            db.session.commit()
        except Exception as e:
            return {"err" : "invalid request"}, 400

        return host.as_dict(), 201

    def read(self, id, by=None):
        if by == 'mac':
            host = FuzzingHost.query.filter_by(mac=id).first()
        else:
            host = FuzzingHost.query.filter_by(id=id).first()
        if host is None:
            return {"err": "not found"}, 404
        return host.as_dict(), 200

    def update(self, id, data):
        host = FuzzingHost.query.filter_by(id=id).first()
        if host is None:
            return {"err": "not found"}, 404

        host.updated_at = datetime.now()

        if data['name'] is not None:
            host.name = data['name']

        if data['mac'] is not None:
            host.mac = data['mac']

        if data['ip'] is not None:
            host.ip = data['ip']

        platform = FuzzingPlatform.query.filter_by(id=data['platform_id']).first()
        if platform is not None:
            host.platform = platform

        arch = FuzzingArch.query.filter_by(id=data['arch_id']).first()
        if arch is not None:
            host.arch = arch

        try:
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return host.as_dict(), 201

    def delete(self, id):
        host = FuzzingHost.query.filter_by(id=id).first()
        if host is None:
            return {"err": "not found"}, 404
        try:
            db.session.delete(host)
            db.session.commit()
        except Exception as e:
            return {"err": "invalid request"}, 400

        return {"msg" : "record removed successfully"}, 201

    def list(self, offset=0, limit=10000):
        hosts = FuzzingHost.query.offset(offset).limit(limit).all()
        hosts = [h.as_dict() for h in hosts ]
        JobManager.assign_jobs()
        return { 'serverTime': str(datetime.now()), 'hosts' : hosts } , 200

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        parser.add_argument('mac', type=int)
        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            else:
                return self.list()
        else:
            if args['delete'] == 1:
                return self.delete(id)
            elif args['mac'] == 1:
                return self.read(id, 'mac')
            else:
                return self.read(id)

    def post(self, id=None):
        parser = reqparse.RequestParser()
        if id is None:
            parser.add_argument('name', required=True, location='json')
            parser.add_argument('mac', required=True, location='json')
            parser.add_argument('ip', required=True, location='json')
            parser.add_argument('platform_id', required=True, location='json')
            parser.add_argument('arch_id', required=True, location='json')
            return self.create(parser.parse_args())
        else:
            parser.add_argument('name', location='json')
            parser.add_argument('mac', location='json')
            parser.add_argument('ip', location='json')
            parser.add_argument('platform_id', location='json')
            parser.add_argument('arch_id', location='json')
            return self.update(id, parser.parse_args())