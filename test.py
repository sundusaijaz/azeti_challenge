import json
import requests
url = "http://localhost:5080/ready"  
    #http://localhost:5080/ready
while True:
    try:
        response = requests.get(url)
        print('+++++++')
        print(response)
        if response.status_code == 200:
            print("Server is ready")
            break
    except requests.ConnectionError:
        print("Waiting for server to be ready...")
        break