import requests
import json


def calling_backend_api(url, payload):
    try:
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            return response.text
        else:
            return "INTERNAL SERVER ERROR"
    except Exception as e:
        print(str(e))
