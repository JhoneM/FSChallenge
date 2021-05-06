from flask import Blueprint

web_client = Blueprint("web", __name__, url_prefix="/api")

from . import web
