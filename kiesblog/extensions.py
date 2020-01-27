from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager


login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()

# 分离实例化和初始化, 如果把实例化和初始化放在工厂函数中,就没有全局的扩展对象可以用

@login_manager.user_loader
def load_user(user_id):
    from kiesblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
    # 返回已经注册过的用户信息


login_manager.login_view = 'auth.login'# 指定视图保护的视图函数
# print(login_manager.login_view)
login_manager.login_message_category = 'warning'
# login_manager.login_message = u'请先登录！'
# 当用户没有登陆 却要访问需要登陆的url  就会跳转到视图保护的页面
