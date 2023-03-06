from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Loggar in användaren """
    # Om användaren är inloggad omdirigeras man till index.
    if current_user.is_authenticated:
        return redirect(url_for("user", user_id=current_user.id))
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
            next_page = url_for("user", user_id=current_user.id)
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
        return redirect(url_for('index'))
    form = RegistrationForm()
    # Om registreringen godkänns skapas en instans från User-klassen med information från vårat användarformulär
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Här lägger vi till den nya användaren till vår databas.
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a proud member of MonsterSpace')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
def user(user_id):

    # Sparar vems sida vi är på som en user
    user = User.query.filter_by(id=user_id).first_or_404()
    # Posts för o se vad för posts som finns på sidan
    posts = Post.query.filter_by(page=user.id).all()
    # Laddar in alla användare för att kunna skapa hyperlänkar
    profiles = User.query.all()
    post_list = []

    # Sparar relevant information om "posten" som en lista av dictionaries
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

    # Skapar en post och sparar den i vår databas och sen laddar om sidan
    form = PostForm()
    if form.validate_on_submit():
        post = Post(page=user.id, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("user", user_id=user.id))

    # Skickar med relevant information till vårt user.html fil
    return render_template("user.html", user=user, form=form, posts=post_list, profiles=profiles)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # Om formen gick igenom utan problem
    if form.validate_on_submit():
        # Updaterar användarens username och about_me i databasen
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        # Skickar tillbaka användaren till hens profilsida
        return redirect(url_for("user", user_id=current_user.id))
    # Om det finns inskrivit så läser vi in det från databasen
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


if __name__ == '__main__':
    pass


