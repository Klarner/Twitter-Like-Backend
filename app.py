from ast import Del
from cgitb import handler
from flask import request
from backend_twitter_like_app import create_app
from flask_restful import Resource, Api, reqparse
from model import Users, Tweets, db, usersSchema, tweetsSchema

app = create_app()
app.app_context().push()
api = Api(app=app)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username of the said account.')
parser.add_argument('password', type=str, help='Password of the said account.')
parser.add_argument('handler', type=str, help='Handler of the said account.')
parser.add_argument('content', type=str, help='The content of the tweet.')

def authenticator(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
    return 404

class Register(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        handler = request.form['handler']
        user = Users(username=username, password=password, handler=handler)
        db.session.add(user)
        db.session.commit()
        # Note, don't send the registration data back to client. Interception is a possiblility, this is just a demo.
        return {'message':'Registration successfully.', 'username':username, 'password':password, 'handler':handler}, 201

class User(Resource):
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first_or_404()
        if user != 404:
            return {'username':user.username, 'handler':user.handler}, 201
        return 404

class AddTweet(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = authenticator(username=username, password=password)
        if user != 404:
            content = request.form['content']
            tweet = Tweets(handler=user.handler, content=content)
            db.session.add(tweet)
            db.session.commit()
            return {'handler': user.handler, 'content':content}, 201
        return 404

class DeleteTweet(Resource):
    def delete(self, tweet_id):
        username = request.form['username']
        password = request.form['password']
        user = authenticator(username=username, password=password)
        if user!= 404:
            tweet = Tweets.query.filter_by(id=tweet_id).first_or_404()
            if tweet != 404 and tweet.handler == user.handler:
                db.session.delete(tweet)
                db.session.commit()
                return {'message':'Tweet has been deleted'}
        return 404

class GetTweet(Resource):
    def get(self, tweet_id):
        tweet = Tweets.query.filter_by(id=tweet_id).first_or_404()
        if tweet != 404:
            return {'handler':tweet.handler, 'content':tweet.content}, 201
        return 404

api.add_resource(Register, '/register/')
api.add_resource(User, '/user/<user_id>/')
api.add_resource(AddTweet, '/addtweet/')
api.add_resource(DeleteTweet, '/deletetweet/<tweet_id>')
api.add_resource(GetTweet, '/gettweet/<tweet_id>/')

if __name__ == "__main__":
    app.run()