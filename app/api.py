import os
import requests
from datetime import datetime, timedelta
from flask_login import current_user
from app import db
from app.models import User, Role, Permission
from app.forms import RolePermission
from app.logs_lib import date_sort
from app.activity_check import get_activity
from app.config import public_logs_servers_list, mcskill_url_staff, invalids, staff_settings
all_staff = requests.get(mcskill_url_staff).json()


def get(parameter, post_data=None):
    data = {}
    if parameter == 'get_activity_data':
        users, data['all_players'] = User.query.filter(User.roles.any(Role.name == 'Назначенный состав')).all(), {}
        data['servers'] = {}
        for server in public_logs_servers_list:
            server_logs_dates = date_sort(os.listdir(f'logs/public/{server}'), reverse_date=True, with_txt=False)
            monday = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
            if monday not in server_logs_dates:
                monday = server_logs_dates[0]
            data['servers'][server] = {
                'staff': [],
                'dates': [server_logs_dates[0], server_logs_dates[-1], monday]
            }
        for user in users:
            role = user.get_max_role()
            data['servers']['UltimaTech']['staff'].append(user.login)
            data['all_players'][user.login] = {
                'view': role['view_checker'],
                'color': role['color'],
                'avatar': user.avatar
            }
        for server in all_staff[3:6]:
            data['servers'][invalids[server['title']]]['staff'] = []
            for player in server['moders']:
                data['servers'][invalids[server['title']]]['staff'].append(player['name'])
                if player['name'] not in data['all_players']:
                    data['all_players'][player['name']] = staff_settings[player['group']]
    elif (parameter == 'get_roles'
          and current_user.is_authenticated and current_user.have_permission('Access edit roles')
          and current_user.get_max_role(star=True)['lvl'] == 999):
        form = RolePermission()
        if form.validate_on_submit():
            for role in Role.query.all():
                if role.lvl != 999:
                    data[role.name] = []
                    for permission in role.permissions:
                        data[role.name].append(permission.name)
    elif (parameter == 'update_role'
          and current_user.is_authenticated and current_user.have_permission('Access edit roles')
          and current_user.get_max_role(star=True)['lvl'] == 999):
        form = RolePermission()
        if form.validate_on_submit():
            if post_data['act'] == 'update_role':
                role = Role.query.filter_by(name=post_data['role']).first()
                permission = Permission.query.filter_by(name=post_data['permission']).first()
                if post_data['state'] and permission not in role.permissions:
                    role.permissions.append(permission)
                elif not post_data['state'] and permission in role.permissions:
                    role.permissions.remove(permission)
            if post_data['act'] == 'create_role':
                db.session.add(Role(name='Назначенный состав', color='white', lvl=1, checker_view=True))
            db.session.commit()
    elif parameter == 'get_activity_check' and post_data:
        data = get_activity(post_data['server'], post_data['players'], post_data['date_1'], post_data['date_2'])
    return data
