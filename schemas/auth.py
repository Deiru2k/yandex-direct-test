from .common import *

create_user = {
    "type": "object",
    "required": ["username", "firstName", "lastName", "password"],
    "properties": {
        "username": string,
        "firstName": string,
        "lastName": string,
        "password": string
    }
}

login = {
    "type": "object",
    "required": ["username", "password"],
    "properties": {
        "username": string,
        "password": string
    }
}
