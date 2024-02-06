# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_access_cookies

from api.extensions import login_manager
from api.public.forms import LoginForm
from api.user.forms import RegisterForm
from api.user.models import User
from api.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_identity_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id)).id

@login_manager.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    user_id = jwt_data["sub"]
    return User.get_by_id(int(user_id))

@blueprint.route("/", methods=["GET", "POST"])
@jwt_required(optional=True)
def home():
    """Home page."""
    form: LoginForm = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.user.id)
            access_token = create_access_token(identity=int(form.user.id))
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            response = redirect(redirect_url)
            set_access_cookies(response, access_token)
            return response
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@jwt_required()
def logout():
    """Logout."""
    # logout_user()
    flash("You are logged out.", "info")
    response = redirect(url_for("public.home"))
    unset_access_cookies(response)
    return response


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
