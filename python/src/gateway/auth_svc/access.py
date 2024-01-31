import os
import requests

def login(request):
    # Get authorization credentials from request
    auth = request.authorization 
    if not auth:
        return None, ("Missing credentials", 401)

    basic_auth = (auth.username, auth.password)

    # Send POST request to authentication service for login
    auth_svc_address = os.environ.get('AUTH_SVC_ADDRESS')
    if not auth_svc_address:
        return None, ("Authentication service address not found", 500)

    response = requests.post(
        f"http://{auth_svc_address}/login",
        auth=basic_auth
    )

    # Process response from authentication service
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
