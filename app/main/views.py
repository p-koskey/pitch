from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitch, Comments, PitchLike,PitchDislike
from . import main
from .forms import UpdateProfile, PitchForm, CommentForm
from flask_login import login_required,current_user
from .. import db,photos

@main.route('/')
def index():
    interview = Pitch.get_pitches('interviewpitch')
    count1 = len(interview)
    product = Pitch.get_pitches('productpitch')
    count2 = len(product)
    promote = Pitch.get_pitches('promotionpitch')
    count3 = len(promote)
    pickup = Pitch.get_pitches('pickuplines')
    count4 = len(pickup)
    pitches = Pitch.query.all()

    comments = Comments.get_comments(Pitch.id)
    print(comments)
    return render_template('index.html', title='Home', interview=interview, product=product, promote=promote, pickup = pickup
    ,count1=count1,count2=count2,count3=count3,count4=count4, pitches=pitches)

@main.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/pitch/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        pitch_title = form.pitch_title.data
        pitch_content = form.pitch_content.data
        pitch_type = form.pitch_type.data

        # Updated pitch instance
        new_pitch = Pitch(title=pitch_title, content=pitch_content, pitchtype = pitch_type, user_id = current_user.id)

        # save review method
        new_pitch.save_pitch()
        return redirect(url_for('.index' ))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title, pitch_form=form, )

@main.route('/pitches/interview_pitches')
def interview_pitches():

    pitches = Pitch.get_pitches('interviewpitch')
    return render_template("interview.html", pitches = pitches)

@main.route('/pitches/product_pitches')
def product_pitches():

    pitches = Pitch.get_pitches('productpitch')

    return render_template("product.html", pitches = pitches)

@main.route('/pitches/pickup_lines')
def pickup_lines():

    pitches = Pitch.get_pitches('pickuplines')

    return render_template("pickup.html", pitches = pitches)

@main.route('/pitches/promotion_pitches')
def promotion_pitches():

    pitches = Pitch.get_pitches('promotionpitch')

    return render_template("promote.html", pitches = pitches)

@main.route('/pitch/view/<pitch_id>', methods=['GET', 'POST'])
def view_pitch(pitch_id):
   

    pitch = Pitch.query.filter_by(id=pitch_id).first()
    
    comments = Comments.get_comments(pitch_id)
    comment_form = CommentForm()
    if current_user.is_authenticated:
        
        if comment_form.validate_on_submit():
            comments = comment_form.description.data

            new_comment = Comments(comment=comments,user_id=current_user.id,pitch_id = pitch_id)

            new_comment.save_comment()
            

        comments = Comments.get_comments(pitch_id)
    return render_template('pitch.html', pitch=pitch, comments=comments, pitch_id=pitch.id, comment_form = comment_form)


@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    

    return render_template("profile/mypitch.html", user=user,pitches=pitches,pitches_count=pitches_count)
 



@main.route('/pitches/<user_id>', methods =['GET'])
def get_pitches_by_user_id(user_id):

    user=User.query.filter_by(id=user_id).first()
    pitches = Pitch.query.filter_by(user_id=user.id).all()

    return render_template("user_pitches.html", user = user, pitches=pitches, user_id=user_id)

@main.route('/like/<int:pitch_id>/<action>')
@login_required
def like_action(pitch_id, action):
    pitch = Pitch.query.filter_by(id=pitch_id).first_or_404()
    if action == 'like':
        current_user.like_pitch(pitch)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_pitch(pitch)
        db.session.commit()
    return redirect(request.referrer)

@main.route('/dislike/<int:pitch_id>/<action>')
@login_required
def dislike_action(pitch_id, action):
    pitch = Pitch.query.filter_by(id=pitch_id).first_or_404()
    if action == 'dislike':
        current_user.dislike_pitch(pitch)
        db.session.commit()
    if action == 'undislike':
        current_user.undislike_pitch(pitch)
        db.session.commit()
    return redirect(request.referrer)
