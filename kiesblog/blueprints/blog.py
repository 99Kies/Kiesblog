from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect
from flask_login import current_user
from kiesblog.extensions import db, login_manager
from kiesblog.models import Post, Category, Comment
from kiesblog.forms import AdminCommentForm, CommentForm
from kiesblog.email import send_new_reply_email, send_new_comment_email


blog_bp = Blueprint('blog', __name__)
login_manager.login_view = 'login'

@blog_bp.route('/', defaults={'page':1})
@blog_bp.route('/page/<int:page>')
def index(page):
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['KIESBLOG_POST_PER_PAGE'])
    # pagination = Post.query.order_by(Post.timestamp.desc()).all() order_by(Post.timestamp.desc()意思是按照Post.timestamp镜像降序（从高到低——从新到老）
    # 查询执行函数all()换成了paginate(), 它接受的两个最主要的参数分别用来决定把记录分成几页（per_page），返回哪一页的记录（page）
    # paginate会返回page页的信息
    posts = pagination.items
    # 调用items属性返回对应页数的记录
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')



@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    # 通过get_or_404方法查询指定id的记录, 如果没有找到, 返回404错误
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['KIESBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts=pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)

# @blog_bp.route('/post/<int:post_id>', methods=['GET','POST'])
# def show_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     page = request.args.get('page',1, type=int)
#     per_page = current_app.config['KIESBLOG_COMMENT_PER_PAGE']
#     pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page, per_page)
#     comments = pagination.items
#     return render_template('blog/post.html', post=post, pagination=pagination, comments=comments)


@blog_bp.route('/post/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['KIESBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['KIESBLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(author=author, email=email, body=body, from_admin=from_admin, reviewed=reviewed, post=post)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            send_new_comment_email(post)
        return redirect(url_for('.show_post',post_id=post.id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post',post_id=comment.post_id, reply=comment_id, author=comment.author)+'#comment-form')