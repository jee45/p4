import io
import os
import base64
import random

import flask
import bcrypt
import datetime

import re

#import falseData

from init import app, db
import models

from sqlalchemy import desc
from math import ceil

from random_words import LoremIpsum

#from werkzeug import secure_filename



#Note: Test PER_PAGE, need to change to 25
PER_PAGE = 25


@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


@app.before_request
def setup_user():
    if 'auth_user' in flask.session and flask.session['auth_user'] is not None:
        user = models.User.query.get(flask.session['auth_user'])
        flask.g.user = user



def checkAuth():
    if flask.session['auth_user'] is None:
        return flask.redirect('/')


@app.route('/')
def index():


    flask.session['auth_user'] = None
    return flask.render_template('index.html')


@app.route('/login', methods=['POST'])
def login():


    #if the user and password is filled out,
    if flask.request.form['password'] and flask.request.form['username']:
        p = flask.request.form['password']
        u = flask.request.form['username']



        #see if the user already exists
        user = models.User.query.filter_by(username=u).first()
        post = user.posts

        print("testig posts ", post)
        if user:
            #if they do, take them to the homepage
            password = bcrypt.hashpw(p.encode('utf8'), user.password)
            if password == user.password:

                flask.session['auth_user'] = user.id
                return flask.redirect('/home')


        else:
            #if they dont, send them back
            flask.flash('Invalid user name or password')
            return flask.redirect('/')

    else:
        flask.flash('Invalid user name or password')
        return flask.redirect('/')










@app.route('/createNewUser', methods=['POST'])
def createNewUser():
    # todo
    # get gravatar picture url


    #if the user and password is filled out,
    if flask.request.form['password'] and flask.request.form['username'] and flask.request.form['confirm']:
        if flask.request.form['password'] != flask.request.form['confirm']:
            flask.flash('Password not confirmed')
            return flask.redirect('/')
        else:

            #check to see if the username is in the proper format
            p = flask.request.form['password']
            u = flask.request.form['username']


            regex = '(^[a-zA-Z0-9]+$)'
            match = re.findall(regex, p)

            if not match:
                #warn them,
                flask.flash('your username must have no spaces and no punctuation ')
                #reload page
                return flask.redirect('/')

            #ccheck to see if the username is already taken
            user = models.User.query.filter_by(username=u).first()

            if not user:

                newUser = models.User(p,u)
                newUser.username = u
                newUser.password = bcrypt.hashpw(p.encode('utf8'), bcrypt.gensalt(15))
                db.session.add(newUser)
                db.session.commit()
                flask.session['auth_user'] = newUser.id


                return flask.redirect('/home')
            else:
                flask.flash('That username is already taken. ')
                return flask.redirect('/')

    else:
        flask.flash('Fill out all fields.')
        return flask.redirect('/')


def createVoidPost():
    post = models.Post('none', 0, 0)
    db.session.add(post)
    db.session.commit()

def deleteVoidPost():
    postCount = models.Post.query.filter_by(creator_id = 0).count()

    print(postCount)

    if postCount>0:
        while postCount>0:
            post = models.Post.query.filter_by(creator_id = 0).first()
            db.session.delete(post.id)
            db.session.commit()
    print(postCount)



@app.route('/home')
def home():


    if flask.session['auth_user'] is None:
        user=None
        posts = models.Post.query.order_by(models.Post.date.desc()).all()
        posts = posts[0:20]
        return flask.render_template('home.html',
                                 user =user,
                                 posts=posts
                                 )



    '''

    The home page (/) should display one of the following:

    If the user is not logged in, show the 20 most recent posts
    across all users and allow the user to register an account.

    If the user is logged in, show the 20 most recent posts
    from the users they follow.
    '''

    #checkAuth()


    user = models.User.query.get(flask.session['auth_user'])
    posts=[]


    #createVoidPost()


    for f in  user.following:
        post = models.Post.query.filter(models.Post.creator_id == f.followee.id).order_by(models.Post.date.desc()).all()

        for p in post:
            pp = p
            posts.append(pp)

    posts.sort(key=lambda x: x.date, reverse=True)
    posts = posts[0:25]

    user.posts=user.posts[0:20]
    print(user.posts)

    #deleteVoidPost()
    return flask.render_template('home.html',
                                 user =user,
                                 posts=posts
                                 )



@app.route('/logout')
def logout():
    return flask.redirect('/')





@app.route('/submitNewPost', methods=['POST'])
def submitNewPost():
    # todo

    '''
    Allow users to create new posts.
    Posts should be limited to 256 characters,



    in addition to an optional URL
    (this is a deviation from the Twitter model).
    Implement posting via JavaScript as well;
    when the post has succeeded,
    add it to the top of the timeline.

    Messages can have an accompanying photo.

    To implement this, you may need to use
    a traditional HTML form POST instead of JavaScript.

    If the post has a photo,
    display a (size-restricted)
    version of it with the message.

    '''


    date = datetime.datetime.now()
    creator = flask.session['auth_user']
    entry = flask.request.form['entry']
    url = flask.request.form['url']



    # request.files has uploaded files
    file = flask.request.files['image']


    # check that we think the file is an image file
    if not file.mimetype.startswith('image/'):
        # oops
        # in a good app, you provide a useful error message...
        flask.abort(400)




    # posts should be limited to 256 characters,
    if len(entry) > 255:
        return flask.redirect('/home')


    newPost = models.Post(entry, creator, date)

    newPost.photo_type = file.mimetype

    flask.flash(newPost.photo_type)

    # get the photo content. we read it into a 'BytesIO'
    photo_data = io.BytesIO()

    file.save(photo_data)





    # now, we put the data into the model object
    newPost.photo = photo_data.getvalue()

    if url:
        newPost.url = url

    db.session.add(newPost)
    db.session.commit()

    #count pictures in database

    count = models.Post.query.filter(models.Post.photo!=None).count()

    print("pic count ", count)
    stringq = "pic count " + str(count)
    flask.flash(stringq)

    flask.flash('new post submitted!')
    print(flask.request)



    return flask.redirect('/home')


