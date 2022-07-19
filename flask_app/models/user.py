from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
  def __init__(self,data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def save(cls,data):
    query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
    return connectToMySQL('login_registration_schema').query_db(query,data)

  @classmethod
  def get_all(cls): # this is to get all users in the database;
    query = "SELECT * FROM users"
    result = connectToMySQL('login_registration_schema').query_db(query)
    emails = []
    for row in result:
      emails.append(cls(row))
    return result

  @classmethod
  def get_one(cls, data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL('login_registration_schema').query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_id(cls,data): # why does this route EXIST!!!
    query = "SELECT * FROM users WHERE id = %(id)s;"
    results = connectToMySQL('login_registration_schema').query_db(query,data)
    return cls(results[0])

  @staticmethod
  def validate_user( user ):
    is_valid = True
    # -------------------------------- validating first_name --------------------------------
    if len(user['first_name']) < 3:
      flash("First Name must be longer than 3 letters!", 'first_name')
      is_valid = False
    # -------------------------------- validating last_name --------------------------------
    if len(user['last_name']) < 3:
      flash("Last Name must be longer than 3 letters!", 'last_name')
      is_valid = False
    # -------------------------------- validating email --------------------------------
    if not EMAIL_REGEX.match(user['email']):
      flash("Email cannot be blank!", 'email')
      is_valid = False
    # -------------------------------- validating password --------------------------------
    if len(user['password']) < 8:
      flash("Password must be 8 characters long, contain special characters, and match confirmation", 'password')
      is_valid = False
    # -------------------------------- validating password --------------------------------
    if user['password'] != user['password_confirm']:
      flash ("Confirm Password does not match Password", 'password')
      is_valid = False

    return is_valid