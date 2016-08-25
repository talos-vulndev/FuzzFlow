from app import app
from datetime import *
from model.FuzzingJobState import FuzzingJobState

db = app.config['db']


class FuzzingJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    output = db.Column(db.String(8192))
    state_id = db.Column(db.Integer, db.ForeignKey('fuzzing_job_state.id'))
    state = db.relationship('FuzzingJobState', foreign_keys=state_id)
    engine_id = db.Column(db.Integer, db.ForeignKey('fuzzing_engine.id'))
    engine = db.relationship('FuzzingEngine', foreign_keys=engine_id)
    target_id = db.Column(db.Integer, db.ForeignKey('fuzzing_target.id'))
    target = db.relationship('FuzzingTarget', foreign_keys=target_id)
    host_id = db.Column(db.Integer, db.ForeignKey('fuzzing_host.id'))
    host = db.relationship('FuzzingHost', foreign_keys=host_id, backref='jobs')


    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, name, state, engine, target):
        self.name = name
        self.state = state
        self.engine = engine
        self.target = target

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}