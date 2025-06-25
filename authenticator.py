# auth_setup.py
import streamlit_authenticator as stauth

# Define user credentials
credentials = {
    "usernames": {
        "debasishguru337@gmail.com": {
            "name": "Debaish Guru",
            "password": "Admin@123"  # For production, store hashed passwords
        }
    },
    "cookie": {"expiry_days": 30, "key": "cookie_key"},
    "preauthorized": {"emails": ["debasishguru337@gmail.com"]}
}


# Function to return an authenticator instance
def get_authenticator():
    authenticator = stauth.Authenticate(
        credentials,
        cookie_name="auth_cookie",
        key="cookie_key",
        cookie_expiry_days=30
    )
    return authenticator
# Define fields for login form
login_fields={
    "usernames":{"label":"Username","type":"text"},
    "password":{"label":"Password","type":"Password"}
    
}


