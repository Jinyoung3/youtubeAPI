from googleapiclient.discovery import build
api_key = "AIzaSyABkJ_PLePQPjXoIliMufG9t7cWk9Stjbs "
def video_comments(video_id, max_comments):
    # Initialize variables
    replies = []
    comments_fetched = 0
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Retrieve youtube video results
    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        maxResults=100  # Set max results per page
    ).execute()
    
    # Iterate through video response
    while video_response and comments_fetched < max_comments:
        for item in video_response['items']:
            # Check if the max_comments limit was reached
            if comments_fetched >= max_comments:
                break
            
            # Process each comment
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            replycount = item['snippet']['totalReplyCount']
            comments_fetched += 1
            
            if replycount > 0:
                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']
                    replies.append(reply)
                    comments_fetched += 1
                    
                    # Check inside replies if limit reached
                    if comments_fetched >= max_comments:
                        break
            
            # Print comment with list of replies
            print(comment, replies, end='\n\n')
            replies = []
        
        # Check if there are more pages and if the limit hasn't been reached
        if 'nextPageToken' in video_response and comments_fetched < max_comments:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken'],
                maxResults=100
            ).execute()
        else:
            break

# Example usage
video_id = "jM7na1GTNnk"
max_comments = 10  # Set the desired limit here
video_comments(video_id, max_comments)