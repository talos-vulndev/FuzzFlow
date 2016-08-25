from app import app

db = app.config['db']


class FuzzingOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('fuzzing_option_type.id'))
    type = db.relationship('FuzzingOptionType', foreign_keys=type_id)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}