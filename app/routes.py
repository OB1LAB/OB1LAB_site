from app import app
from app.models import User
from app.forms import LoginForm, RolePermission
from app.api import os, date_sort, get
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, request
from app.config import private_routes, public_logs_servers_list, colors_codes, route_data


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="OB1LAB", route_data=route_data)


@app.route('/api/<parameter>', methods=['GET', 'POST'])
def api(parameter, post_data=None):
    if request.method == 'POST':
        post_data = request.get_json(request.json)
    return get(parameter, post_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form, route_data=route_data)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/public_logs', methods=['GET', 'POST'])
def public_logs_servers():
    return render_template('public_logs_servers.html', title="Публичные логи", servers=public_logs_servers_list,
                           route_data=route_data)


@app.route('/public_logs/<server>', methods=['GET', 'POST'])
def public_logs_dates(server):
    if server not in public_logs_servers_list:
        return render_template('error.html', text=f'{server} не найден в списке серверов', title='Error 404',
                               route_data=route_data), 404
    return render_template('public_logs_dates.html', title=server, server=server,
                           dates=date_sort(os.listdir(f'logs/public/{server}')), route_data=route_data)


@app.route('/public_logs/<server>/<date>', methods=['GET', 'POST'])
def public_logs(server, date):
    if server not in public_logs_servers_list or date not in os.listdir(f'logs/public/{server}'):
        return render_template('error.html', text=f'{server} не надйен в списке серверов, либо {date} нет в списке дат',
                               title='Error 404', route_data=route_data), 404
    return render_template('public_logs.html', title=server, route_data=route_data,
                           logs=''.join(open(f'logs/public/{server}/{date}', 'r', encoding='utf-8').readlines()))


@app.route('/private_logs', methods=['GET', 'POST'])
@login_required
def private_logs():
    return render_template('private_logs_dates.html', title="UltimaTech", server='UltimaTech', route_data=route_data,
                           dates=date_sort(os.listdir('logs/private/UltimaTech')))


@app.route('/private_logs/<date>', methods=['GET', 'POST'])
@login_required
def private_logs_date(date):
    if date not in os.listdir(f'logs/private/UltimaTech'):
        return render_template('error.html', text='Данная дата не найдена', title='Error 404', route_data=route_data,
                               ), 404
    logs = open(f'logs/private/UltimaTech/{date}', 'r', encoding='utf-8').read()
    for color in colors_codes:
        logs = logs.replace(color, colors_codes[color])
    logs = [log for log in logs.splitlines() if 'Tried to add entity minecraft' not in log]
    return render_template('private_logs.html', title="UltimaTech", logs=logs, route_data=route_data)


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(login=username).first_or_404()
    role = user.get_max_role()
    if user.avatar:
        path_image = url_for('static', filename=f'css/images/users/{username}/avatar.png')
    else:
        path_image = f'https://skins.mcskill.net/?name={username}&mode=5&fx=128&fy=128'
    return render_template('profile.html', title=username, route_data=route_data, name=username, rank=role['name'],
                           color=role['color'], register_time=user.get_register(), path_image=path_image)


@app.route('/activity_check', methods=['GET', 'POST'])
def activity_check():
    return render_template('activity_check.html', title='Игровая активность', route_data=route_data)


@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    return render_template('admin_panel.html', title='Админ панель', route_data=route_data)


@app.route('/admin_panel/<parameter>', methods=['GET', 'POST'])
@login_required
def admin_panel_act(parameter):
    if parameter not in route_data['admin_panel']:
        return render_template('error.html', text='По данному адресу ничего не найдено', title='Error 404',
                               route_data=route_data), 404
    if not current_user.have_permission(route_data['admin_panel'][parameter]['perm']):
        return render_template('error.html', text='Ю донт хэв пермишенс, куда ты лезешь, зачем?', title='Error 403',
                               route_data=route_data), 403
    form = RolePermission()
    return render_template(f'{parameter}.html', title=route_data['admin_panel'][parameter]['name'], form=form,
                           route_data=route_data)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('error.html', text='По данному адресу ничего не найдено', title='Error 404',
                           route_data=route_data), 404


@app.errorhandler(500)
def internal_error(_):
    return render_template('error.html', text='Внутренняя ошкибка сервера. Сообщите об этом OB1CHAM#7049',
                           title='Error 500', route_data=route_data), 500


@app.before_request
def before_request():
    if len(request.path.split('/')):
        path = request.path.split('/')[1]
    else:
        path = request.endpoint
    if path in private_routes:
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.path))
        if not current_user.have_permission(private_routes[path]['perm']):
            return render_template('error.html', text='Ю донт хэв пермишенс, куда ты лезешь, зачем?', title='Error 403',
                                   route_data=route_data), 403
