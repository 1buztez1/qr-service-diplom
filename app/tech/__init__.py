from flask import Blueprint

bp = Blueprint('tech', __name__)

from app.tech import routes