#creating and intialising database

# Adding project root to sys.path for module resolution
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './app')))
print(sys.path)

from app.myapp import create_app #Import create_app function from app 
from app.models import db  #Import the database instance

# Create the Flask app context
app = create_app()

with app.app_context():
    print("Database created successfully!")