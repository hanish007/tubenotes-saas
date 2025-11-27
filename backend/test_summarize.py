import requests

video_id = "ypFG006G4WQ" # User provided video
url = f"http://localhost:8000/api/summarize?video_id={video_id}"

try:
    print(f"Testing URL: {url}")
    print("Waiting for summary (this might take a few seconds)...")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Success! Summary received.")
        print("-" * 20)
        print(data.get('summary'))
        print("-" * 20)
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
