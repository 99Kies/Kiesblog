# from kiesblog.models import Admin, Category, Post, Comment
# from kiesblog.extensions import db
# from faker import Faker
# import random
# from sqlalchemy.exc import IntegrityError
#
# fake = Faker()
#
# # def fake_admin():
# #     # fake admin datebase
# #
# #     admin = Admin(
# #         username = 'admin',
# #         blog_title = 'KiesBlog',
# #         blog_sub_title = 'sub title',
# #         name = 'Mima Kirigoe',
# #         # about = '123'
# #     )
# #     admin.set_password('helloflask')
# #     db.session.add(admin)
# #     db.session.commit()
#
# def fake_admin():
#     admin = Admin(
#         username='admin',
#         blog_title='kiesblog',
#         blog_sub_title="No, I'm the real thing.",
#         name='Mima Kirigoe',
#         about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
#     )
#     db.session.add(admin)
#     db.session.commit()
#
# def fake_categories(count=10):
#     # fake categories datebase, default count is 10
#
#     category = Category(name='Default')
#     db.session.add(category)
#     for i in range(count):
#         category = Category(name=fake.word())
#         db.session.add(category)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#
# def fake_posts(count=50):
#     # fake posts , to create posts, almost 2000 words, we create 50 posts
#
#     for i in range(count):
#         post = Post(
#             title = fake.sentence(),
#             body = fake.text(2000),
#             categoriex = Category.query.get(random.randint(1, Category.query.count()))
#             # mean: from Category random one data
#             # random.randint(a,b[,c])  ...  a is minnumber, b is maxnumber , c is step, function is make a integer in [a,b] step is c.
#         )
#         db.session.add(post)
#     db.session.commit()
#
# def fake_comments(count=500):
#     for i in range(count):
#         comment = Comment(
#             author=fake.name(),
#             email=fake.email(),
#             site=fake.url(),
#             body=fake.sentence(),
#             timestamp=fake.date_time_this_year(),
#             reviewed=True,
#             post=Post.query.get(random.randint(1, Post.query.count()))
#             # mean: from Post random one data
#
#         )
#         db.session.add(comment)
#
#     salt = int(count * 0.1)
#     for i in range(salt):
#         # Unvetted comments
#         comment = Comment(
#             author=fake.name(),
#             email=fake.email(),
#             site=fake.url(),
#             body=fake.sentence(),
#             reviewed=False,
#             timestamp=fake.date_time_this_year(),
#             post=Post.query.get(random.randint(1, Post.query.count()))
#         )
#         db.session.add(comment)
#         comment = Comment(
#             author="123",
#             email="99Kies@github.com",
#             site="github.com",
#             body=fake.sentence(),
#             timestamp=fake.date_time_this_year(),
#             from_admin=True,
#             reviewed=True,
#             post=Post.query.get(random.randint(1,Post.query.count()))
#         )
#         db.session.add(comment)
#     db.session.commit()
#
#     for i in range(salt):
#         comment = Comment(
#             auther=fake.name(),
#             email=fake.email(),
#             site=fake.url(),
#             body=fake.sentence(),
#             timestamp=fake.date_time_this_year(),
#             reviewed=True,
#             replied=Comment.query.get(random.randint(1, Comment.query.count()))
#         )
#         db.session.add(comment)
#     db.session.commit()


# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError
from kiesblog import db
from kiesblog.models import Admin, Category, Post, Comment
fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='kiesblog',
        blog_sub_title="No, I'm the real thing.",
        name='Mima Kirigoe',
        # about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
        about="hello"
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
