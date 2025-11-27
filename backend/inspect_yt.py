from youtube_transcript_api import YouTubeTranscriptApi

print(f"Type: {type(YouTubeTranscriptApi)}")

if hasattr(YouTubeTranscriptApi, 'list'):
    print("Found 'list' method.")
    try:
        # Try with a known video ID
        # video_id = 'dQw4w9WgXcQ' # Rick Roll
        # Just check signature or docstring
        print(f"Docstring of list: {YouTubeTranscriptApi.list.__doc__}")
    except Exception as e:
        print(f"Error inspecting list: {e}")

if hasattr(YouTubeTranscriptApi, 'fetch'):
    print("Found 'fetch' method.")
    print(f"Docstring of fetch: {YouTubeTranscriptApi.fetch.__doc__}")

# Try to instantiate as user suggested
try:
    yt = YouTubeTranscriptApi()
    print("Instantiated successfully.")
    
    video_id = 'dQw4w9WgXcQ'
    print(f"Fetching transcript for {video_id}...")
    
    transcript_list = yt.list(video_id)
    transcript = transcript_list.find_transcript(['en'])
    print(f"Transcript object type: {type(transcript)}")
    
    fetched = transcript.fetch()
    print(f"Fetched type: {type(fetched)}")
    
    if hasattr(fetched, 'snippets'):
        print("Fetched object has 'snippets' attribute.")
        snippets = fetched.snippets
        print(f"Snippets type: {type(snippets)}")
        if isinstance(snippets, list) and len(snippets) > 0:
            snippet = snippets[0]
            print(f"First snippet: {snippet}")
            print(f"Snippet dir: {dir(snippet)}")
            if hasattr(snippet, 'to_dict'):
                print("Snippet has 'to_dict' method.")
            else:
                print("Snippet does NOT have 'to_dict' method.")
    else:
        print("Fetched object does NOT have 'snippets' attribute.")
        print(f"Dir: {dir(fetched)}")

except Exception as e:
    print(f"Error: {e}")
