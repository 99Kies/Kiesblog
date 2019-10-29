from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional
from flask_ckeditor import CKEditorField
from kiesblog.models import Category

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class PostForm(FlaskForm):
    # 使用CKE模块可能会导致xss攻击，需要在后台服务器处理一遍
    title = StringField('Title', validators=[DataRequired(),Length(1,30)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

class CommitForm(FlaskForm):
    # DataRequired判断不能为空，Optional则可以为空
    author = StringField('Name', validators=[DataRequired(), Length(1,30)])
    email = StringField('Email' ,validators=[DataRequired(), Email(), Length(1,255)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0,255)])
    # site 可以为空
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

class AdminForm(FlaskForm):
    author = HiddenField()
    #
    email = HiddenField()
    site = HiddenField()

# class