# a URL handler to return the photo data
@app.route('/<int:post_id>/photo')
def photo(post_id):

    if flask.g.user is None:
        flask.abort(403)

    post = models.Post.query.get_or_404(post_id)

    flask.flash(post.photo_type)

    #return (post.photo, post.photo_type)
    return flask.send_file(io.BytesIO(post.photo))


@app.route('/viewPhoto/<int:post_id>')
def viewPhoto(post_id):
    post = models.Post.query.get_or_404(post_id)

    return flask.render_template('viewPhoto.html', post=post)










@app.route('/editMyProfile')
def editMyProfile():
    # todo
    u = flask.session['auth_user']
    user=models.User.query.get(u)

    return flask.render_template('editMyProfile.html', user=user)









@app.route('/findOtherUsers')
def findOtherUsers():
    user_id = flask.session['auth_user']
    list = models.User.query.all()


    return  flask.render_template('findOtherUsers.html',

                                  list=list,


                                  )



@app.route('/otherUser/<int:otherUserId>')
def otherUser(otherUserId):

    print(otherUserId)
    otherUser = models.User.query.get(otherUserId)


    if flask.session['auth_user']:
        user =  models.User.query.get(flask.session['auth_user'])
        alreadyFollowing = user.isFollowing(otherUser.id)

    else:
        user = None
        alreadyFollowing =False


    posts=[]
    if otherUser:
        if user:
            alreadyFollowing = user.isFollowing(otherUser.id)
            print("already following",alreadyFollowing )

        posts=otherUser.posts[:10]

        return  flask.render_template('otherUser.html',
                                      user=otherUser,
                                      posts=posts,
                                      alreadyFollowing=alreadyFollowing
                                      )

    else:
        flask.flash('something went wrong while looking for the user you requested')
        return flask.redirect('/home')






@app.route('/submitProfileEdits', methods=['POST'])
def submitProfileEdits():

    print(flask.request.form)
    location = ''
    bio = ''

    if flask.request.form['location']:
        location = flask.request.form['location']

    if flask.request.form['bio']:
        bio =  flask.request.form['bio']
    if flask.request.form['gravataremail']:
        gravataremail =  flask.request.form['gravataremail']

    user = models.User.query.get(flask.session['auth_user'])
    if bio != '':
        user.bio = bio
    if location != '':
        user.location = location
    if gravataremail != '':
        user.gravataremail = gravataremail

    db.session.commit()


    return flask.redirect('/home')



@app.route('/fileUpload', methods=['POST'])
def fileUpload():

    photo_data = io.BytesIO()

    print(flask.request)
    return "ok"






















import string
from random import choice



def sequencedStringGenerator( letterSelector, repeats):
    string_val = "".join( string.ascii_lowercase[letterSelector:letterSelector+1] for i in range(repeats))
    return string_val



def createFakeUsers():
    for x in range(10):
        for y in range(10):

            u =  sequencedStringGenerator(y,x)
            print(u)
            user = models.User.query.filter_by(username=u).first()
            print(user)

            if user is None:

                newUser =  models.User(u,bcrypt.hashpw(u.encode('utf8'), bcrypt.gensalt(15)))
                db.session.add(newUser)
                db.session.commit()

            else:
                print('user already exists')

def createFakeRelationships():

    # find out how many users there are.
    count = models.User.query.count()
    print('count', count)
    iterations = 300
    for x in range(iterations):
        # get a random id within the range of the count
        user1Id = random.randint(0, count)

        # get another random id
        user2Id = random.randint(0, count)

        print('uid1', user1Id)
        print('uid2', user2Id)
        # check to see if theres a follow relationship between them already.
        follow = models.Follow.query.filter_by(follower_id=user1Id, followee_id=user2Id).first()
        print(follow)
        #if theres not make one.
        if follow is None:
            f = models.Follow(user1Id, user2Id)
            db.session.add(f)
            db.session.commit()



        else:
            print('already there')


def createFakePosts():
    li = LoremIpsum()
    # find out how many users there are
    count = models.User.query.count()

    iterations = 1000
    for x in range(iterations):
        # get a random id within the range of the count
        user1Id = random.randint(0, count)

        #create a random string
        li = LoremIpsum()
        li.get_sentences(1+ x%2)


        entry = li.get_sentences(1+ x%2)

        print(entry)
        #entry = falseData.randomStringGenerator(x, x)


        #add it as a post
        #post_text, creator_id, date
        newPost = models.Post(entry, user1Id, datetime.datetime.now())
        db.session.add(newPost)
        db.session.commit()

