#Main python file for the project
#Used to store sessions and manage user data

#Names: Nicole Song and Kaili Takara
#Date: November 26, 2026

from calculations import *  # Imports all functions from calculations.py
from json_files import *  # Imports all functions from json_files.py
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-secret-key")

#index.html
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #Ask the user to sign in and decide whether to create a new travel planner or access an existing one
        name = request.form.get("name", "").strip()
        passcode = request.form.get("passcode", "").strip()
        if name:
            session["name"] = name
        if passcode:
            session["passcode"] = passcode

        users = load_users()
        if name not in users:
            passcode_exists = False
            for user_name, user_data in users.items():
                if user_data.get("passcode") == passcode:
                    passcode_exists = True
                    usernum = user_name
                    break

            if passcode_exists: #User is a new collaborator of an existing travel planner
                users[usernum]["collaborators"].append(name)
                save_users(users)
            else: #New user and travel planner
                users[name] = {"passcode": passcode, "collaborators": []}
                save_users(users)

    return render_template(
        "index.html",
        name=session.get("name"),
        passcode=session.get("passcode"),
    )

#Allows user to log out
@app.route("/logout")
def logout():
    session.pop("name", None)
    session.pop("passcode", None)
    return redirect(url_for("index"))

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
