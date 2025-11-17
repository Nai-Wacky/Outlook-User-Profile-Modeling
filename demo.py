import os
import requests
import pandas as pd
from ms_graph import generate_access_token

def get_emails(headers, save_folder):

    try:
        email_headers = requests.get(
            GRAPH_API_ENDPOINT + 'me/messages?$select=internetMessageHeaders&$top=5',
            headers=headers
        )

        print(email_headers.status_code)
        
        emails = email_headers.json()["value"]

        headers_needed = ["Date", "Message-ID", "From", "To", "Subject"]
        filtered_emails = []

        for email in emails:
            header = email.get("internetMessageHeaders", [])
            data = {h["name"]: h["value"] for h in header if h["name"] in headers_needed}
            filtered_emails.append(data)

        for i, datos in enumerate(filtered_emails, 1):
            print(f"Correo {i}:")
            for k, v in datos.items():
                print(f"{k}: {v}")
        
        print("Hola, si corre?")
        
        df = pd.DataFrame(filtered_emails)
        
        output_path = os.path.join(save_folder, "filtered_emails.csv")
        
        df.to_csv(output_path, index=False)

    except Exception as e:
        print(e)
        return False

# Step 1: Get the acces token
APP_ID = 'e98ea992-fd7c-4529-a12a-025a265c94f1'
SCOPES = ['Mail.Read']
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0/'

save_folder = os.path.join(os.getcwd(), "emails")
os.makedirs(save_folder, exist_ok=True)

access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
#print(access_token)
headers = {
    'Authorization': 'Bearer' + access_token['access_token']
}

# Step 2: Get the emails and save them to CSV
get_emails(headers=headers, save_folder=save_folder)
