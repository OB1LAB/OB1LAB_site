from app import app
from app.models import User
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from flask import render_template, flash, redirect, url_for, request
from app.config import private_routes


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'OB1CHAM'}
    return render_template('index.html', title="OB1LAB", user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин/Пароль')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/private_logs/<date>', methods=['GET', 'POST'])
def private_logs(date):
    return date


@app.before_request
def before_request():
    if request.endpoint in private_routes:
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.path))
        if not current_user.have_permission(private_routes[request.endpoint]):
            return 'Ю донт хэв пермишенс'
