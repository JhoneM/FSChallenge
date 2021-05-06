from flask import Blueprint

auths = Blueprint("auth", __name__)

from . import auth
