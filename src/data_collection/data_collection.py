import os
import sys
from youtube_extractor import get_replay_live_chat, get_comments

if __name__ == "__main__":
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if len(sys.argv) < 2:
        print("Error: No video ID provided. Please pass the YouTube Video ID as an argument.")
        sys.exit(1)

    video_id = sys.argv[1]

    # Extract chat messages of given video
    chats_df = get_replay_live_chat(video_id, max_chat=500)
    chats_df.to_csv(f'data/{video_id}_chats.csv', index=False)
    print(f"Extracted {len(chats_df)} chat messages.")

    # Extract chat messages of given video
    comments_df = get_comments(video_id, youtube_api_key=youtube_api_key, max_comments=300)
    comments_df.to_csv(f'data/{video_id}_comments.csv', index=False)
    print(f"Extracted {len(comments_df)} comments messages.")


