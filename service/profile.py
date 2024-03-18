from models.models import User


def get_format_user_profile(id: int) -> str:
    user = User.get(User.id == id)

    return f"{user.name}, {user.age}, {user.city}\n\n{user.bio}"
