"""
Sample codebase with multiple related functions.
This simulates a small web application backend.
"""

# User Management Functions
def create_user(username, email, password):
    """Create a new user account with validation."""
    if not validate_email(email):
        return None
    if not validate_password(password):
        return None
    
    user = {
        'username': username,
        'email': email,
        'password': hash_password(password),
        'created_at': get_timestamp()
    }
    return user

def validate_email(email):
    """Validate email format has @ and domain."""
    return '@' in email and '.' in email.split('@')[1]

def validate_password(password):
    """Check password meets security requirements: 8+ chars, uppercase, digit."""
    if len(password) < 8:
        return False
    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    return has_digit and has_upper

def hash_password(password):
    """Hash password using SHA-256 for secure storage."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

# Database Functions
def save_to_database(table, data):
    """Save data record to specified database table."""
    print(f"Saving to {table}: {data}")
    return True

def query_database(table, conditions):
    """Query database table with filter conditions."""
    print(f"Querying {table} with {conditions}")
    return []

def update_record(table, record_id, updates):
    """Update existing database record with new values."""
    print(f"Updating {table} record {record_id}")
    return True

def delete_record(table, record_id):
    """Delete record from database table."""
    print(f"Deleting from {table} record {record_id}")
    return True

# Utility Functions
def get_timestamp():
    """Get current timestamp in ISO format."""
    from datetime import datetime
    return datetime.now().isoformat()

def send_notification(user_id, message):
    """Send push notification to user."""
    print(f"Notifying user {user_id}: {message}")
    return True

def log_event(event_type, details):
    """Log system event with timestamp."""
    timestamp = get_timestamp()
    print(f"[{timestamp}] {event_type}: {details}")

def format_error_message(error_code, context):
    """Format user-friendly error message."""
    messages = {
        'INVALID_EMAIL': 'Please enter a valid email address',
        'WEAK_PASSWORD': 'Password must be at least 8 characters',
        'USER_EXISTS': 'This username is already taken'
    }
    return messages.get(error_code, 'An error occurred')

# Authentication Functions
def authenticate_user(username, password):
    """Authenticate user credentials against database."""
    user = query_database('users', {'username': username})
    if not user:
        return None
    
    hashed = hash_password(password)
    if user[0]['password'] == hashed:
        log_event('LOGIN_SUCCESS', f'User {username} logged in')
        return user[0]
    
    log_event('LOGIN_FAILED', f'Failed login attempt for {username}')
    return None

def generate_session_token(user_id):
    """Generate random session token for authenticated user."""
    import random
    import string
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    save_to_database('sessions', {'user_id': user_id, 'token': token})
    return token

def validate_session(token):
    """Validate session token exists and is active."""
    session = query_database('sessions', {'token': token})
    return session is not None and len(session) > 0

def logout_user(token):
    """Invalidate user session token."""
    delete_record('sessions', token)
    return True