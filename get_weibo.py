import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Set your API key and secret
client_id = "your_client_id"
client_secret = "your_client_secret"

# Set URLs for obtaining authorization
token_url = "https://api.weibo.com/oauth2/access_token"
authorization_base_url = "https://api.weibo.com/oauth2/authorize"
redirect_uri = "http://localhost/callback"

# Set up OAuth2 client and session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url=token_url, client_id=client_id,
                          client_secret=client_secret)

# Set up API request headers
headers = {
    "Authorization": f"Bearer {token['access_token']}"
}

# Make an API request
response = requests.get("https://api.weibo.com/2/statuses/user_timeline.json",
                        headers=headers, params={"screen_name": "example_user"})
print(response.json())
