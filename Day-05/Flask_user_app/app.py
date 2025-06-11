from flask import Flask, request, render_template, jsonify
from users import users  # ✅ Import the dictionary from users.py

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/user/<username>')
def user_profile(username):
    user = users.get(username.lower())
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user_form', methods=["GET", "POST"])
def user_form():
    if request.method == "POST":
        username = request.form['username'].lower()
        user = users.get(username)
        if user:
            return render_template("user_result.html", user=user)
        else:
            return render_template("user_result.html", user=None, username=username)
    return render_template("user_form.html")

if __name__ == '__main__':
    app.run(debug=True)
