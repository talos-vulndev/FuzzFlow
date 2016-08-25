from app import app

db = app.config['db']


class FuzzingScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    script = db.Column(db.String(8192), nullable=False)
    visible = db.Column(db.Integer, default=1, nullable=False)

    def __init__(self, name, script, visible=1):
        self.name = name
        self.script = script
        self.visible = visible

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}