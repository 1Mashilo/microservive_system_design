import os
import requests

def token(request):
    # Check if 'Authorization' header is present in the request
    if "Authorization" not in request.headers:
        return None, ("Missing credentials", 401)

    # Extract the token from the 'Authorization' header
    token = request.headers.get("Authorization")

    # If token is missing, return error response
    if not token:
        return None, ("Missing credentials", 401)

    # Send a POST request to the authentication service for token validation
    auth_svc_address = os.environ.get('AUTH_SVC_ADDRESS')
    if not auth_svc_address:
        return None, ("Authentication service address not found", 500)

    response = requests.post(
        f"http://{auth_svc_address}/validate",
        headers={"Authorization": token},
    )

    # Process the response from the authentication service
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
