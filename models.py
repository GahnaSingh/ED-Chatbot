from db_setup import db  # Import db from db_setup

class UserQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)

