from flask import render_template,request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/register', methods=['POST'])
def create():
  if not User.validate_user(request.form):
    return redirect('/')
  data ={ 
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": bcrypt.generate_password_hash(request.form['password'])
  }
  id = User.save(data)
  session['user_id'] = id # storing the users id when creating the acocunt
  return redirect('/success')

# READ

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/success')
def show_info():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id': session['user_id']
  }
  return render_template('results.html', results=User.get_by_id(data))

@app.route('/login',methods=['POST'])
def login():
  user = User.get_one(request.form)

  # -------------------------------- validating user email on login --------------------------------
  if not user:
    flash("Invalid Email","login")
    return redirect('/')
  # -------------------------------- validating user password on login --------------------------------
  if not bcrypt.check_password_hash(user.password, request.form['password']):
    flash("Invalid Password","login")
    return redirect('/')

  session['user_id'] = user.id # I'm not sure why this needs to be here
  return redirect('/success')

# UPDATE

# DELETE

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')