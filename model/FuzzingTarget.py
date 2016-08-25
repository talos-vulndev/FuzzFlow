from app import app

db = app.config['db']

# fuzzing_target_config = db.Table('fuzzing_target_config ',
#     db.Column('config_id', db.Integer, db.ForeignKey('fuzzing_config.id')),
#     db.Column('target_id', db.Integer, db.ForeignKey('fuzzing_target.id'))
#)


class FuzzingTarget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    path = db.Column(db.String(1024), unique=True, nullable=False)
    visible = db.Column(db.Integer, default=1, nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('fuzzing_platform.id'))
    platform = db.relationship('FuzzingPlatform', foreign_keys=platform_id)
    arch_id = db.Column(db.Integer, db.ForeignKey('fuzzing_arch.id'))
    arch = db.relationship('FuzzingArch', foreign_keys=arch_id)

    #configs = db.relationship('FuzzingConfig', secondary=fuzzing_target_config,
    #                          backref=db.backref('targets', lazy='dynamic'))

    def __init__(self, name, path, platform, arch):
        self.name = name
        self.path = path
        self.platform = platform
        self.arch = arch
        self.visible = 1
        #if configs is not None:
        #    self.configs = configs

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}