import datetime
from sqlalchemy.orm import relationship

from init import db,app
import hashlib



class User(db.Model):
    #__tablename__ = 'jusers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    #email = db.Column(db.String(50))

    location = db.Column(db.String(50))
    bio = db.Column(db.Text)

    gravataremail = db.Column(db.String(50))

    posts = relationship("Post",
                         order_by="desc(Post.date)",
                         primaryjoin="Post.creator_id==User.id")


    following = relationship("Follow",
                         order_by="desc(Follow.id)",
                         primaryjoin="Follow.follower_id==User.id")



    followers = relationship("Follow",
                         order_by="desc(Follow.id)",
                         primaryjoin="Follow.followee_id==User.id")


    def __init__(self,username, password):
        self.username = username
        self.password = password

    def isFollowing(self, otheruserid):
        for f in self.following:
            if f.followee_id == otheruserid:
                return True
        return False




    @property
    def grav_hash(self):
        hash = hashlib.md5()
        hash.update(self.gravataremail.strip().lower().encode('utf8'))
        return hash.hexdigest()


    @property
    def jsonable(self):


        return {
            'id': self.id,
            'grav_hash': self.grav_hash,
            'name': self.name
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(50))
    post_text = db.Column(db.Text)

    url = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', primaryjoin=creator_id == User.id)

    photo = db.Column(db.LargeBinary)
    photo_type = db.Column(db.String(50))


    def __init__(self,post_text, creator_id, date):
        self.post_text = post_text
        self.creator_id = creator_id
        self.date = date


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower = db.relationship('User', primaryjoin=follower_id == User.id)

    followee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followee = db.relationship('User', primaryjoin=followee_id == User.id)


    def __init__(self,follower_id, followee_id ):
        self.follower_id = follower_id
        self.followee_id = followee_id



#create
db.create_all()