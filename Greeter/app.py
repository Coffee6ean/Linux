from flask import Flask, request, render_template
from random import choice, randint, sample
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)  #=> Creating new server

print('Hi')
app.config['SECRET_KEY'] = 'thousandSunny17'
#debug = DebugToolbarExtension(app)

#--- Routes ---#
@app.route('/')
def home_page():
    """Return simple 'Home Page' route"""
    return render_template('hello.html')

@app.route('/form')
def form_page():
    """Return simple 'Home Page' route"""
    return render_template('form.html')

@app.route('/form-2')
def form_2_page():
    """Return simple 'Home Page' route"""
    return render_template('form_2.html')

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
