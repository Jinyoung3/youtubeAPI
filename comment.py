import os
import googleapiclient.discovery
import json

def read_video_id_from_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data['video_id']
def main(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyABkJ_PLePQPjXoIliMufG9t7cWk9Stjbs"  # Replace with your actual developer key

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=5,  # Adjust based on your needs
        order="relevance",  # This doesn't sort by likes but helps find relevant comments
        textFormat="plainText"
    )
    response = request.execute()
    json_filename = "comment.json"  # This will create or overwrite youtube_response.json in the current directory
    # Serialize response to JSON formatted string and write to the file
    with open(json_filename, 'w') as json_file:
        json.dump(response, json_file, indent=4)
    print(f"Response has been saved to {json_filename}")

if __name__ == "__main__":
    json_file_path = "youtubeInfo.json" 
    video_id = read_video_id_from_json(json_file_path) # Replace with the actual video ID
    main(video_id)
