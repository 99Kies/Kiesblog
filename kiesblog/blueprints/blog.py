from flask import Blueprint, render_template, request, current_app
from kiesblog.models import Post, Category


blog_bp = Blueprint('blog', __name__)

# @blog_bp.route('/')
# def index():
# # 利用get的方法得到page值
#     page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页面
#     per_page = current_app.config['KIESBLOG_POST_PER_PAGE'] # 每页数量
#     pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
#     # pagination = Post.query.order_by(Post.timestamp.desc()).all() order_by(Post.timestamp.desc()意思是按照Post.timestamp镜像降序（从高到低——从新到老）
#     # 查询执行函数all()换成了paginate(), 它接受的两个最主要的参数分别用来决定把记录分成几页（per_page），返回哪一页的记录（page）
#     # paginate会返回page页的信息
#     posts = pagination.items
#     # 调用items属性返回对应页数的记录
#     return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/', defaults={'page':1})
@blog_bp.route('/page/<int:page>')
def index(page):
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['KIESBLOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)




@blog_bp.route('/about')
def abouit():
    return render_template('blog/about.html')

# @blog_bp.route('/category/<int:category_id>')
# def show_category(category_id):
#     return render_template('blog/category.html')
@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['KIESBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html',category=category, posts=posts)




# @blog_bp.route('/post/<int:post_id>', methods=['GET','POST'])
# def show_post(post_id):
#     return render_template('blog/post.html')

@blog_bp.route('/post/<slug>')
def show_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)




# @blog_bp.route('/post/electric_charge',method=['POST'])
# def electric_charge():
#     return render_template('')