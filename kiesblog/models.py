# # -*- coding: utf-8 -*-
from kiesblog.extensions import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    # password hash messages
    blog_title = db.Column(db.String(60))
    # blog title
    blog_sub_title = db.Column(db.String(100))
    # blog sub title
    name = db.Column(db.String(30))
    # name
    about = db.Column(db.Text)
    # about messages

    def __repr__(self):
        return '<Admin: {}>'.format(self.name)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
# Category and Post: One to many relationship

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #这个是外键的意思,mean,category_id <==> category.id, to build category id for relationship with category, category_id : post == one to many
    category = db.relationship('Category', back_populates='posts')
    # comments = db.relationship('Comment', backref='post', cascade='all')  #here bug
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    # to build relationship with comments, comments : post == many to one

    # 一条文章可以多条评论，一个分类可以有多条文章

# Post and Comment: One to many bothway relationship
# so if i del post, comment del too

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # Same with:
    # replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    # cascade='all,delete-orphan')