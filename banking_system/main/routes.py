from flask import render_template, request, Blueprint
# from flaskblog.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)


# @app.route is decorator and / is routepage
@main.route("/")
@main.route("/home")
def home():
    print("dsfghjk")
    return render_template('home.html', title='homepage')
    # page= request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # return render_template('home.html', posts = posts)

@main.route("/about")
def about():
    return render_template('about.html', title='Abouttitle')
