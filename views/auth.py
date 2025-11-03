from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user
from flask_mail import Message
from models.user import User
from extensions import db, mail
from utils.token_utils import generate_token, confirm_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Credenciais inválidas.", "danger")
    
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            msg = Message(
                subject="Redefinição de senha",
                recipients=[user.email],
                body=f"Para redefinir sua senha, acesse: {reset_url}"
            )
            mail.send(msg)

        flash("Se o email estiver cadastrado, enviamos um link de redefinição.", "info")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token")
    if not token:
        flash("Token não fornecido.", "danger")
        return redirect(url_for("auth.forgot_password"))

    email = confirm_token(token)
    if not email:
        flash("Link inválido ou expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first_or_404()

    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            flash("Senha inválida.", "danger")
            return render_template("auth/reset_password.html", token=token)

        user.set_password(password)
        db.session.commit()
        flash("Senha redefinida com sucesso.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)
