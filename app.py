from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User
# Garante que importa dos arquivos de views corretos
from views.auth import auth_bp
from views.users import users_bp


app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    # Garante que o usuário seja carregado pelo ID para o Flask-Login
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    # Rota dashboard para usuários logados
    return render_template("dashboard.html")

# INICIALIZAÇÃO E CRIAÇÃO DO USUÁRIO ADMIN
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@seloedu.com").first():
        user = User(nome="Admin", email="admin@seloedu.com", role="master")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        print("Usuário admin criado com sucesso!")

# REGISTRO DOS BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)