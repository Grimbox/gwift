#coding=utf-8
from flask import Flask, render_template
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, DateTimeField, BooleanField, DecimalField, IntegerField
from flask_peewee.admin import Admin
from api_resources import ItemResource, UserResource

import datetime
import config


app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(config)

db = Database(app)

auth = Auth(app, db)
user_auth = UserAuthentication(auth)

class WishList(db.Model):
    """
    Defines a new wishlist, created by a specific user (that must be registered).
    This wishlist contains a subset of several items.
    """
	name = CharField()
	description = CharField()
	validity_date = DateField()
	user = ForeignKeyField(auth.User, related_name='wishlists')

class Item(db.Model):
    """
    Defines the item class. 
    An item the following fields : 
        * a name
        * a short description
        * an url if it exists
        * a price
        * and can be split in several parts.
    """
	name = CharField()
	description = CharField(max_length=2000, null=True)
	url = CharField()
	price = DecimalField(max_digits=10, decimal_places=2)
	wishlist = ForeignKeyField(WishList, related_name='items')
	numberOfParts = IntegerField()

class Part(db.Model):
    """
    A part is the smallest subdivision of an item.
    Thanks to this, an item can be bought by several different users.
    """
	user = ForeignKeyField(auth.User, related_name='gifts')
	item = ForeignKeyField(Item, related_name='parts')

# admin part
admin = Admin(app, auth)

admin.register(WishList)
admin.register(Item)
admin.register(Part)


# api part
api = RestAPI(app, default_auth=user_auth)

api.register(WishList)
api.register(Item, ItemResource)
api.register(Part)

# setup
admin.setup()
api.setup()

@app.route('/') 
def index():
	return render_template('index.html')
	
if __name__ == '__main__':	 
	auth.User.create_table(fail_silently=True)
	
	WishList.create_table(fail_silently=True)
	Item.create_table(fail_silently=True)
	Part.create_table(fail_silently=True)
	app.run(debug=True)
