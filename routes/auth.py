from flask import Blueprint
from views import auth as auth_views

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Mapeia rotas para funções definidas no views/auth.py
auth_bp.add_url_rule("/login",  view_func=auth_views.login, methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", view_func=auth_views.logout)