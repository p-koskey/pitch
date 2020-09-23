from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,  BooleanField, TextAreaField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Required
from app.models import User, Pitch, Comments

class PitchForm(FlaskForm):
    pitch_title = StringField('Title', validators = [Required()])
    pitch_content = TextAreaField("Create your one minute pitch?", validators = [Required()])
    pitch_type = RadioField('Label', choices = [('promotionpitch', 'Promotion Pitch'), ('interviewpitch', 'Interview Pitch'), ('pickuplines', 'Pick-Up Lines'), ('productpitch', 'Product Pitch')], validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    description = TextAreaField('Add comments', validators = [Required()])
    submit = SubmitField('Submit')

class UpvoteForm(FlaskForm):
    submit = SubmitField()

class Downvote(FlaskForm):
    submit = SubmitField()
