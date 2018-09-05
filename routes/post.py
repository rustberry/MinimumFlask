from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models import Post
from models import Comment

main = Blueprint('post', __name__)


@main.route('/')
def index():
    posts = Post.all()
    return render_template("post_index.html", posts=posts)


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    Post.new(form)
    return redirect(url_for('.index'))


@main.route('/comment/<int:post_id>', methods=["GET", "POST"])
def comment(post_id):
    post = Post.find(id=post_id)
    comments = Comment.find_all(post_id=post_id)
    if request.method == "GET":
        return render_template("post_comment.html", p=post, comments=comments)
    form = request.form
    Comment.new(form)
    redirect(url_for('.index'))


@main.route('/edit/<int:post_id>', methods=["GET", "POST"])
def edit(post_id):
    pass


@main.route('/delete/<int:post_id>', methods=["GET"])
def delete(post_id):
    pass