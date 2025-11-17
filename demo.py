import os
import requests
from ms_graph import generate_access_token

def get_emails(headers):

    try:
        response = requests.get(
            GRAPH_API_ENDPOINT + 'me/messages?$select=internetMessageHeaders&$top=10'
            
            )

    except Exception as e:
        print(e)
        return False

# Step 1: Get the acces token
APP_ID = os.getenv('APP_ID')
SCOPES = ['Mail.Read']
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
headers = {
    'Authorization': 'Bearer' + access_token['access_token']
}
