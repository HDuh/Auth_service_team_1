from application.models import Permission, Role


def set_permissions(db, role, permissions):
    role.role = [
        Permission(permission_name=permission) for permission in permissions
    ]
    db.session.commit()


def get_access_roles(db):
    return {
        role.role_name: [permission.permission_name for permission in role.role]
        for role in db.session.query(Role).all()
    }


def get_permissions(db):
    return db.session.query(Permission).all()
