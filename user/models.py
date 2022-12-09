from flask import  jsonify, request, session, redirect,render_template #flask dependencies importations
import uuid #we used it to get a unique id
from passlib.hash import pbkdf2_sha256 #we used it to crypt the password
import pymongo #mongo iportation

#database configuration
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

#the main class that we will be using 
class User:

   #define the session 
   def start_session(self, user):
     del user['password']
     session['logged_in'] = True
     session['user'] = user
     return jsonify(user), 200

   #define the signup method
   def signup(self):
  
    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "balance":100
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    
    if db.users.find_one({ "email": user['email'] }):   # Check for existing email address
      return jsonify({ "error": "Email address already in use" }), 400
    if db.users.insert_one(user):
        return self.start_session(user)  #otherwise start the session after creating the account
    return jsonify({"error":"signup failed"}), 400   #return error by default

   #define the signout method
   def signout(self):
    session.clear() #close the session
    return redirect('/') #go to the main page

   #define the login method
   def login(self):

    user = db.users.find_one({     #Check for existing of the email address
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']): #check of the compatibility of the two passwords using the passlib to get the main password which is crypted 

      return self.start_session(user) #start the session if nothing go wrong
    
    return jsonify({ "error": "Invalid login credentials" }), 401 #otherwise it will give an error message 
  
   #define the changePassword method
   def changePasword(self):
        
        #get variables from html form
        email=request.form.get('email')
        OldPassword=request.form.get('oldpassword')
        NewPassword=request.form.get('newpassword')
        #check if there is any variable that is empty 
        if email == "" or OldPassword == "" or NewPassword == "":
            return redirect('/user/change-password') #in that case we will stay in the change_password.html
        else:
            user = db.users.find_one({  #otherwise we will look for that email
              "email": request.form.get('email')
            })
            #create the new user with the new password
            newuser = {
              "name" : user['name'], 
              "email" : email,
              "password": pbkdf2_sha256.encrypt(NewPassword),
              "balance" : user['balance']
            }
            if user and pbkdf2_sha256.verify(request.form.get('oldpassword'), user['password']): #check of the compatibility of the old and the new password using passlib as usual
               #print("pwd matched")
               db.users.update_one({'email': email}, {'$set': newuser}) #update the user with the "newuser" that we have already created
               return redirect('/')
            else:
                return redirect('/user/changepassword')#stay in the change_password page if you make any mistake (of course you can get out of it if you hit the "back" button ^^)

   #define the list method
   def list(self):
    x=db.users
    users= x.find() #find all users
    return render_template('users.html',users=users)

   #define the changemoney method
   def changemoney(self):
        #get variables from form 
        email=request.form.get('email')
        money=request.form.get('moneytogive')
        #converting variables we will neded into numbers
        z=int(money)
        m=int(session['user']['balance'])
        x=m-z #till here we are just saving the result of the operation (balance of the main user - money he is willing to give)
        
        
        if email == "" or money == "" : ##both variables should not be empty
            return redirect('/sendmoney/')
        else:
            user = db.users.find_one({ # looking for the user that we will send him money 
              "email": request.form.get('email')
            })
            n=int(user["balance"])
            y=n+z #(balance of the other user - money he is getting from the main user)


            if( m>z) or ( m==z): #check if the user can afford that much money or not
                mainuser = {
              "balance" : x 
                }
                newuser = {
              "balance" :y
                }
                db.users.update_one({'email': session['user']['email']}, {'$set': mainuser}) #update the giving user
                db.users.update_one({'email': email}, {'$set': newuser}) #update the gifted user

                return redirect('/dashboard/')
            else:
                
                return redirect('/sendmoney/')
  



