"""Authentication routes for VoiceExpress."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from .data import USERS, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Handle login via nickname/password."""
    error = ""
    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        password = request.form.get("password", "").strip()
        user = USERS.get(nickname)
        if user and user.password == password:
            session["user"] = nickname
            return redirect(url_for("public.home"))
        error = "Invalid credentials."
    return render_template("login.html", error=error)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup() -> str:
    """Handle lightweight user signup with nickname/password."""
    error = ""
    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        password = request.form.get("password", "").strip()
        if nickname in USERS:
            error = "Nickname already exists."
        elif not nickname or not password:
            error = "Nickname and password are required."
        else:
            USERS[nickname] = User(nickname=nickname, password=password, role="Reader")
            session["user"] = nickname
            return redirect(url_for("public.home"))
    return render_template("signup.html", error=error)


@auth_bp.route("/logout")
def logout() -> str:
    """Log out the current user."""
    session.pop("user", None)
    return redirect(url_for("public.home"))
