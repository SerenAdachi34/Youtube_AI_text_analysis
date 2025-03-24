import sys
import os
import pandas as pd
from ai_functions import *
from markdown_functions import *

if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if len(sys.argv) < 2:
        print("Error: No video ID provided. Please pass the YouTube Video ID as an argument.")
        sys.exit(1)

    video_id = sys.argv[1]

    # Get chat and comment data
    chats_df = pd.read_csv(f"data/{video_id}_chats.csv")
    comments_df = pd.read_csv(f"data/{video_id}_comments.csv")
    comments = comments_df['Comment'].dropna().tolist()
    chats = chats_df['Chat'].dropna().tolist() 
    chat_emoji_df = pd.read_csv(f"data/{video_id}_emoji.csv")

    # Word cloud plots
    word_cloud_diff = compare_two_images("results/plots/wordcloud1.jpg", "results/plots/wordcloud2.jpg", openai_api_key)
    # Bar plots
    word_freq_diff = compare_two_images("results/plots/wordfrequency1.jpg", "results/plots/wordfrequency2.jpg", openai_api_key)
    # Emoji
    emoji_analysis = analyse_emoji(chat_emoji_df, openai_api_key)
    other_analysis = [word_cloud_diff, word_freq_diff, emoji_analysis]

    # AI analysis
    chats_summary = clean_markdown_string(gpt_summary(chats, openai_api_key))
    comments_summary = clean_markdown_string(gpt_summary(comments, openai_api_key))
    chats_sentiment = sentiment_analysis(chats)
    comments_sentiment = sentiment_analysis(comments)
    difference_summary = clean_markdown_string(compare_chats_and_comments(chats_summary, comments_summary, chats_sentiment, comments_sentiment, other_analysis, openai_api_key)) 

    # Report results as Markdown
    markdown_overall_summary(difference_summary, word_cloud_diff, word_freq_diff, chat_emoji_df, emoji_analysis, 
                             chats_summary, comments_summary, chats_sentiment, comments_sentiment)
    
