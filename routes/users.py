from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from flask_login import login_required
from models.user import User
from extensions import db

# CORRIGIDO: O nome do Blueprint deve ser 'users_bp' e o prefixo '/users'
users_bp = Blueprint('users', __name__, url_prefix="/users")

@users_bp.route("/")
@login_required
def index():
    usuarios = User.query.all()
    return render_template("users/index.html", usuarios=usuarios)

@users_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        role = request.form.get("role", "aluno")

        # ADICIONADA: Validação de e-mail duplicado
        if User.query.filter_by(email=email).first():
            flash("Erro: O e-mail já está em uso.", "danger")
            return render_template("users/form.html", nome=nome, email=email, role=role)

        user = User(nome=nome, email=email, role=role)
        # Atenção: Manter senha padrão, mas idealmente deve vir do formulário.
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        # CORRIGIDO: Categoria 'success'
        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("users.index"))
    
    return render_template("users/form.html")