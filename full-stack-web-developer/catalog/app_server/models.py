from app_server import db
from sqlalchemy import UniqueConstraint

#### Models ####
""" User table """
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    last_seen = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # if this instance is defined user be authenticated
    def is_authenticated(self):
        return True

    # if this instance is alive user should be active
    def is_active(self):
        return True

    # if this instance is alive, user is not anonymous
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

""" Categories table """
class Categories(db.Model):
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

""" items under each category """
class Items(db.Model):
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

