from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    comments = db.relationship('Comments', backref='user', lazy=True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    liked = db.relationship('PitchLike',foreign_keys='PitchLike.user_id', backref='user', lazy='dynamic')
    disliked = db.relationship('PitchDislike',foreign_keys='PitchDislike.user_id', backref='user', lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def like_pitch(self, pitch):
        if not self.has_liked_pitch(pitch):
            like = PitchLike(user_id=self.id, pitch_id=pitch.id)
            dislike = PitchDislike(user_id=self.id, pitch_id=pitch.id)
            db.session.add(like)
            PitchDislike.query.filter_by(
                user_id=self.id,
                pitch_id=pitch.id).delete()
    def unlike_pitch(self, pitch):
        if self.has_liked_pitch(pitch):
            PitchLike.query.filter_by(
                user_id=self.id,
                pitch_id=pitch.id).delete()

    def has_liked_pitch(self, pitch):
        return PitchLike.query.filter(
            PitchLike.user_id == self.id,
            PitchLike.pitch_id == pitch.id).count() > 0

    def dislike_pitch(self, pitch):
        if not self.has_disliked_pitch(pitch):
            dislike = PitchDislike(user_id=self.id, pitch_id=pitch.id)
            like = PitchLike(user_id=self.id, pitch_id=pitch.id)
            db.session.add(dislike)
            PitchLike.query.filter_by(
                user_id=self.id,
                pitch_id=pitch.id).delete()

    def undislike_pitch(self, pitch):
        if self.has_disliked_pitch(pitch):
            PitchDislike.query.filter_by(
                user_id=self.id,
                pitch_id=pitch.id).delete()

    def has_disliked_pitch(self, pitch):
        return PitchDislike.query.filter(
            PitchDislike.user_id == self.id,
            PitchDislike.pitch_id == pitch.id).count() > 0
    

    def __repr__(self):
        return f'User {self.username}'

class PitchLike(db.Model):
    __tablename__ = 'pitch_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

class PitchDislike(db.Model):
    __tablename__ = 'pitch_dislike'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content= db.Column(db.Text, nullable=False)
    pitchtype = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='title', lazy='dynamic')
    likes = db.relationship('PitchLike', backref='pitch', lazy='dynamic')
    dislikes = db.relationship('PitchDislike', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls, category):
        pitches = Pitch.query.filter_by(pitchtype=category).all()
        return pitches
    
    @classmethod
    def get_all_pitches():
        pitches = Pitch.query.all()

        return pitches

    @classmethod
    def get_pitch(cls, id):
        pitch = Pitch.query.filter_by(id=id).first()

        return pitch
    
    @classmethod
    def get_pitches_by_user_id(cls, user_id):
        pitches = Pitch.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(user_id = user_id)

        return pitches

    @classmethod
    def count_pitches(cls, uname):
        user = User.query.filter_by(username=uname).first()
        pitches = Pitch.query.filter_by(user_id=user.id).all()

        pitches_count = 0
        for pitch in pitches:
            pitches_count += 1

        return pitches_count

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch):
        comments = Comments.query.filter_by(pitch_id=pitch).all()
        return comments