from app import app
from datetime import *


db = app.config['db']


fuzzing_engine_option = db.Table('fuzzing_engine_option',
    db.Column('option_id', db.Integer, db.ForeignKey('fuzzing_option.id')),
    db.Column('engine_id', db.Integer, db.ForeignKey('fuzzing_engine.id'))
)

# fuzzing_engine_config = db.Table('fuzzing_engine_config',
#     db.Column('config_id', db.Integer, db.ForeignKey('fuzzing_config.id')),
#     db.Column('engine_id', db.Integer, db.ForeignKey('fuzzing_engine.id'))
# )


class FuzzingEngine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    path = db.Column(db.String(1024), nullable=False)
    visible = db.Column(db.Integer, default=1, nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('fuzzing_platform.id'))
    platform = db.relationship('FuzzingPlatform', foreign_keys=platform_id)
    arch_id = db.Column(db.Integer, db.ForeignKey('fuzzing_arch.id'))
    arch = db.relationship('FuzzingArch', foreign_keys=arch_id)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    options = db.relationship('FuzzingOption', secondary=fuzzing_engine_option,
                              backref=db.backref('engines', lazy='dynamic'))
    #configs = db.relationship('FuzzingConfig', secondary=fuzzing_engine_config,
    #                          backref=db.backref('engines', lazy='dynamic'))

    def __init__(self, name, path, platform, arch, options=None):
        self.name = name
        self.path = path
        self.platform = platform
        self.arch = arch
        if options is not None:
            self.options = options

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
