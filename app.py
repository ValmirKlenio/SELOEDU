from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return redirect("/")  # simulação de login
    return render_template("auth/login.html")

if __name__ == "__main__":
    app.run(debug=True)
