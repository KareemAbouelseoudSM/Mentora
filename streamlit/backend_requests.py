import requests

def chat(user_input,session_id,user_id,base_url="http://localhost:8000"):
    url = f"{base_url}/chatter"
    payload = {
        "user_input": user_input,
        "session_id": session_id,
        "user_id": user_id
    }
    response=requests.post(url, json=payload,stream=True) 
    if response.status_code==200:
        return response 
    else:
        print(response.status_code)
        print(response.text)