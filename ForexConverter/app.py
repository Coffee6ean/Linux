from flask import Flask, request, render_template, flash, redirect, url_for

# Create a Flask web application
app = Flask(__name__)

# Set the secret key for session management
app.secret_key = 'your_secret_key'

# Global variables for calculated rate and error message
calculated_rate = None
error_message = None

# Define the route for the main page
@app.route('/')
def app_page():
    global error_message

    # Display flash messages based on calculated rate or error message
    if isinstance(calculated_rate, (int, float)):
        flash('Calculation successful', 'success')
    elif error_message:
        flash(error_message, 'danger')
        error_message = None

    # Render the HTML template with the calculated rate
    return render_template('index.html', result=calculated_rate)

# Define the route for handling rate calculation via POST method
@app.route('/calculate_rate', methods=['POST'])
def calculate_rate():
    global calculated_rate
    global error_message

    # Get input data from the JSON request
    first_input = request.json.get('firstInput')
    second_input = request.json.get('secondInput')
    amount_input = request.json.get('amountInput')

    try:
        # Check for missing input data
        if not (first_input and second_input and amount_input):
            raise ValueError('Missing input data')

        # Calculate the exchange rate and update the global variable
        rate1 = float(first_input)
        rate2 = float(second_input)
        amount = float(amount_input)
        calculated_rate = (rate2 / rate1) * amount
    except ValueError as e:
        # Handle errors and set the error message in the global variable
        calculated_rate = 'NaN'
        error_message = str(e)

    # Redirect to the main page to display flash messages
    return redirect(url_for('app_page'))

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
