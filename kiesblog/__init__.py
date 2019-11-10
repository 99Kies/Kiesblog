import os
import click
from flask import Flask, template_rendered, render_template
from kiesblog.settings import config
from kiesblog.extensions import bootstrap, db, moment, mail, ckeditor, login_manager
# from kiesblog.blueprints import auth, admin, blog
from kiesblog.blueprints.admin import admin_bp
from kiesblog.blueprints.auth import auth_bp
from kiesblog.blueprints.blog import blog_bp
from kiesblog.fakes import db, fake_comments, fake_posts, fake_categories, fake_admin
from kiesblog.models import Admin, Post, Comment, Category

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        # if not set config_name ,than use development config
    # print(config_name)
    app = Flask('kiesblog')

    app.config.from_object(config[config_name])
    # app.debug=True
    # app.config.update(DEBUG=True)
    # 注册函数
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    return app

def register_logging(app):
    pass

def register_extensions(app):
    # 要分开实例化模块，这样是为了避免引包重复
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    # app.register_blueprint(blog.blog_bp)
    # app.register_blueprint(admin.admin_bp, url_prefix='/admin')
    # app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comment, default is 500')
    def forge(category, post, comment):

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categoried...' % category)
        fake_categories()

        click.echo('Generating %d posts...' % post)
        fake_posts()

        click.echo('Generating %d comments...' % comment)
        fake_comments()

        click.echo('Done.')




def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def not_found_page(e):
        return render_template('errors/404.html'), 404


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    # 定义模板上下文
    @app.context_processor
    def make_template_context():
        # 博主的数据和分类信息要放到模板上下文中，
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin,categories=categories)



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)