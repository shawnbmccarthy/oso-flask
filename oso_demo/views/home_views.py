from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from sqlalchemy.orm import Session
from oso_demo.models import User
from typing import List, Type

app_views_bp = Blueprint("home", __name__, template_folder="templates")

@app_views_bp.route("/")
def index():
    return render_template("home.html")

@app_views_bp.route("/login", methods=["GET", "POST"])
def login():
    with Session(current_app.engine) as s:
        if request.method == "POST":
            uid = request.form.get("uid")
            user: User | None = s.query(User).filter_by(id=uid).first()
            if user:
                session["uid"] = user.id
                session["username"] = user.name
            return redirect(url_for("home.index"))

        users = s.query(User).all()
        return render_template("login.html", users=users)

@app_views_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
