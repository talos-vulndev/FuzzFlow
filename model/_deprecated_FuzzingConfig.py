from app import app
from model.FuzzingEngine import fuzzing_engine_config
db = app.config['db']


class FuzzingConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('fuzzing_host.id'))
    host = db.relationship('FuzzingHost', foreign_keys=host_id)
    arch_id= db.Column(db.Integer, db.ForeignKey('fuzzing_arch.id'))
    arch = db.relationship('FuzzingArch', foreign_keys=arch_id)
    platform_id= db.Column(db.Integer, db.ForeignKey('fuzzing_platform.id'))
    platform = db.relationship('FuzzingPlatform', foreign_keys=platform_id)

    def __init__(self, host, arch, platform):
        self.host = host
        self.arch = arch
        self.platform = platform

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}