from app import app
from datetime import datetime

db = app.config['db']


class FuzzingHost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    mac = db.Column(db.String(64), unique=True, nullable=False)
    ip = db.Column(db.String(32), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('fuzzing_platform.id'))
    platform = db.relationship('FuzzingPlatform', foreign_keys=platform_id)
    arch_id = db.Column(db.Integer, db.ForeignKey('fuzzing_arch.id'))
    arch = db.relationship('FuzzingArch', foreign_keys=arch_id)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(),
                           onupdate=datetime.now())

    def __init__(self, name, mac, ip, platform, arch):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.platform = platform
        self.arch = arch

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}