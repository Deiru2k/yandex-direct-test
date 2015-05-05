from crypt import mksalt
import datetime
import functools
from hashlib import sha256

from tornado.gen import coroutine

from bson import ObjectId
from bson.errors import InvalidId
from tornado_resource.resource import APIError


def hash_password(password, salt):

    password_hashed = sha256(password).hexdigest()
    password_plus_salt = password_hashed + salt
    password_salted = sha256(password_plus_salt.encode("UTF-8")).hexdigest()
    return password_salted


def salt_password(password):

    salt = mksalt()
    password_salted = hash_password(password, salt)
    return password_salted, salt


def authenticated_async(group="users"):
    def decorator(f):
        @functools.wraps(f)
        @coroutine
        def wrapper(self, *args, **kwargs):
            self._auto_finish = False
            session_key = self.request.headers.get("Authorization", None)
            if not session_key:
                raise APIError(code=401, message="Not Authorized")
            try:
                session_key = ObjectId(session_key)
            except InvalidId:
                raise APIError(code=400, message="Bad Authorization Token")
            session = yield self.db.sessions.find_one(session_key)
            if not session:
                raise APIError(code=401, message="Not Authorized")
            treshold = datetime.datetime.now() - datetime.timedelta(days=30)
            if session['updatedAt'] < treshold:
                yield self.db.sessions.remove(session_key)
                raise APIError(code=401, message="Session expired", data=str(session_key))
            user = yield self.db.users.find_one({"username": session['user']})
            if not user:
                yield self.db.sessions.remove(session_key)
                raise APIError(code=404, message="User was not found for this session", data=str(session_key))
            if group not in user['groups']:
                raise APIError(code=403, message="Resource is inaccessible by this user", data=str(session_key))
            del user['password']
            del user['salt']
            setattr(self, 'user', user)
            setattr(self, 'session_key', session_key)
            yield self.db.sessions.update({"id": session_key}, {"$set": {"updatedAt": datetime.datetime.now()}})
            result = yield f(self, *args, **kwargs)
            return result
        return wrapper
    return decorator
