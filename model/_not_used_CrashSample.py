from app import app
from datetime import *

db = app.config['db']


class CrashSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(2048))
    job_id = db.Column(db.Integer, db.ForeignKey('fuzzing_job.id'))
    job = db.relationship('FuzzingJob', foreign_keys=job_id)
    bucket_id = db.Column(db.Integer, db.ForeignKey('crash_bucket.id'))
    bucket = db.relationship('CrashBucket', foreign_keys=bucket_id)
    repro_file = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                       nullable=False,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __init__(self, note, job, bucket, iteration, inst, repro):
        if note is not None:
            self.note = note

        self.job = job
        self.bucket = bucket

        if iteration is not None:
            self.iteration = iteration

        if inst is not None:
            self.instruction = inst

        if repro is not None:
            self.repro_file = repro

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}