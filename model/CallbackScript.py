from app import app

db = app.config['db']


class CallbackScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    path = db.Column(db.String(1024), unique=True, nullable=False)
    visible = db.Column(db.Integer, default=1, nullable=False)

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}