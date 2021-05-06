from flask import Blueprint

homes = Blueprint("home", __name__)

from . import home
