from flask import Flask, request, render_template, redirect, flash, jsonify
from random import choice, randint, sample
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)  #=> Creating new server

print('Initialize')
app.config['SECRET_KEY'] = 'thousandSunny17'
#debug = DebugToolbarExtension(app)

#--- Routes ---#
@app.route('/')
def home_page():
    """Return simple 'Home Page' route"""
    return render_template('hello.html')

#--- Redirect to 'Home Page' ---#
@app.route('/old-home-page')
def redirect_to_home():
    """Redirects to new 'Home Page'"""
    flash('Deprecated page. Redirecting to new route')
    return redirect('/')

MOVIES = {'Amadeus', 'Rango', 'Batman', 'The Truman Show', 'Lego Movie'}

@app.route('/movies')
def show_all_movies():
    return render_template('movies.html', movies = MOVIES)

#--- Redirect: POST method & Flash Messaging ---#
@app.route('/movies/new', methods = ['POST'])
def add_movie():
    title = request.form['title']
    #Pretend DB
    if title in MOVIES:
        flash('Movie already registered', 'error')
    else:
        MOVIES.add(title)
        flash('Added new movie', 'success')
    return redirect('/movies')

#--- Returning JSON ---#
@app.route('/movies/json')
def get_movies_json():
    #info = jsonify('{"Boyhood": {"year" : 2015}}')
    info = jsonify(list(MOVIES))
    return info

@app.route('/form')
def form_page():
    """Return simple 'Home Page' route"""
    return render_template('form.html')

@app.route('/form-2')
def form_2_page():
    """Return simple 'Home Page' route"""
    return render_template('form_2.html')

#--- Variables & Inputs ---#
@app.route('/greet')
def get_greeting():
    username = request.args['username']
    get_compliment = choice(COMPLIMENTS)
    return render_template('greet.html', username = username, 
        compliment = get_compliment)

@app.route('/greet-2')
def get_greeting_2():
    username = request.args['username']
    #wants_complimnets = request.args['wants_compliments']  //KeyError
    wants = request.args.get('wants_compliments')
    nice_things = sample(COMPLIMENTS, 3)
    return render_template('greet_2.html', 
        username = username, wants_compliments = wants, 
        compliments = nice_things)

COMPLIMENTS = ['cool', 'awesome', 'academic wepon', 'sexy beast', 
    'hacker', 'Him-othy', 'big kahuna']

@app.route('/spell/<word>')
def spell_word(word):
    caps = word.upper()
    return render_template('spell_word.html', word = caps)

@app.route('/lucky')
def lucky_number():
    num = randint(1,10)
    return render_template('lucky.html', lucky_num = num, msg = 'You are soo lucky')
