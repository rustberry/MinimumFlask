from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

main = Blueprint('post', __name__)

@main.route('/')
