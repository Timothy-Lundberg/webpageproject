from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Loggar in användaren """
    # Om användaren är inloggad omdirigeras man till index.
    if current_user.is_authenticated:
        return redirect(url_for('user', user_id=current_user.id))
    # Om användaren inte är inloggad.
    form = LoginForm()
    # Här kollar man fall inloggning blivit godkänd.
    if form.validate_on_submit():
        #  Kollar om användaren har skrivit in korrekt lösenord motsvarande till sitt användarnamn.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # next_page sparas för att omredigera användaren vidare efter lyckad inloggning om det finns en next.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', user_id=current_user.id)
        return redirect(next_page)
    return render_template("login.html", title='Sign In', form=form)


@app.route('/logout')
def logout():
    """ Loggar ut användaren """
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Registrerar användaren """
    # Om användaren är inloggad omdirigeras man till index.
    if current_user.is_authenticated:
        return redirect(url_for('user', user_id=current_user.id))
    form = RegistrationForm()
    # Om registreringen godkänns skapas en instans från User-klassen med information från vårat användarformulär
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Här lägger vi till den nya användaren till vår databas.
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a proud member of TBD')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route('/')
@app.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
def user(user_id):

    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(page=user.id).all()
    profiles = User.query.all()
    post_list = []

    for post in posts:
        poster_id = post.user_id
        poster = User.query.filter_by(id=poster_id).first_or_404()
        new_post = {
            'poster': poster.username,
            'body': post.body,
            'user': poster,
            'id': poster_id,
        }
        post_list.append(new_post)

    form = PostForm()
    if form.validate_on_submit():
        post = Post(page=user.id, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("user", user_id=user.id))

    return render_template("user.html", user=user, form=form, posts=post_list, profiles=profiles)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for("edit_profile"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


if __name__ == '__main__':
    app.run()

