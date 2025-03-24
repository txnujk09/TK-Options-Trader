import sys #imports the sys module
import os #imports the os module
from flask_login import LoginManager #imports the 'LoginManager' class from Flask-Login


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adds the app directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/monte_carlo'))) #adds the monte_carlo directory to the sys.path
print(sys.path) #prints the updated sys.path

from myapp import create_app #imports the 'create_app' function from myapp
from models import User #imports the 'User' class from models

login_manager = LoginManager() #creates an instance of the 'LoginManager' class

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id)) #returns the user object for the given user ID

if __name__ == '__main__': 
    app = create_app()  #creates the Flask app
    login_manager.init_app(app) #initialises the login manager with the app
    login_manager.login_view='login'
    app.run(debug=True) #runs the app in debug mode


