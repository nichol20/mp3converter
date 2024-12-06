import os, requests

def create(request):
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/user",
        json=request.get_json()
    )
    if response.status_code == 201:
        return None
    return (response.text, response.status_code)