import os
import webbrowser
import msal

def generate_access_token(app_id, scopes):
    access_token_cache = msal.SerializableTokenCache()

    # Verifica si ya existe el Token de acceso, si no existe manda al cliente al browser 
    # para que inicie sesion y se genere el access token 
    if os.path.exists('api_token_access.json'):
        access_token_cache.deserialize(open('api_token_access.json', 'r').read())

    client = msal.PublicClientApplication(client_id = app_id, token_cache = access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        flow = client.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise ValueError("No se pudo iniciar el flujo de dispositivo.")
        print("Por favor ingresa este código:", flow["user_code"])
        print("Entra a:", flow["verification_uri"])
        webbrowser.open(flow["verification_uri"])
        token_response = client.acquire_token_by_device_flow(flow)
    
    with open('api_token_access.json', 'w') as _f:
        _f.write(access_token_cache.serialize())
    return token_response

if __name__ == "__main__":
    # ID de la aplicacion que nos dio AZURE
    APP_ID = 'e98ea992-fd7c-4529-a12a-025a265c94f1'
    # Permisos que son delegados
    SCOPES = ['User.Read'] 

    token_response = generate_access_token(APP_ID, SCOPES)
    print(token_response['access_token'])

