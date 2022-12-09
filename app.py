from flask import Flask, render_template, session, redirect
from functools import wraps



app = Flask(__name__)
from user import routes
app.secret_key = b'\xbb\x08v\xe6\xf5u\xfa\x19\xbe\xcf\x90\xbc_\xf7\xc1w'

# Decorators used to make sure you can't access to the pages without beeing connected
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap


@app.route('/')
def home():
    return render_template ('login.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template ('dashboard.html')

@app.route('/create/')
def create():
    return render_template ('register.html')

@app.route('/users/')
@login_required
def users():
    return render_template ('users.html')

@app.route('/sendmoney/')
@login_required
def sendmoney():
    return render_template ('sendmoney.html')


@app.route('/user/changepassword')
@login_required
def changepassword():
    return render_template ('changepassword.html')

