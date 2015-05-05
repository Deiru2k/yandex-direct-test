import datetime
from tornado.gen import coroutine
from base import BaseHandler
from tornado_resource.validation import validate
from tornado_resource.resource import Resource, APIError
from tornado_resource.crypto import salt_password, hash_password, authenticated_async
import schemas.auth
import schemas.common


class Auth(Resource):
    name = "auth"
    url = "/auth"

    class Handler(BaseHandler):

        @validate(input_schema=schemas.auth.create_user)
        @coroutine
        def post(self):
            now = datetime.datetime.now()
            user = self.db.users.find_one({"username": self.input['username']})
            if user:
                raise APIError(code=401, message="Такой пользователь уже существует", data=self.input['username'])
            self.yb.create_client(
                username=self.input['username'],
                first_name=self.input['firstName'],
                last_name=self.input['lastName']
            )
            self.input['password'], self.input['salt'] = salt_password(self.input['password'])
            self.input['createdAt'], self.input['updatedAt'] = now, now
            yield self.db.users.insert(self.input)
            return 201, self.input['username']


class Login(Resource):
    name = "login"
    url = "/auth/login"

    class Handler(BaseHandler):

        @validate(input_schema=schemas.auth.login)
        @coroutine
        def post(self):
            now = datetime.datetime.now()
            user = yield self.db.users.find_one({"username": self.input['username']})
            if not user:
                raise APIError(code=404, message="Такого пользователя не существует", data=self.input['username'])
            password = hash_password(self.input['password'].encode(), user['salt'])
            if password != user['password']:
                raise APIError(code=401, message="Введенн неправильный пароль")
            session = {"createdAt": now, "updatedAt": now, "user": user['username']}
            session_key = yield self.db.sessions.insert(session)
            return 200, session_key

        @authenticated_async()
        @coroutine
        def delete(self):
            yield self.db.sessions.remove({"_id": self.session_key})
            return 204, None