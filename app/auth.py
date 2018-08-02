from datetime import timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from app.models import User

class SingUp(Resource):
    """
        This is resource used to register new users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
                                 type=str, required=True,
                                 help='username is required!'
                                )
        self.parser.add_argument('email',
                                 type=str, required=True,
                                 help="Email is required"
                                )
        self.parser.add_argument('password',
                                 type=str, required=True,
                                 help="password is required"
                                )
        self.parser.add_argument('confirm_password',
                                 type=str, required=True,
                                 help="confirm Password is required"
                                )
    def post(self):
        """ Register a new user """
        data = self.parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        if not len(password) >= 8:
            return{"Server Response":"Password length should altest 8 characters"}, 401
        if not password == confirm_password:
            return {"message":"Double check your password"}, 400
        user = User().get_user_by_email(email)
        if email in str(user):
            return{"Server Response":'User with email: {} exists'.format(email)}, 400
        else:
            new_user = (username, email, password)
            User().save(new_user)
            return{"Server Response":" Hello {}, your account was created".format(username).title()}, 201

class Login(Resource):
    """
        This is resource used to login existing users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email',
                                 type=str, required=True,
                                 help='email is required!'
                                )
        self.parser.add_argument('password',
                                 type=str, required=True,
                                 help="Password is required"
                                )
    def post(self):
        """ This method logins the user and creates an access token """
        data = self.parser.parse_args()
        email = data['email']
        password = data['password']
        db_email = User().match_email(email)
        if not db_email:
            return {"Server Response":"User with email:'{}' does not exist".format(email)}, 400
        if User().verify_password(email, password):
            user_id = User().get_id_by_email(email)
            exp = timedelta(minutes=1440)
            access_token = create_access_token(identity=user_id, expires_delta=exp)
            return {"Welcome to your personal diary, your access token is":access_token}, 200
        return {"Server Response":"Your password was Incorrect, please double check it."}, 400
