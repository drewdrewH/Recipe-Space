from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response, render
import re

import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def get_home(req):
  # Connect to the database and retrieve the users
  

  return render_to_response('templates/home.html',{},request = req )

def sign_up(req):
  msg = ''
    # Check if "name", "password" and "email" POST reqs exist (user submitted POST)
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  
  name = str(req.POST.get('name-signUp'))
  password = str(req.POST.get('password-SignUp'))
  email = str(req.POST.get('email-Signup'))
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
  return render_to_response('templates/home.html', {}, request = req)

def login(req):
  

  return render_to_response('templates/home.html', {}, request=req)


''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up', request_method='POST')

  config.add_route('login', '/login')
  config.add_view(login , route_name='login', request_method='POST')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()