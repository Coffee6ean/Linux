### Conceptual Exercise

Answer the following questions below:

- What are important differences between Python and JavaScript?
  JavaScript is a scripting language that helps you create interactive web pages, while Python is a high-level object-oriented programming language that has built-in data structures, combined with dynamic binding and typing, which makes it an ideal choice for rapid application development  

- Given a dictionary like ``{"a": 1, "b": 2}``: , list two ways you
  can try to get a missing key (like "c") *without* your programming
  crashing.
  `list = {"a": 1, "b": 2}`
  `list.get('c')`

- What is a unit test?
  A unit test is a way of testing a unit - the smallest piece of code that can be logically isolated in a system. In most programming languages, that is a function, a subroutine, a method or property.

- What is an integration test?
  Integration testing -- also known as integration and testing (I&T) -- is a type of software testing in which the different units, modules or components of a software application are tested as a combined entity

- What is the role of web application framework, like Flask?
  GeeksforGeeks describes ‘web application frameworks’ or ‘web frameworks’ as “a software framework that is designed to support the development of web applications including web services, web resources and web APIs”. In simple words, web frameworks are a piece of software that offers a way to create and run web applications. Thus, you don’t need to code on your own and look for probable miscalculations and faults.

- You can pass information to Flask either as a parameter in a route URL
  (like '/foods/pretzel') or using a URL query param (like
  'foods?type=pretzel'). How might you choose which one is a better fit
  for an application?
  There isn't an exact better way to do this but it depends on the situation. You can generally use query string parameters if you are describing the object you are on vs using the route for the object itself. For example, in the above case I would use /foods/pretzel and then use a query string parameter if I am decribing the pretzel such as /foods/pretzel?type=salty or /foods/pretzel?type=sugar.

- How do you collect data from a URL placeholder parameter using Flask?
  You can specify the variable in the app.route and then use that variable as a paramater in the routing function. Here is an example of the pretzel:
  ```py
  @app.route('/foods/<food>')
  def grocery(food):
  x = food
  ```

- How do you collect data from the query string using Flask?
  With a query string the data can be found in the request.args dictionary:
  ```py
  @app.route('/foods')
  def grocery():
  x = request.args.get('type')
  ```

- How do you collect data from the body of the request using Flask?
  You can get the data form a post request in the body using the request.form dictionary
  ```py
  @app.route('/foods')
  def grocery():
  x = request.form.get('type')
  ```

- What is a cookie and what kinds of things are they commonly used for?
  Cookies are text files containing small snippets of information such as login details to identify your computer when you connect to the internet. They are used to identify and improve your web browsing experience by allowing you to identify specific users.

- What is the session object in Flask?
  The session object is built off of using cookies. It allows the server to set many different things in the in the session for the client to remember wihout having to create many different cookies and just have one session. It is also encoded so that someone can't change session data on the client before sending it to the server.

- What does Flask's `jsonify()` do?
  jsonify will take JSON serializeable data in python and convert it to a JSON string.