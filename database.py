from peewee import *
import config

db = PostgresqlDatabase(database=config.database, user=config.user, password=config.password, host=config.host, port=config.port)


class BaseModel(Model):
    class Meta:
        database = db


class Staff(BaseModel):
    id = PrimaryKeyField(column_name='id', primary_key=True, unique=True)
    institution_id = IntegerField(column_name='institution_id')
    position = IntegerField(column_name='position', default=1)
    name = TextField(column_name='name', null=True)
    slogan = TextField(column_name='slogan', null=True)
    login = TextField(column_name='login')
    password = TextField(column_name='password')
    salt = TextField(column_name='salt')
    email = TextField(column_name='email')
    photo = TextField(column_name='photo', null=True)
    date_job_begin = TextField(column_name='date_job_begin', null=True)
    date_job_end = TextField(column_name='date_job_end', null=True)
    requisites = TextField(column_name='requisites', null=True)
    push_token = TextField(column_name='push_token', null=True)
    push_platform = TextField(column_name='push_platform', null=True)

    class Meta:
        table_name = 'staff'
