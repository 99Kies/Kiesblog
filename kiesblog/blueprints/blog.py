from flask import Blueprint, render_template, url_for

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    return render_template('blog/index.html')

@blog_bp.route('/about')
def abouit():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')

@blog_bp.route('/post/<int:post_id>', method=['GET','POST'])
def show_post(post_id):
    return render_template('blog/post.html')


# @blog_bp.route('/post/electric_charge',method=['POST'])
# def electric_charge():
#     return render_template('')

