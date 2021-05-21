from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response, render
from pyramid.session import SignedCookieSessionFactory

import re
import json
import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def access_database(sqlcomand,values=None,fetch='all'):
  assert isinstance(sqlcomand,str), "sqlcommand must be a string"
  assert values is None or isinstance(values,tuple), "Values must be type Tuple"
  assert fetch == 'all' or fetch == 'one' or fetch == 'none' or fetch is None, "Fetch can only be 'all', 'one', 'none', or None."
  
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass) # must we always open and close this?
  cursor = db.cursor()
  if values:
    cursor.execute(sqlcomand,values)
  else:
    cursor.execute(sqlcomand)
  
  if fetch is not None and not fetch =='none':
    if fetch == 'all':
      records = cursor.fetchall()
    elif fetch == 'one':
      records = cursor.fetchone()
    else:
      records = None # we should never hit this because of the assert statement above
  else:
    records = None
  
  if db.in_transaction: # only commit if we need to (i.e., select statements don't need to commit)
    db.commit()
  db.close()
  return records


def get_home(req):
  # This function is responsible for gathering the information
  # and rendering the home.html page.

  session = req.session

  popular = access_database("SELECT DISTINCT * FROM Recipes \
    r INNER JOIN (SELECT name, Count(*) FROM Bookmarks GROUP BY name \
    ORDER BY count(*) DESC LIMIT 4) p on r.name = p.name;", values=None,fetch='all')
  ingredients = {}

  for i in popular:
    top_5 = i[4].split(';') # the fourth index holds all the ingredients. They are separated by semicolons
                            # Thus this selects the first five recipes in the record
                            # Note that this is a dictionary with the key being the recipe name and the value
                            # being the ingredients, so print(ingredients['Meatballs']) displays '["Ground Beef","Flour","etc."]'
    ingredients.update({str(i[1]):top_5[:5]}) # i[1] == recipe name
  
  records = access_database("SELECT * FROM Recipes;",values=None,fetch='all') # we gather all the recipes so that we can display them on the page
  basic = {} # Basic will hold the top 5 ingredients of every recipe, not just the popular ones.
  for i in records:
    top_5 = i[4].split(';')
    basic.update({str(i[1]):top_5[:5]}) # print(ingredients['Meatballs']) displays '["Ground Beef","Flour","etc."]'
                                        # TODO: could we somehow combine this with the ingredients variable? That
                                        # would make more sense to me

 
  return render_to_response('templates/home.html',\
    {'session':session, 'recipes':records, 'popular':popular, 'ingredients':ingredients, 'basic':basic},\
    request = req )

def profile(req):
  # This function is responsible for rendering the profile page

  # db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  # cursor = db.cursor()
  session = req.session # grab the current session
  email = session['email'] # Do we need to check for an invalid email field? We don't even check if session['login'] is True
  records = access_database("SELECT * FROM Bookmarks WHERE email = %s ;",\
                            values=(email,),fetch='all') # gather all the bookmarks associated with that user

  basic = {}
  for i in records:
    top_5 = i[5].split(';')
    basic.update({str(i[2]):top_5[:5]})
  
  return render_to_response('templates/profile.html',{'session':session, 'recipes':records, 'basic':basic},request = req )

def sign_up(req):
  msg = ''
    # Check if "name", "password" and "email" POST reqs exist (user submitted POST)
  session = req.session

  name = str(req.POST.get('name-signUp')) # there is a form with inputs that are named 'name-signUp', etc. which
  password = str(req.POST.get('password-SignUp')) # allows us to grab the form input data with req.POST.get('name')
  email = str(req.POST.get('email-Signup')) # (it's located in navbar.html)
  
  session = req.session
  
  print(name , password, email)
  account = access_database('SELECT * FROM Users WHERE email = %s ;', values=(email,),fetch='one')
  
        # If account exists show error and validation checks
  if account:
    msg = 'Account already exists!'
    success = False 
  elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    msg = 'Invalid email address!'
    success = False 
  elif not re.match(r'[A-Za-z0-9]+', name):
    msg = 'name must contain only characters and numbers!'
    success = False 
  elif not name or not password or not email:
    msg = 'Please fill out the POST!'
    success = False 
  else:
            # Account doesnt exists and the POST data is valid, now insert new account into accounts table
    access_database('INSERT INTO Users (full_name, email, password) VALUES ( %s, %s, %s);',values=(name,email, password),fetch=None)
  
    # update the session with the current information
    session['login'] = True 
    session['email'] = email
    msg = 'You have successfully registered!'
    success = True
  
  # db.close()
  print(msg)
  # TODO: do something with the success and msg dictionary elements
  # Also, what happens when we don't sucessfully register?
  return render_to_response('templates/profile.html', {"session": session, "message":msg, "success" : success }, request = req)


def login(req):

  email = str(req.POST.get('email')) # grab the form data
  password = str(req.POST.get('password'))
  print(email, password)

  account = access_database('SELECT * FROM Users WHERE email = %s and password = %s;',values=(email,password),fetch='one')

  print(account)
  if account:
     # Create session data, we can access this data in other routes
    session = req.session
    session['login'] = True
    session['id'] = account[0] # We keep the user id in the session but we never use it
    session['email'] = account[2]
    records = access_database("SELECT * FROM Recipes;",values=None,fetch='all') # is this records being used?

            # Redirect to home page
    return get_home(req)
  else:
            # Account doesnt exist or username/password incorrect
            # TODO: make this return a meaningful value -- as of right now incorrect login info
            # causes 'A server error has occured, please contact the adminstrator' error to appear
    return 'Incorrect username/password!'

