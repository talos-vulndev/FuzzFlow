from app import app

db = app.config['db']


class FuzzingJobOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('fuzzing_job.id'))
    job = db.relationship('FuzzingJob', foreign_keys=job_id)
    option_id = db.Column(db.Integer, db.ForeignKey('fuzzing_option.id'))
    option = db.relationship('FuzzingOption', foreign_keys=option_id)
    value = db.Column(db.String(256), nullable=False)


    def __init__(self, job, option, value):
        self.job = job
        self.option = option
        self.value = value

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}