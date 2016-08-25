from app import app
from datetime import *

db = app.config['db']


class CrashBucket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    info = db.Column(db.String(512))
    job_id = db.Column(db.Integer, db.ForeignKey('fuzzing_job.id'))
    job = db.relationship('FuzzingJob', foreign_keys=job_id)
    # state_id = db.Column(db.Integer, db.ForeignKey('crash_bucket_state.id'))
    # state = db.relationship('CrashBucketState', foreign_keys=state_id)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                       nullable=False,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __init__(self, name, info, job, state):
        self.name = name
        if info is not None:
            self.info = info
        if job is not None:
            self.job = job
        if state is not None:
            self.state = state

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}