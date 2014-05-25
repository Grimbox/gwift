#coding=utf-8
from flask import Flask, render_template
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from auth import auth

from api_resources import ItemResource, UserResource
from models import WishList, Item, Part, User

app = Flask(__name__, static_folder='static', static_url_path='') # création de l'appli Flask
	
user_auth = UserAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)

api.register(WishList)
api.register(Item, ItemResource)
api.register(Part)
api.register(User, UserResource)

api.setup()

@app.route('/') 
def index():
	return render_template('index.html')
	
if __name__ == '__main__':	 
	app.run(debug=True)