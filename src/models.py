#coding=utf-8
from flask_peewee.auth import BaseUser
from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, DateTimeField, BooleanField, DecimalField, IntegerField

import datetime

db = SqliteDatabase('ev.db', threadlocals=True)  # création de la base de données.

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel, BaseUser):
	username = CharField()
	password = CharField()
	email = CharField()
	join_date = DateTimeField(default=datetime.datetime.now)
	active = BooleanField(default=True)
	admin = BooleanField(default=False)

class WishList(BaseModel):
	name = CharField()
	description = CharField()
	validity_date = DateField()
	user = ForeignKeyField(User, related_name='wishlists')

class Item(BaseModel):
	name = CharField()
	description = CharField(max_length=2000, null=True)
	url = CharField()
	price = DecimalField(max_digits=10, decimal_places=2)
	wishlist = ForeignKeyField(WishList, related_name='items')
	numberOfParts = IntegerField()

class Part(BaseModel):
	user = ForeignKeyField(User, related_name='gifts')
	item = ForeignKeyField(Item, related_name='parts')

def create_tables():
	User.create_table()
	WishList.create_table()
	Item.create_table()
	Part.create_table()