def logout(req):

  session = req.session
  session['login'] = False # we don't clear the email field. Is this an issue?
  return get_home(req) # redirect to home page
  
def search(req):
  # This is used when we are searching for recipes, not recipe ingredients
  session = req.session
  search_val = str(req.POST.get('search-val'))

  query = "SELECT * FROM Recipes WHERE name LIKE '% "+ search_val + "%' OR ingredients LIKE '% "+ search_val + "%';"
  # We only do a substring match
  records = access_database(query,values=None,fetch='all')
  basic = {}
  for i in records:
    top_5 = i[4].split(';')
    basic.update({str(i[1]):top_5[:5]})
  


  return render_to_response('templates/browse.html', {"session": session, 'recipes':records, 'basic':basic}, request = req)


def browse(req):
  # This method is responsible for rendering the browse page with all the recipes
  session = req.session
  
  records = access_database("SELECT * FROM Recipes;",values=None,fetch='all')
  basic = {}
  for i in records:
    top_5 = i[4].split(';')
    basic.update({str(i[1]):top_5[:5]})
  
  return render_to_response('templates/browse.html', {'session':session, 'recipes':records, 'basic':basic}, request=req)

def bookmark(req):
  # This function is responsible for updating the bookmarks database
  session = req.session
  recipe = req.json_body.get('recipe') # since this session gets referred by javascript, we get the information from the json body
  email = req.json_body.get('email')
  src = req.json_body.get('book_src')
  print(recipe)
 
  access_database("UPDATE Recipes SET bookmark = %s  WHERE name = %s ;", values=(src,recipe), fetch=None)

  if src ==  "https://img.icons8.com/cute-clipart/64/000000/bookmark-ribbon.png":
    access_database("DELETE FROM Bookmarks WHERE name = %s and email = %s;", values = (recipe, email), fetch=None)
  else:
  # first we must get the recipe record so that we can create/remove the bookmark record
    record = list(access_database('SELECT DISTINCT * FROM Recipes WHERE name = %s ;',values=(recipe,),fetch='one'))
    record = record[1:len(record)-1]
    record.insert(0, email) # we attach the email to it to conform to the bookmark record
  
    # TODO: create logic to remove a bookmark if it is already present
    query = """insert into Bookmarks (email, name, time, serving, ingredients, instructions,
            nutrition, related, image, taste, ease, cleanup, bookmark) values (%s,%s, %s,  %s,%s, %s,  %s,%s, %s,  %s,%s, %s, %s);"""

    access_database(query,values=tuple(record),fetch=None)
  
  json_object = json.dumps({'message':'sucessfully bookmarked recipe'}, indent = 4)  

  return json_object

def filter_ingredient(req):
  # This function is responsible for rendering the browse page filtering based on ingredient
  # So that we search "Ground Beef" and get all the dishes that have ground beef in them
  session = req.session
  search_val = str(req.POST.get('filter-search-val'))

  query = "SELECT * FROM Recipes WHERE ingredients LIKE '%" + search_val + "%';"

  records = access_database(query,values=None,fetch='all')

  return render_to_response('templates/browse.html', {"session": session, 'recipes':records}, request = req)

def search_autocomplete(req):
  # This method is responsible for gathering the ingredients that match
  # the search value, so that we can get a nice google-esqe autofill-looking thing
  # when we are filtering by ingredients.
  search_val = req.matchdict.get('ingredient')
  if(search_val == ""):
    return {'ingredients': 'no search'}

  query = "SELECT ingredient FROM Ingredients WHERE ingredient LIKE '" + search_val + "%' LIMIT 10;"

  records = access_database(query,values=None,fetch='all')
  if(records == []):
    return {'ingredients':'no records'}
  return {'ingredients':records}

def recipe(req):
  session = req.session
  recipeId = req.matchdict.get('recipe', None)
 
  query = "SELECT * FROM Recipes WHERE id = " + recipeId +  " ;"
  
  records = access_database(query, values=None, fetch='all')

  basic = {}
  for i in records:
    top_5 = i[4].split(';')
    basic.update({str(i[1]):top_5})
  
  ins = records[0][5].split('.')

  return render_to_response('templates/recipe.html', {"session": session, 'recipes':records, 'basic':basic, 'instructions':ins }, request = req)


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

  config.add_route('bookmark', '/bookmark')
  config.add_view(bookmark , route_name='bookmark', request_method='POST', renderer='json')

  config.add_route('filter_ingredient', '/filter_ingredient')
  config.add_view(filter_ingredient , route_name='filter_ingredient', request_method='POST')

  config.add_route('search_autocomplete', '/search_autocomplete/{ingredient}')
  config.add_view(search_autocomplete , route_name='search_autocomplete', renderer='json')

  config.add_route('recipe', '/{recipe}')
  config.add_view(recipe , route_name='recipe' )

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()