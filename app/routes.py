from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

user = {
        "username": "Luntyy"
    }

posts = [
    {
        'author': {'username': 'Hymon'},
        'body': 'Beautiful HS Luntyy',

    },
    {
        'author': {'username': 'Pendt'},
        'body': "You're insane at the game timoez"
    }
]


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", user=user, title="Home", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template("login.html", title='Sign In', form=form)


if __name__ == '__main__':
    app.run()

