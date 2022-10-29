from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint(__name__,"views")

@views.route("/")
@login_required
def home():
    return render_template("index.html", name="pessoa")

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/go-to-home")
@login_required
def go_to_home():
    return render_template('index.html')

@views.route("/sign-up")
def to_sign_up():
    return render_template('sign_up.html')