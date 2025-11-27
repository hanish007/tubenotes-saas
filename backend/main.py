from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
    client = None

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import re

@app.get("/")
def read_root():
    return {"message": "TubeNotes Backend is running!"}

def extract_video_id(url_or_id: str) -> str:
    # Robust regex to extract video ID from various YouTube URL formats
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url_or_id)
    if match:
        return match.group(1)
    # If no match, assume it's already an ID if it's 11 chars
    if len(url_or_id) == 11:
        return url_or_id
    raise ValueError("Invalid YouTube URL or Video ID")

def fetch_transcript_data(video_id: str):
    print(f"Fetching transcript for video_id: {video_id}")
    clean_video_id = extract_video_id(video_id)
    print(f"Extracted clean_video_id: {clean_video_id}")
    
    # Instantiate the class as per new syntax
    yt = YouTubeTranscriptApi()
    
    # Use yt.list instead of list_transcripts
    transcript_list = yt.list(clean_video_id)
    
    try:
        # Try to get manually created English transcript
        transcript = transcript_list.find_transcript(['en'])
    except:
        # Fallback to generated English transcript
        print("Manual English transcript not found, trying generated...")
        transcript = transcript_list.find_generated_transcript(['en'])
    
    fetched_object = transcript.fetch()
    print("Transcript fetched successfully")
    
    # Convert Snippet objects to dictionaries
    fetched_transcript = [
        {'text': s.text, 'start': s.start, 'duration': s.duration}
        for s in fetched_object.snippets
    ]
    return fetched_transcript

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        transcript_data = fetch_transcript_data(video_id)
        return {"transcript": transcript_data}
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/summarize")
def summarize_video(video_id: str):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured.")
        
    try:
        transcript_data = fetch_transcript_data(video_id)
        
        # Concatenate transcript text
        full_text = " ".join([item['text'] for item in transcript_data])
        
        print(f"Sending transcript (length: {len(full_text)}) to Gemini...")
        
        system_prompt = "You are an expert study assistant. Convert the following video transcript into structured study notes. Use H2 headers for main topics, bullet points for details, and code blocks for any technical syntax. Keep it concise."
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        
        return {"summary": response.text}
        
    except Exception as e:
        print(f"Error summarizing video: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
