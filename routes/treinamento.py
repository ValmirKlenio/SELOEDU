from flask import Blueprint
from views import treinamento as treinamento_views

treinamento_bp = Blueprint('treinamento', __name__, url_prefix="/treinamentos")

treinamento_bp.add_url_rule("/", view_func=treinamento_views.listar, endpoint="listar")
treinamento_bp.add_url_rule("/novo", view_func=treinamento_views.novo, methods=["GET", "POST"], endpoint="novo")
