import os
import requests
import pandas as pd
from ms_graph import generate_access_token

def get_emails(headers, save_folder):
    
    #Declaramos variables que usaremos despues
    url = GRAPH_API_ENDPOINT + "me/messages?$select=internetMessageHeaders&$top=999"
    all_emails = []
    headers_needed = ["Date", "Message-ID", "From", "To", "Subject"]

    # try catch donde se hace el request, se separan los datos y se guardan en un csv
    try:
        # ciclo donde se obtienen los correos
        while url:
            response = requests.get(url, headers=headers)
            print(response.status_code)
            data = response.json()

            # Extrae los headers necesarios de cada correo
            emails = data.get("value", [])
            for email in emails:
                header = email.get("internetMessageHeaders", [])
                filtered = {h["name"]: h["value"] for h in header if h["name"] in headers_needed}
                all_emails.append(filtered)

            # Verifica si hay siguiente página
            url = data.get("@odata.nextLink")

        # Imprime 10 correos obtenidos
        for i, datos in enumerate(all_emails[:10], 1):
            print(f"Correo {i}:")
            for k, v in datos.items():
                print(f"{k}: {v}")

        # Exporta a CSV
        df = pd.DataFrame(all_emails)
        output_path = os.path.join(save_folder, "filtered_emails.csv")
        df.to_csv(output_path, index=False)

    except Exception as e:
        print(e)
        return False

# Paso 1: Obtenemos el token de acceso
# El ID que nos da Azure de nuestra aplicación
APP_ID = 'e98ea992-fd7c-4529-a12a-025a265c94f1'
# Permisos que se pide al usuario
SCOPES = ['Mail.Read']
# Endpoint de microsoft
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0/'

#Carpeta donde se guardaran los resultados
save_folder = os.path.join(os.getcwd(), "emails")
# Si la carpeta no existe, la crea
os.makedirs(save_folder, exist_ok=True)

# Llamamos al metodo que nos genera el token
access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
#print(access_token)
headers = {
    'Authorization': 'Bearer' + access_token['access_token']
}

# Paso 2: Obtiene los email y los guarda en un csv
get_emails(headers=headers, save_folder=save_folder)
