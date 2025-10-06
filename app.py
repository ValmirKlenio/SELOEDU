from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User
from views.auth import auth_bp
from views.users import users_bp


app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@seloedu.com").first():
        user = User(nome="Admin", email="admin@seloedu.com", role="master")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()
        print("Usuário admin criado com sucesso!")

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)