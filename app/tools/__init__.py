from flask import Blueprint

blueprint = Blueprint(
    "tools_blueprint",
    __name__,
    url_prefix="/tools",
    template_folder="templates",
    static_folder="static",
)
