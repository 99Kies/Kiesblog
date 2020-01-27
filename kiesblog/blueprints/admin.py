from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required
from kiesblog.models import Post, Admin, Category, Comment, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings')
@login_required
# login_required 只有登陆了才能访问到这个东西  若无登陆进行请求则进入视图保护
def settings():
    print("hello")
    return render_template('admin/settings.html')

# @admin_bp.before_request
# @login_required
# def login_protect():
#     '''
#     给整个admin_bp子目录添加视图保护
#     '''
#     pass

@admin_bp.route('/post/delete/<id>', methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    post.delete()
    return redirect(url_for('blog.index'))

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["KIESBLOG_MANAGE_POST_PER_PAGE"]
    )
    posts = pagination.items
    # 每页的文章信息
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)