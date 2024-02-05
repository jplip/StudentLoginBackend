""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.String)
    _exercise = db.Column(db.JSON, nullable=True)
    _tracking = db.Column(db.JSON, nullable=True)
    _coins = db.Column(db.Integer, nullable=True)
   

#If When I change the schema (aka add a field)….  I delete the .db file as it will generate when it does not exist.
#Do not have a underscore in a website name 
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
   # trackers = db.relationship("Tracker", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, exercise, tracking, dob,  coins,  password="123qwerty" ):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._tracking = tracking
        self.set_password(password)
        self._dob = dob
        self._exercise = exercise
        self._tracking = tracking
        self._coins = coins


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        if password is not None:
            self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        return self._dob
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def tracking(self):
        return self._tracking
    
    @tracking.setter
    def tracking(self, tracking):
        self._tracking = tracking
        
        
    @property
    def exercise(self):
        return self._exercise
    
    @exercise.setter
    def exercise(self, exercise):
        self._exercise = exercise
        
    
    @property
    def age(self):
        today = date.today()
        return 9
        
    @property
    def coins(self):
       return self._coins
     
    @coins.setter  
    def coins(self, coins):
        self._coins = coins
       

        
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "password": self.password,
            "dob": self.dob,
            "age": self.age,
            "exercise": self.exercise,
            "tracking": self.tracking,
            "coins": self.coins
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="",  exercise = "", tracking="", coins="", dob=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(exercise) > 0:
            self.exercise = exercise
        if len(tracking) > 0:
            self.tracking = tracking 
        if coins > 0:
            self.coins = coins
        if dob is not None:
            self.dob = dob    
        db.session.commit()
        return self
    

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        """Tester data for table"""
        users_data = [
            {'name': 'Thomas Edison', 'uid': 'toby', 'password': '123toby', 'dob': date(1847, 2, 11),
             'tracking': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
             'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
             'coins': 0},
            # Add more user data as needed
        ]

        # Add users to the database session with duplicate _uid handling
        for user_data in users_data:
            existing_user = User.query.filter_by(_uid=user_data['uid']).first()

            if existing_user:
                # Handle the case where the user already exists
                print(f"User with _uid '{user_data['uid']}' already exists. Updating user data.")
                existing_user.update(
                    name=user_data['name'],
                    password=user_data['password'],
                    dob=user_data['dob'],
                    tracking=user_data['tracking'],
                    exercise=user_data['exercise'],
                    coins=user_data['coins']
                )
            else:
                # Proceed with inserting the new user
                new_user = User(
                    name=user_data['name'],
                    uid=user_data['uid'],
                    password=user_data['password'],
                    dob=user_data['dob'],
                    tracking=user_data['tracking'],
                    exercise=user_data['exercise'],
                    coins=user_data['coins']
                )
                db.session.add(new_user)

        # Commit the changes to the database
        db.session.commit()
        
        
        


# def initUsers():
#     with app.app_context():
#         """Create database and tables"""
#         db.create_all()

#         """Tester data for table"""
#         users_data = [
#             {'name': 'Thomas Edison', 'uid': 'toby', 'password': '123toby', 'dob': date(1847, 2, 11),
#              'tracking': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'coins': 0},
#             {'name': 'Nicholas Tesla', 'uid': 'niko', 'password': '123niko', 'dob': date(1856, 7, 10),
#              'tracking': '{"userName":"Nicholas Tesla","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'coins': 0},
#             {'name': 'Alexander Graham Bell', 'uid': 'lex', 'dob': date(1856, 7, 10),
#              'tracking': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'coins': 0},
#             {'name': 'Grace Hopper', 'uid': 'hop', 'password': '123hop', 'dob': date(1906, 12, 9),
#              'tracking': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'coins': 0},
#             {'name': 'Eun Lim', 'uid': 'lim', 'password': '123lim', 'dob': date(2007, 12, 9),
#              'tracking': '{"userName":"Eun Lim","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'exercise': '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }',
#              'coins': 0}
#         ]

#         # Add users to the database session with duplicate _uid handling
#         for user_data in users_data:
#             existing_user = User.query.filter_by(_uid=user_data['uid']).first()

#             if existing_user:
#                 # Handle the case where the user already exists (update or return an error)
#                 print(f"User with _uid '{user_data['uid']}' already exists.")
#             else:
#                 # Proceed with inserting the new user
#                 new_user = User(
#                     name=user_data['name'],
#                     uid=user_data['uid'],
#                     dob=user_data['dob'],
#                     tracking=user_data['tracking'],
#                     exercise=user_data['exercise'],
#                     coins=user_data['coins']
#                 )
#                 new_user.set_password(user_data['password'])  # Set the password separately
#                 db.session.add(new_user)

#         # Commit the changes to the database
#         db.session.commit()





# def initUsers():
#     with app.app_context():
#         """Create database and tables"""
#         db.create_all()
#         """Tester data for table"""
#         u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', exercise = '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', foodandwater ='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }' )
#         u2 = User(name='Nicholas Tesla', uid='niko', password='123niko', dob=date(1856, 7, 10), tracking='{"userName":"Nicholas Tesla","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', exercise = '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', foodandwater ='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }')
#         u3 = User(name='Alexander Graham Bell', uid='lex', dob=date(1856, 7, 10), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', exercise = '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', foodandwater ='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }')
#         u4 = User(name='Grace Hopper', uid='hop', password='123hop', dob=date(1906, 12, 9), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', exercise = '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', foodandwater ='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }') 
#         u5 = User(name='Eun Lim', uid='lim', password='123lim', dob=date(2007, 12, 9), tracking='{"userName":"Eun Lim","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', exercise = '{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }', foodandwater ='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }') #testing create method
#         users = [u1, u2, u3, u4, u5]

#         """Builds sample user/note(s) data"""
#         for user in users:
#             try:
#                 '''add a few 1 to 4 notes per user'''
#                 for num in range(randrange(1, 4)):
#                     note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
#                     #user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
#                 '''add user/post data to table'''
#                 user.create()
#             except IntegrityError:
#                 '''fails with bad or duplicate data'''
#                 db.session.remove()
#                 print(f"Records exist, duplicate email, or error: {user.uid}")
            