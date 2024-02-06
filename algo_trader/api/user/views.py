# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@jwt_required()
def members():
    """List members."""
    return render_template("users/members.html")
