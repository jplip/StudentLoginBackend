import json
from flask import Blueprint, request, jsonify,  make_response
from flask_restful import Api, Resource # used for REST API building
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash


from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')
            coins = 0
            
            
            tracking = body.get('tracking') #validate tracking
            #
            exercise = body.get('exercise') #validate exercise

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, #user name
                      uid=uid, tracking=tracking, exercise=exercise, dob=dob, coins=coins)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            # if dob is not None:
            #     try:
            #         uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
            #     except:
            #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            if tracking is not None:
                uo.tracking = tracking
            
            if exercise is not None:
                uo.exercise = exercise
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                #return jsonify(user.read())
                return user.read()
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            #return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps 
            return (json_ready) 
    class _UD(Resource):        
        def put(self, user_id):
            body = request.get_json()
            user_id = body.get('id')
            if user_id is None:
                return {'message': 'Id not found.'}, 400
            user = User.query.filter_by(id=user_id).first()  # Use filter_by to query by UID
            if user:
                if 'exercise' and 'tracking' in body:
                     user.exercise = body['exercise']
                     user.update()
                     user.tracking = body['tracking']
                     user.update() 
                     return user.read()
                return {'message': 'You may only update tracking or exercise'}, 400
            return {'message': 'User not found.'}, 404    
        def get(self, user_id):
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.read()  # Assuming you have a 'read' method in your User model
            return {'message': 'User not found.'}, 404
            
            # body = request.get_json()
            # user_id = body.get('uid')
            # if user_id is None:
            #     return {'message': 'Id not found.'}, 400
            # user = User.query.get(id = user_id)
            # if body.get('tracking'):
            #     user.update(tracking = body.get('tracking')) 
            #     #return jsonify(user.read())
            #     return user.read()
            # return {'message': 'You may only update tracking.'}, 400

    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            name = body.get('name')
            uid = body.get('uid')
            password = body.get('password')
            dob = body.get('dob')
            exercise = body.get('exercise')
            tracking = body.get('tracking')
            coins = 0
            if exercise is not None:
                new_user = User(name=name, uid=uid, password=password, dob=dob, exercise=exercise, tracking='', coins = coins)
            elif tracking is not None:
                new_user = User(name=name, uid=uid, password=password, dob=dob, exercise = '', tracking=tracking, coins = coins)
            else: 
                new_user = User(name=name, uid=uid, password=password, dob=dob, exercise='', tracking='', coins = coins )
            user = new_user.create()
            # success returns json of user
            if user:
                #return jsonify(user.read())
                return user.read()
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            login_user(user)
            return jsonify(user.read())
        
    # class LoginAPI(Resource):
    #     def post(self):
    #         data = request.get_json()

    #         # Retrieve uid and password from the request data
    #         uid = data.get('uid')
    #         password = data.get('password')

    #         # Check if uid and password are provided
    #         if not uid or not password:
    #             response = {'message': 'Invalid credentials'}
    #             return make_response(jsonify(response), 401)

    #         # Retrieve user by uid from the database
    #         user = User.query.filter_by(_uid=uid).first()

    #         # Check if the user exists and the password is correct
    #         if user and user.is_password(password):
    #             # Perform login operations here (if needed)
                
    #             return make_response(jsonify(response), 200)

    #         response = {'message': 'Invalid UID or password'}
    #         return make_response(jsonify(response), 401)
    class LoginAPI(Resource):
        def post(self):
            data = request.get_json()

            # Retrieve uid and password from the request data
            uid = data.get('uid')
            password = data.get('password')

            # Check if uid and password are provided
            if not uid or not password:
                response = {'message': 'Invalid credentials'}
                return make_response(jsonify(response), 401)

            # Retrieve user by uid from the database
            user = User.query.filter_by(_uid=uid).first()

            # Check if the user exists and the password is correct
            if user and user.is_password(password):
         

                # Construct the response with the user's name included
                response = {
                    'message': 'Logged in successfully',
                    'user': {
                        'name': user.name,  
                        'id': user.id
                    }
                }
                return make_response(jsonify(response), 200)

            response = {'message': 'Invalid UID or password'}
            return make_response(jsonify(response), 401)



    class LogoutAPI(Resource):
        @login_required
        def post(self):
            logout_user()
            return {'message': 'Logged out successfully'}, 200
            
   

                 

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_UD, '/<int:user_id>')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(LoginAPI, '/login')
    api.add_resource(LogoutAPI, '/logout')
    api.add_resource(_Create, '/create')
    
    
    
    