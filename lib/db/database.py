from google.appengine.ext import db
from google.appengine.api import memcache
import hashlib

def get_user(num):
    if num:
        user = memcache.get(str(num))
        if not user:
            user = User.get_by_id(int(num))
            if user:
                memcache.set(str(num), user)
        return user
def update_user(user):
    memcache.set(str(user.key().id()), user)
    
def gravatar(email, size=100, rating='g', default='retro', force_default=False,
             force_lower=False, use_ssl=True):
    if not email: email = ""
    if use_ssl:
        url = "https://secure.gravatar.com/avatar/"
    else:
        url = "http://www.gravatar.com/avatar/"
    if force_lower:
        email = email.lower()
    hashemail = hashlib.md5(email).hexdigest()
    link = "{url}{hashemail}?s={size}&d={default}&r={rating}".format(
        url=url, hashemail=hashemail, size=size,
        default=default, rating=rating)
    if force_default:
        link = link + "&f=y"
    return link

    
class User(db.Model):
	firstName = db.StringProperty(required = True)
	lastName = db.StringProperty(required = True)
	userName = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	birthday = db.DateProperty(required = True)

