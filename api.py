import datetime
import flask
from init import app, db
import models


@app.route('/api/update-check', methods =['POST'])
def update_check():



    print(flask.request.form)
    print('to answer',flask.request.form['followee_id'])

    if 'auth_user' not in flask.session:
        print('not auth user')


        flask.abort(403)


    user_id = flask.session['auth_user']

    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        print('aborting')
        flask.abort(400)



    #get values from request
    followee_id = int(flask.request.form['followee_id'])
    want_to_follow = flask.request.form['want_to_follow']
    nextState = flask.request.form['state']


    if want_to_follow == 'true':
        want_to_follow = True
    else:
        want_to_follow = False


    print('followee id ', followee_id)
    print('want to follow ', want_to_follow)
    print('next state ',nextState)

    print(type(user_id))
    print(type(followee_id))



    #check to see if it is already there:
    follow = models.Follow.query.filter_by(follower_id=user_id, followee_id = followee_id).first()

    print (follow)

    if  follow is None :

        print('now following        >>>>>>>>')

        follow = models.Follow(user_id, followee_id)
        db.session.add(follow)
        db.session.commit()
        return flask.jsonify({'result' : 'ok'})
    else:

        db.session.delete(follow)
        db.session.commit()
        print('now UN-following        >>>>>>>>')
        return flask.jsonify({'result' : 'ok'})





@app.route('/api/newPost', methods =['POST'])
def newPost():


    print("in api: ")
    print(flask.request.form)

    date = datetime.datetime.now()
    creator = flask.session['auth_user']
    entry = flask.request.form['entry']
    url = flask.request.form['url']

    print(" url >>>> api" ,url)
    # posts should be limited to 256 characters,
    if len(entry) > 255:
        return flask.redirect('/home')


    newPost = models.Post(entry, creator, date)

    if url:
        newPost.url = url

    db.session.add(newPost)
    db.session.commit()

    flask.flash('new post submitted! from api with javascript')
    print(flask.request.form)


    return flask.jsonify({'result' : 'ok'})
