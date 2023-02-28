from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
# Login_required gör så att enbart inloggade personer kan se "index" sidan.
@login_required
def index():
    return render_template("index.html", title="Home Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Loggar in användaren """
    # Om användaren är inloggad omdirigeras man till index.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Sign In', form=form)


@app.route('/logout')
def logout():
    """ Loggar ut användaren """
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Registrerar användaren """
    # Om användaren är inloggad omdirigeras man till index.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template("user.html", user=user, posts=posts)




if __name__ == '__main__':
    app.run()

