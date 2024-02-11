# import json
# from flask import Blueprint, request, jsonify,  make_response
# from flask_restful import Api, Resource # used for REST API building
# from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.security import check_password_hash
# from flask import request, Response, current_app
# from flask_restful import Resource
# import jwt
# from __init__ import db

# from datetime import datetime
# from auth_middleware import token_required

# from model.users import User

# user_api = Blueprint('user_api', __name__,
#                    url_prefix='/api/users')

# # API docs https://flask-restful.readthedocs.io/en/latest/api.html
# api = Api(user_api)

# class UserAPI:        
#     class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
#         def post(self): # Create method
#             ''' Read data for json body '''
#             body = request.get_json() 
            
#             ''' Avoid garbage in, error checking '''
#             # validate name
#             name = body.get('name')
#             if name is None or len(name) < 2:
#                 return {'message': f'Name is missing, or is less than 2 characters'}, 400
#             # validate uid
#             uid = body.get('uid')
#             if uid is None or len(uid) < 2:
#                 return {'message': f'User ID is missing, or is less than 2 characters'}, 400
#             # look for password and dob
#             password = body.get('password')
#             dob = body.get('dob')
#             coins = 0
            
            
#             tracking = body.get('tracking') #validate tracking
#             #
#             exercise = body.get('exercise') #validate exercise

#             ''' #1: Key code block, setup USER OBJECT '''
#             uo = User(name=name, #user name
#                       uid=uid, tracking=tracking, exercise=exercise, dob=dob, coins=coins)
            
#             ''' Additional garbage error checking '''
#             # set password if provided
#             if password is not None:
#                 uo.set_password(password)
#             # convert to date type
#             # if dob is not None:
#             #     try:
#             #         uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
#             #     except:
#             #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
#             if tracking is not None:
#                 uo.tracking = tracking
            
#             if exercise is not None:
#                 uo.exercise = exercise
                
#             ''' #2: Key Code block to add user to database '''
#             # create user in database
#             user = uo.create()
#             # success returns json of user
#             if user:
#                 #return jsonify(user.read())
#                 return user.read()
#             # failure returns error
#             return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400
#         def get(self): # Read Method
#             users = User.query.all()    # read/extract all users from database
#             json_ready = [user.read() for user in users]  # prepare output in json
#             return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

                    
#     class _Create(Resource):
#         def post(self):
#             body = request.get_json()
#             # Fetch data from the form
#             name = body.get('name')
#             uid = body.get('uid')
#             password = body.get('password')
#             dob = body.get('dob')
#             exercise = body.get('exercise')
#             tracking = body.get('tracking')
#             coins = 0
#             if exercise is not None:
#                 new_user = User(name=name, uid=uid, password=password, dob=dob, exercise=exercise, tracking='', coins = coins)
#             elif tracking is not None:
#                 new_user = User(name=name, uid=uid, password=password, dob=dob, exercise = '', tracking=tracking, coins = coins)
#             else: 
#                 new_user = User(name=name, uid=uid, password=password, dob=dob, exercise='', tracking='', coins = coins )
#             user = new_user.create()
#             # success returns json of user
#             if user:
#                 #return jsonify(user.read())
#                 return user.read()
#             # failure returns error
#             return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400
        
        
#     class _UD(Resource):       
#             def put(self, user_id):
#                 body = request.get_json()
#                 user_id = body.get('id')
#                 if user_id is None:
#                     return {'message': 'Id not found.'}, 400
#                 user = User.query.filter_by(id=user_id).first()  # Use filter_by to query by UID
#                 if user:
#                     if 'exercise' and 'tracking' in body:
#                         user.exercise = body['exercise']
#                         user.update()
#                         user.tracking = body['tracking']
#                         user.update() 
#                         return user.read()
#                     return {'message': 'You may only update tracking or exercise'}, 400
#                 return {'message': 'User not found.'}, 404    
#             def get(self, user_id):
#                 user = User.query.filter_by(id=user_id).first()
#                 if user:
#                     return user.read()  # Assuming you have a 'read' method in your User model
#                 return {'message': 'User not found.'}, 404  
            
#         # def put(self, user_id):
#         #     '''Update a user'''
#         #     user = User.query.get(user_id)
#         #     if not user:
#         #         return {'message': 'User not found'}, 404
#         #     body = request.get_json()
#         #     user.name = body.get('name', user.name)
#         #     user.uid = body.get('uid', user.uid)
#         #     db.session.commit()
#         #     return user.read(), 200

#         # def delete(self, user_id):
#         #     '''Delete a user'''
#         #     user = User.query.get(user_id)
#         #     if not user:
#         #         return {'message': 'User not found'}, 404
#         #     db.session.delete(user)
#         #     db.session.commit()
#         #     return {'message': 'User deleted'}, 200
           

#     class _Security(Resource):
#         def post(self):
#             try:
#                 body = request.get_json()

#                 if not body:
#                     return jsonify({
#                         "message": "Please provide user details",
#                         "data": None,
#                         "error": "Bad request"
#                     }), 400

#                 uid = body.get('uid')
#                 password = body.get('password')

#                 if uid is None or password is None:
#                     return jsonify({'message': 'User ID or password is missing'}), 400

#                 user = User.query.filter_by(_uid=uid).first()

#                 if not user or not user.is_password(password):
#                     return jsonify({'message': "Invalid user ID or password"}), 400

#                 token = self.generate_token(user)

#                 # Additional response data
                
#                 print("User Object:", user)
#                 response_data = {
#                     "message": f"Authentication for {user._uid} successful",
#                     "data": {
#                         "jwt": token,
#                         "user": {
#                     'name': user.name,
#                     'id': user.id,
#                     'password': user.password
#                 }
#                     }
#                 }

#                 resp = jsonify(response_data)
#                 resp.set_cookie("jwt", token,
#                                 max_age=3600,
#                                 secure=True,
#                                 httponly=True,
#                                 path='/'
#                                 )

#                 return resp

#             except Exception as e:
#                 return jsonify({
#                     "message": "Something went wrong!",
#                     "error": str(e),
#                     "data": None
#                 }), 500

#         def generate_token(self, user):
#             try:
#                 token = jwt.encode(
#                     {"_uid": user._uid},
#                     current_app.config["SECRET_KEY"],
#                     algorithm="HS256"
#                 )
#                 return token
#             except Exception as e:
#                 return jsonify({
#                     "error": "Something went wrong during token generation",
#                     "message": str(e)
#                 }), 500




     


    

        
    
                 

#     # building RESTapi endpoint
#     api.add_resource(_CRUD, '/', '/<int:user_id>')
#     api.add_resource(_UD, '/<int:user_id>')
#     api.add_resource(_Security, '/authenticate')
#     api.add_resource(_Create, '/create')
    
    
    