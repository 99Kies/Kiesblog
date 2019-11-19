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

