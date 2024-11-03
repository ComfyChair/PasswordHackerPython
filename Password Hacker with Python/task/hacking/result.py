from enum import Enum


class Result(Enum):
    WRONG_LOGIN = "Wrong login!"
    WRONG_PASSWORD = "Wrong password!"
    BAD_REQUEST = "Bad request!"  # not a valid JSON format or missing field
    LOGIN_EXCEPTION = "Exception happened during login" # e.g. actual pw starts with provided pw
    SUCCESS = "Connection success!"