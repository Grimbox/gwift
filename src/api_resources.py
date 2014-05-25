from flask_peewee.rest import RestResource, RestrictOwnerResource

class ItemResource(RestrictOwnerResource):
	owner_field = 'wishlist__user'

class UserResource(RestResource):
    exclude = ('password', 'email',)