from app import app
from datetime import *

db = app.config['db']

'''
For simplicity I am just using one simple model for each crash and not using the previous db schema. We may want to move
the crash system to a bugzilla friendly format. Based on the decision on the design of crash analysis (clientside or serverside)
, improvement could be made.
'''


class FuzzingCrash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('fuzzing_job.id'))
    job = db.relationship('FuzzingJob', foreign_keys=job_id)
    repro_file = db.Column(db.String(512), nullable=False)
    dump_file = db.Column(db.String(512), nullable=False)
    dbg_file = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                       nullable=False,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __init__(self, job, repro):
        self.job = job
        self.repro_file = repro


    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}