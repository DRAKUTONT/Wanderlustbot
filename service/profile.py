from models.models import User


def get_format_user_profile(id: int) -> str:
    user = User.get(User.id == id)

    return f"ID: `{id}`\n{user.name}, {user.age}\n{user.address}\n\n{user.bio}"
