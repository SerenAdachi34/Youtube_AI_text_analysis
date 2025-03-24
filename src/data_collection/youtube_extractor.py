import os
import pytchat
import pandas as pd
from googleapiclient.discovery import build

def get_replay_live_chat(video_id: str, max_chat:int=100):
    """ 
    Fetches live chat messages from YouTube video
    input: 
        video_id (str): youtube video id
        max_chat (int): maximum chat number to be extracted. Default is 100 chat messages. False then no limit
    output: messages (pd.Dataframe): dataframe of randomly selected chat messages
    """ 
    chat = pytchat.create(video_id=video_id)
    messages_list = []

    # Get all chat messages
    while chat.is_alive():
        for c in chat.get().sync_items():
            messages_list.append({'Author': c.author.name, 'Chat': c.message})
            if len(messages_list) % 10 == 0: #progress
                print(f"chats extracted: {len(messages_list)}")
            if max_chat is not False and len(messages_list) > max_chat:
                return pd.DataFrame(messages_list)

    return pd.DataFrame(messages_list)

    
def get_comments(video_id: str, youtube_api_key: str,  max_comments: int=100):
    """ 
    Fetches comments from YouTube videp
    input: video_id (str) -- youtube video id
           youtube_api_key (str) -- your youtubeAPI
           max_comments (int) -- maximum comment number to be extracted. Default is 100 comments. False then no limit
    output: comments (pd.Dataframe) -- dataframe of Youtube comments
    """ 
    
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    # Initialize an empty list to store comments
    comments_list = []

    # Fetch comments using the commentThreads endpoint
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # Maximum results per request
    )
    response = request.execute()

    # Loop through all comments
    while request:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments_list .append({'Author': author, 'Comment': comment})
            if len(comments_list) % 10 == 0: #progress
                print(f"comments extracted: {len(comments_list)}")
            if max_comments is not False and len(comments_list) > max_comments:
                return pd.DataFrame(comments_list)
            
        # Check if there's a next page
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

    return pd.DataFrame(comments_list)