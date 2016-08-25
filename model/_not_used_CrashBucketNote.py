from app import app
from datetime import *

db = app.config['db']


class CrashBucketNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(2048))
    crash_bucket_id = db.Column(db.Integer, db.ForeignKey('crash_bucket_file.id'))
    crash_bucket = db.relationship('CrashBucketFile', foreign_keys=crash_bucket_id)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, note):
        self.note = note

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}