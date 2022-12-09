from flask import Flask,jsonify
from app import app
from user.models import User

#the signup route that uses the signup method from the user class 
@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

#the signout route that uses the signout method from the user class 
@app.route('/user/signout')
def signout():
  return User().signout()

#the login route that uses the login method from the user class
@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

#the update route that uses the ChangePassword method from the user class to change the password
@app.route('/users/update', methods=['POST'])
def update():
        return User().changePasword()

#the list route that uses the list method from the user class to display all users
@app.route('/users/list', methods=['GET'])
def userlist():
        return User().list()
    
#the updatemoney route that uses the changemoney method from the user class which allow us to transfer money between accounts
#you need to logout from your account and login after to see the changes in your balance
@app.route('/users/updatemoney', methods=['POST'])
def update_money():
        return User().changemoney()