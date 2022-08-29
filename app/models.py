from app import db, login
from flask_login import UserMixin
from app.OB1L1B import generate_password
from datetime import datetime

permission_role = db.Table('permission_role',
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                           )

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                     )


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(256))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    color = db.Column(db.String(10))
    permissions = db.relationship('Permission', secondary=permission_role, backref=db.backref('role'))
    checker_view = db.Column(db.Boolean)
    lvl = db.Column(db.Integer)

    def set_color(self, color):
        self.color = color
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), default=generate_password)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('user'))
    register_time = db.Column(db.DateTime, index=True, default=datetime.now)
    avatar = db.Column(db.Boolean, default=False)

    def set_avatar(self, file_name):
        self.avatar = file_name
        db.session.commit()

    def update_password(self):
        self.password = generate_password()
        db.session.commit()

    def check_password(self, password):
        return self.password == password

    def have_permission(self, permission):
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission:
                    return True
        return False

    def get_max_role(self, star=False):
        role_name, lvl, color, is_view = 'Игрок', 0, '#BBB', False
        for role in self.roles:
            if not star and role.lvl == 999:
                continue
            if role.lvl > lvl:
                role_name, lvl, color, is_view = role.name, role.lvl, role.color, role.checker_view
        return {'name': role_name, 'color': color, 'view_checker': is_view, 'lvl': lvl}

    def get_register(self):
        return self.register_time.strftime('%d-%m-%Y %H:%M')

    def get_password(self):
        return self.password


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
