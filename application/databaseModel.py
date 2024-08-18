import datetime

from flask_login import UserMixin, current_user
from sqlalchemy import Column, String, Boolean, Integer, Text, func, Date

from .extension import db

favorite_association_table = db.Table('favorite_association',
                                      db.Column('user_id', Integer, db.ForeignKey('user.id'), primary_key=True),
                                      db.Column('product_id', Integer, db.ForeignKey('product.id'), primary_key=True)
                                      )


class FavoriteProduct(db.Model):
    __table__ = favorite_association_table


bookmark_association_table = db.Table('bookmark_association',
                                      db.Column('user_id', Integer, db.ForeignKey('user.id'), primary_key=True),
                                      db.Column('review_id', Integer, db.ForeignKey('review.id'), primary_key=True)
                                      )


class Bookmark(db.Model):
    __table__ = bookmark_association_table


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128))
    is_admin = Column(Boolean, default=False)
    is_suspended = Column(Boolean, default=False)
    profile_picture = Column(String(128))

    reviews = db.relationship("Review", backref='reviewed_by')
    favorite_products = db.relationship("Product", secondary=favorite_association_table, backref="users")
    comments = db.relationship("Comment", backref="commented_by")
    bookmarked_reviews = db.relationship("Review", secondary=bookmark_association_table, backref="bookmarked_by")

    def get_unread_notifications(self):
        return Notifications.query.filter_by(user_id=self.id, read=False).order_by(Notifications.id.desc()).limit(
            5).all()

    def get_global_notifications(self):
        return Notifications.query.filter_by(user_id=None).order_by(Notifications.id.desc()).limit(5).all()


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    description = Column(Text)
    category_id = Column(Integer, db.ForeignKey('category.id'))
    price = Column(db.Float)
    purchase_link = Column(String(255))
    image_path = Column(String(255))

    reviews = db.relationship("Review", backref="reviewed_on")

    def average_rating(self):
        return db.session.query(func.avg(Review.rating)).filter(Review.product_id == self.id). \
            filter(Review.status == True).scalar()


class Review(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    rating = Column(db.Float)
    pros = Column(Text)
    cons = Column(Text)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    product_id = Column(Integer, db.ForeignKey('product.id'))
    status = Column(Boolean, default=False)

    comments = db.relationship("Comment", backref="reviewed_on")


class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    description = Column(String(128))

    products = db.relationship("Product", backref="category")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
    user_id = Column(Integer, db.ForeignKey('user.id'))
    review_id = Column(Integer, db.ForeignKey('review.id'))


class Blog(db.Model):
    id = Column(Integer, primary_key=True)
    heading = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Blog {self.heading}>"


class Notifications(db.Model):
    id = Column(Integer, primary_key=True)
    message = Column(String(255))
    for_admin = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    notification_time = Column(Date, default=datetime.datetime.now())
    user_id = Column(Integer, db.ForeignKey('user.id'))

    def assign_to_admin(self):
        self.for_admin = True

    def review_comment_notification(self, review):
        if review.reviewed_by == current_user:
            return

        self.message = f"{current_user.username} commented on your review. {review.content[:10]}..."
        self.user_id = review.reviewed_by.id

        return self

    def product_addition_notification(self, product):
        self.message = f"New Product Added. {product.name}"


class Contacts(db.Model):
    id = Column(Integer, primary_key=True)
    fullname = Column(String(255))
    email = Column(String(255))
    message = Column(Text)
