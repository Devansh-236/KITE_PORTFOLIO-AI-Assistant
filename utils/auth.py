from kite_api.connector import kite_connector
import webbrowser

def setup_kite_auth():
    """Interactive Kite authentication setup"""
    print("🔐 Setting up Kite Connect authentication...")
    
    # Get login URL
    login_url = kite_connector.get_login_url()
    print(f"Please visit this URL to login: {login_url}")
    
    # Auto-open browser
    webbrowser.open(login_url)
    
    # Get request token from user
    request_token = input("Enter the request_token from the redirect URL: ")
    
    # Generate session
    session_data = kite_connector.generate_session(request_token)
    access_token = session_data['access_token']
    
    print(f"✅ Authentication successful!")
    print(f"Add this to your .env file:")
    print(f"KITE_ACCESS_TOKEN={access_token}")
    
    return access_token

if __name__ == "__main__":
    setup_kite_auth()
