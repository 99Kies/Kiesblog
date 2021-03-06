from flask import Blueprint, url_for, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from kiesblog.models import Admin
from kiesblog.forms import LoginForm
from kiesblog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_back(url_for('blog.index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        admin = Admin.query.first()
        if admin:
            # 验证用户名和密码
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Weclome back.', 'info')
                return redirect_back() # 返回上一个页面
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout success.", 'info')
    return redirect_back()

# @auth_bp.route('/')