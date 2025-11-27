import requests
import json

video_id = "ypFG006G4WQ" # User provided video
url = f"http://localhost:8000/api/transcript?video_id={video_id}"

try:
    print(f"Testing URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Response JSON keys:", data.keys())
            transcript = data.get('transcript')
            print(f"Type of transcript: {type(transcript)}")
            
            if isinstance(transcript, list):
                print(f"Transcript is a list of length {len(transcript)}")
                if len(transcript) > 0:
                    print(f"First item type: {type(transcript[0])}")
                    print(f"First item: {transcript[0]}")
            else:
                print("Transcript is NOT a list.")
                print(f"Content: {transcript}")
                
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
            print(f"Raw text: {response.text}")
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
