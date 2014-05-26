#coding=utf-8
from flask import Flask, render_template
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from flask_peewee.auth import Auth
from flask_peewee.auth import BaseUser
from flask_peewee.db import Database
from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, DateTimeField, BooleanField, DecimalField, IntegerField

from api_resources import ItemResource, UserResource

import datetime

DATABASE = {
	'name' : 'example.db',
	'engine' : 'peewee.SqliteDatabase',
}

DEBUG = True

app = Flask(__name__, static_folder='static', static_url_path='') # création de l'appli Flask
app.config.from_object(__name__)

db = Database(app)

class UserBidule(db.Model):
	name = CharField()

class WishList(db.Model):
	name = CharField()
	description = CharField()
	validity_date = DateField()
	user = ForeignKeyField(UserBidule, related_name='wishlists')

class Item(db.Model):
	name = CharField()
	description = CharField(max_length=2000, null=True)
	url = CharField()
	price = DecimalField(max_digits=10, decimal_places=2)
	wishlist = ForeignKeyField(WishList, related_name='items')
	numberOfParts = IntegerField()

class Part(db.Model):
	user = ForeignKeyField(UserBidule, related_name='gifts')
	item = ForeignKeyField(Item, related_name='parts')

auth = Auth(app, db)

user_auth = UserAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)

api.register(WishList)
api.register(Item, ItemResource)
api.register(Part)
api.register(UserBidule, UserResource)

api.setup()

@app.route('/') 
def index():
	return render_template('index.html')
	
if __name__ == '__main__':	 
	auth.User.create_table(fail_silently=True)
	
	UserBidule.create_table(fail_silently=True)
	WishList.create_table(fail_silently=True)
	Item.create_table(fail_silently=True)
	Part.create_table(fail_silently=True)
	
	
	app.run(debug=True)
