from apps.users.models import User

def create_user(username, email, password, role=User.Roles.CUSTOMER):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role
    )
    return user

def deactivate_user(user: User):
    user.is_active = False
    user.save()
    return user