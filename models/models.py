import peewee

from models.base import BaseModel


class Journey(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    about = peewee.TextField(null=True)
    owner = peewee.DeferredForeignKey("User", on_delete="CASCADE")
    stat_time = peewee.DateField()
    end_time = peewee.DateField()

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    class Meta:
        table_name = "journeys"


class Location(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    journey = peewee.ForeignKeyField(
        Journey,
    )

    class Meta:
        table_name = "locations"


class User(BaseModel):
    id = peewee.BigIntegerField(primary_key=True)
    name = peewee.CharField()
    age = peewee.IntegerField()
    country = peewee.CharField()
    city = peewee.CharField(null=True)
    bio = peewee.TextField(null=True)
    journeys = peewee.ManyToManyField(
        Journey,
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    class Meta:
        table_name = "users"
