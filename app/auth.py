# user authentication logic
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def register_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    print(f"Hashed Password: {hashed_password}")  # Debugging line to check hashing
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    print(f"Stored Password: {user.password}")  # Check if stored as a hash
    if user and check_password_hash(user.password, password):
        return True
    return False