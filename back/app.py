
from flask import *
import json

app = Flask(__name__)


# Loads user data from a JSON file
with open('users.json', 'r') as json_file:
    users_data = json.load(json_file)


# home page
@app.route('/')
def home():
    return render_template('index.html')


# login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = any(user['username'] == username and user['password'] == password for user in users_data['users'])

        if user_exists:
            # Successful login
            return render_template('success.html')
        else:
            # Failed login
            msg = 'Invalid username or password'
            return render_template('login.html', msg = msg)
    return render_template('login.html', msg = msg) #GET


# signup function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        # Checks if the new username is already taken
        if any(user['username'] == new_username for user in users_data['users']):
            msg = 'Username already taken. Please choose a different one.'
            return render_template('signup.html', msg=msg)

        # Adds the new user to the user data
        new_user = {'username': new_username, 'password': new_password}
        users_data['users'].append(new_user)

        # Writes the updated user data back into the JSON file
        with open('users.json', 'w') as json_file:
            json.dump(users_data, json_file, indent=2)

        # Redirects to the login page and shows a success message
        return render_template('login.html',msg='Signup successful! Please login.')

    return render_template('signup.html')



if __name__ == "__main__":
    app.run(debug=True)