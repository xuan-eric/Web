from flask import Blueprint
bp = Blueprint("admin", __name__)
@bp.route("/admin")
def index():
    return "後台首頁"