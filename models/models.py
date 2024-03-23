import peewee

from models.base import BaseModel


class Journey(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    about = peewee.TextField(null=True)
    owner = peewee.DeferredForeignKey("User", on_delete="CASCADE")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    class Meta:
        table_name = "journeys"


class Location(BaseModel):
    id = peewee.PrimaryKeyField()
    address = peewee.CharField()
    lat = peewee.CharField()
    lon = peewee.CharField()
    start_date = peewee.DateField()
    end_date = peewee.DateField()
    journey = peewee.ForeignKeyField(
        Journey,
        on_delete="CASCADE",
    )

    class Meta:
        table_name = "locations"

    def __repr__(self) -> str:
        return f"<Location {self.address}>"


class User(BaseModel):
    id = peewee.BigIntegerField(primary_key=True)
    name = peewee.CharField()
    age = peewee.IntegerField()
    address = peewee.CharField()
    lat = peewee.CharField()
    lon = peewee.CharField()
    bio = peewee.TextField(null=True)
    journeys = peewee.ManyToManyField(
        Journey,
        backref="users",
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    class Meta:
        table_name = "users"


class Note(BaseModel):
    id = peewee.PrimaryKeyField()
    title = peewee.CharField()
    text = peewee.TextField(null=True)
    file_id = peewee.CharField(250, null=True)
    is_private = peewee.BooleanField(default=False)
    journey = peewee.ForeignKeyField(
        Journey,
        on_delete="CASCADE",
    )

    def __repr__(self) -> str:
        return f"<Note {self.title}>"

    class Meta:
        table_name = "notes"
