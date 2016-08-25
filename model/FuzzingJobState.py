from app import app

db = app.config['db']


class FuzzingJobState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}