from app import db, login
from flask_login import UserMixin
from app.OB1L1B import generate_password


permission_role = db.Table(
    'permission_role',
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    permissions = db.relationship('Permission', secondary=permission_role, backref=db.backref('role'))
    lvl = db.Column(db.Integer)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), default=generate_password)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('user'))

    def check_password(self, password):
        return self.password == password

    def have_permission(self, permission):
        permissions = []
        for role in self.roles:
            [permissions.append(permission.name) for permission in role.permissions if permission not in permissions]
        return permission in permissions


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
