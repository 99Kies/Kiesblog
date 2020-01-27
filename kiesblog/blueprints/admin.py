from flask import Blueprint, render_template
from flask_login import login_required

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
