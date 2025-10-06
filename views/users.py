from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models.user import User
from extensions import db
from functools import wraps

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            if current_user.role != role:
                flash("Acesso não autorizado. Você precisa ser 'master'.", "danger")
                return redirect(url_for('dashboard')) 
            return f(*args, **kwargs)
        return decorated_function
    return decorator


users_bp = Blueprint('users', __name__, url_prefix="/users")


@users_bp.route("/")
@login_required
@role_required('master')
def index():
    usuarios = User.query.all()
    return render_template("users/index.html", usuarios=usuarios)


@users_bp.route("/<int:user_id>")
@login_required
@role_required('master')
def show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)


@users_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required('master')
def create():
    form_data = None 
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        role = request.form.get("role", "aluno")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Erro: O e-mail já está em uso.", "danger")
            form_data = {'nome': nome, 'email': email, 'role': role}
            return render_template("users/form.html", form_data=form_data)

        user = User(nome=nome, email=email, role=role)
        user.set_password(password) 
        db.session.add(user)
        db.session.commit()
        flash(f"Usuário '{nome}' criado com sucesso!", "success")
        return redirect(url_for("users.index"))
    
    return render_template("users/form.html", form_data=form_data)


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required('master')
def edit(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        user.nome = request.form.get("nome")
        user.email = request.form.get("email")
        
        existing_user = User.query.filter(User.email == user.email, User.id != user_id).first()
        if existing_user:
            flash("Erro: O e-mail já está em uso por outro usuário.", "danger")
            return render_template("users/form.html", user=user) 

        user.role = request.form.get("role")
        
        new_password = request.form.get("password")
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash(f"Usuário '{user.nome}' atualizado com sucesso!", "success")
        return redirect(url_for("users.index"))

    return render_template("users/form.html", user=user)


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@role_required('master')
def delete(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash("Você não pode deletar sua própria conta enquanto estiver logado.", "danger")
        return redirect(url_for("users.index"))

    db.session.delete(user)
    db.session.commit()
    flash(f"Usuário '{user.nome}' excluído com sucesso!", "success")
    return redirect(url_for("users.index"))