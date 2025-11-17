import os
import requests
from ms_graph import generate_access_token

def get_emails(headers):
    response = requests.get(GRAPH_API_ENDPOINT + 'me/messages?$select=internetMessageHeaders&$top=10')

# Step 1: Get the acces token
APP_ID = 'e98ea992-fd7c-4529-a12a-025a265c94f1'
SCOPES = ['Mail.Read']
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
headers = {
    'Authorization': 'Bearer' + access_token['access_token']
}
