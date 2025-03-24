# user authentication logic
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def register_user(username, password): #function to register a new user
    hashed_password = generate_password_hash(password, method='sha256') #hash the password
    print(f"Hashed Password: {hashed_password}")  # Debugging line to check hashing
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user) #add the new user to the database
    db.session.commit()

def login_user(username, password): #function to login a user
    user = User.query.filter_by(username=username).first()
    print(f"Stored Password: {user.password}")  # Check if stored as a hash
    if user and check_password_hash(user.password, password):
        return True #return True if the password is correct
    return False