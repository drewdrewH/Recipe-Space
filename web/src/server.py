from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response, render
from pyramid.session import SignedCookieSessionFactory

import re

import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']


def get_home(req):
  
  session = req.session
  
  return render_to_response('templates/home.html',{'session':session},request = req )

def profile(req):
  
  session = req.session
  
  return render_to_response('templates/profile.html',{'session':session},request = req )

def sign_up(req):
  msg = ''
    # Check if "name", "password" and "email" POST reqs exist (user submitted POST)
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  session = req.session
  
 
  name = str(req.POST.get('name-signUp'))
  password = str(req.POST.get('password-SignUp'))
  email = str(req.POST.get('email-Signup'))
  session['login'] = True
  session['email'] = email
  print(name , password, email)
  cursor.execute('SELECT * FROM Users WHERE email = %s ;', (email,))
  account = cursor.fetchone()
        # If account exists show error and validation checks
  if account:
    msg = 'Account already exists!'
  elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    msg = 'Invalid email address!'
  elif not re.match(r'[A-Za-z0-9]+', name):
    msg = 'name must contain only characters and numbers!'
  elif not name or not password or not email:
      msg = 'Please fill out the POST!'
  else:
            # Account doesnt exists and the POST data is valid, now insert new account into accounts table
    cursor.execute('INSERT INTO Users (full_name, email, password) VALUES ( %s, %s, %s);', (name,email, password))
    db.commit()
    msg = 'You have successfully registered!'
  
  db.close()
  print(msg)
  return render_to_response('templates/home.html', {'session':session}, request = req)


def login(req):

  email = str(req.POST.get('email'))
  password = str(req.POST.get('password'))
  print(email, password)
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute('SELECT * FROM Users WHERE email = %s and password = %s;', (email,password))
  account = cursor.fetchone()
  db.close()
  print(account)
  if account:
     # Create session data, we can access this data in other routes
    session = req.session
    session['login'] = True
    session['id'] = account[0]
    session['email'] = account[2]
            # Redirect to home page
    return render_to_response('templates/home.html', {"session": session }, request = req)
  else:
            # Account doesnt exist or username/password incorrect
    return 'Incorrect username/password!'



  

  #return render_to_response('templates/home.html', {}, request=req)
def logout(req):

  session = req.session
  session['login'] = False
  return render_to_response('templates/home.html', {"session": session }, request = req)
  
def search(req):
  session = req.session
  search_val = str(req.POST.get('search-val'))
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  quuery = "SELECT * FROM Users WHERE name LIKE '%"+ search_val + "%';"
  cursor.execute()
  return render_to_response('templates/browse.html', {"session": session, 'recipes':records}, request = req)


def browse(req):

  return render_to_response('templates/browse.html', {}, request=req)

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()
  session_factory = SignedCookieSessionFactory('recipeSpaceECE140B')
  
  config.set_session_factory(session_factory)

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('browse', '/browse')
  config.add_view(browse, route_name='browse')

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up', request_method='POST')

  config.add_route('login', '/login')
  config.add_view(login , route_name='login', request_method='POST')

  config.add_route('logout', '/logout')
  config.add_view(logout , route_name='logout', request_method='GET')
  
  config.add_route('profile', '/profile')
  config.add_view(profile , route_name='profile', request_method='GET')

  config.add_route('search', '/search')
  config.add_view(search , route_name='search', request_method='POST')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()