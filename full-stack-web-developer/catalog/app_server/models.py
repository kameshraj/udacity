from app_server import db
from sqlalchemy import UniqueConstraint

#### Models ####

class User(db.Model):
    """
    Table to hold all user information

    Fields:
        id:         System ID (auto generated)
        nickname:   Nickname returned by OpenID. If none set script will use email
                    ID (with out domain)
        email:      Email address of the user
        created_on: UTC time when users was 1st added to our system
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    last_seen = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def is_authenticated(self):
        """
        True if user is authenticated. Which is always true if this instance exists
        """
        return True

    def is_active(self):
        """
        True if user is active. Which is always true if this instance exists
        """
        return True

    def is_anonymous(self):
        """
        False if user is not anonymous. If this instance is alive user is not anonymous
        """
        return False

    def get_id(self):
        """
        Return user ID of this user
        """
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Categories(db.Model):
    """
    Table to hold all Category in our catalog

    Fields:
        id:         System ID (auto generated)
        name:       Name of the category
        created_by: User ID of user who created this item
        created_on: UTC time when this category was created
        updated_on: UTC time when this category was last updated
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # back reference
    user = db.relationship(User, backref=db.backref("categories", lazy="dynamic"))

    def __repr__(self):
        return '<Category %r>' % self.name

class Items(db.Model):
    """
    Table to hold all Item in our catalog

    Fields:
        id:          System ID (auto generated)
        name:        Name of the Item
        category_id: Category ID for this item
        created_by:  User ID of user who created this item
        created_on:  UTC time when this category was created
        updated_on:  UTC time when this category was last updated
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.String(1000), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, index=True, default=db.func.now(), onupdate=db.func.now())

    # back reference
    category = db.relationship(Categories, backref=db.backref("items", lazy="dynamic"))
    user = db.relationship(User, backref=db.backref("items", lazy="dynamic"))

    # item must be unique with a category
    _table_args__ = (UniqueConstraint('name', 'category_id'))

    def __repr__(self):
        return '<Item %r>' % self.name

