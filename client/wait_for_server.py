import requests
import time

REST_SERVER_URL = "http://0.0.0.0:5080"  # Update this to your actual REST server URL

def wait_for_server_ready():
    url = f"{REST_SERVER_URL}/ready"
    max_attempts = 100  # Any number greater than 60 because database initialization can take time from 5-60 seconds
    attempts = 0

    while attempts < max_attempts:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("REST server is ready")
                return True
        except requests.ConnectionError as con_err:
            pass
        
        print('Waiting for server to be ready')
        attempts += 1
        time.sleep(1)

    print(f"Failed to connect to REST server after {max_attempts} attempts")
    return False

if __name__ == "__main__":
    wait_for_server_ready()
