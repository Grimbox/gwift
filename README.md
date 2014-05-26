Gwift is a simple wishlist application. 

Users are able to create an account based on their email address; from this point, they may contribute to a list submitted by another user, or create a new list that contains a list of elements. Elements are identified by an URL, and can be split in several parts. Each contributer can 'buy' a part for a specific element.

Creating a new user
-------------------

First of all, don't forget to set the `SECRET_KEY` parameter in the `config.py` file: user password will be salted.

```python
from app import auth
auth.User.create_table(fail_silently=True)  # make sure table created.
admin = auth.User(username='admin', email='', admin=True, active=True)
admin.set_password('admin')
admin.save()
```

After this step, you will be able to access the admin area, through the /admin url.
