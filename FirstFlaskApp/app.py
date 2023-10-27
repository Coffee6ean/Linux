from flask import Flask, request 

app = Flask(__name__)  #=> Creating new server

print('Hi')
#--- Routes ---#
@app.route('/')
def home_page():
    """Return simple 'Home Page' route"""
    html = """
    <html>
        <body>
            <h1>Home Page</h1>
            <h3>Welcome to my app</h3>
            <div>
                <a href='/hello'>Go to 'Hello' page</a>
            </div>
            <div>
                <a href='/bye'>Go to 'GoodBye' page</a>
            </div>
        </body>
    </html>
    """
    return html

@app.route('/hello')  # Decorator
def say_hello():
    """Return simple 'Hello'"""
    html = """
    <html>
        <body>
            <h1>Hello There</h1>
        </body>
    </html>
    """
    return html

@app.route('/bye')  # Decorator
def say_goodbye():
    """Return simple 'Goodbye'"""
    html = "<html><body><h1>Good Bye</h1></body></html>"
    return html

#--- GET Request ---#
@app.route('/search')
def search_page():
    term = request.args['term']
    sort = request.args['sort']
    # Use term to find in DB the data that matches 'term'
    return f'<h1>Search Results For: {term}</h1><p>Sorting by: {sort}</p>'

# http://127.0.0.1:5000/search?term=cat&sort=top

#--- Requests ---#
@app.route('/post', methods = ['POST'])
def post_demo():
    return 'You made a POST req'
#  curl -X POST http://127.0.0.1:5000/post => 'You made a POST req'

@app.route('/post', methods = ['GET'])
def get_demo():
    return 'You made a GET req'
# curl http://127.0.0.1:5000/ => 'You made a GET req'

@app.route('/add-comment')
def add_comment_form():
    return """
        <h1>Add Comment</h1>
        <form method="POST">
            <input type="text" placeholder="Comment" name="comment"/>
            <input type="text" placeholder="Username" name="username"/>
            <button>Submit</button>
        </form>
    """

@app.route('/add-comment', methods = ['POST'])
def save_comment_form():
    comment = request.form["comment"]
    username = request.form["username"]
    print(request.form)
    return f"""
        <h1>Saved your form</h1>
        <ul>
            <li>Username: {username}</li>
            <li>Comment: {comment}</li>
        </ul>
    """

#--- Path Variables ---#
@app.route('/r/<subreddit>')
def show_subrredit(subreddit):
    return f"""
        <h1>Browsing the '{subreddit}' Subrredit</h1>
    """

@app.route('/r/<subreddit>/comments/<int: post_id>')
def show_comments(subreddit, post_id):
    return f"""
        <h1>
            Viewing comments for post with id: {post_id} from the '{subreddit}' Subreddit
        </h1>
    """


POSTS = {
    1: 'I like chicken nuggets',
    2: 'I love Carito Chan',
    3: 'kill me pls',
    4: '#LOL'
}

@app.route('/posts/<int:post_id>')
def find_post(post_id):
    post = POSTS.get(post_id, "Post Not Found")
    return f"""
        <h1>{post}</h1>
    """