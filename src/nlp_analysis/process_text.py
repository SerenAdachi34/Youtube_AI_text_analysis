import sys
import pandas as pd
from text_utils import *

STOPLIST = load_stopwords()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No video ID provided. Please pass the YouTube Video ID as an argument.")
        sys.exit(1)

    video_id = sys.argv[1]

    # Get chat and comment data
    chats_df = pd.read_csv(f"data/{video_id}_chats.csv")
    comments_df = pd.read_csv(f"data/{video_id}_comments.csv")

    # Wordcloud
    generate_wordcloud_from_dataframe(chats_df, 'Chat', STOPLIST, type_list=["名詞"], save_path="results/plots/wordcloud1.jpg") #Noun 
    generate_wordcloud_from_dataframe(comments_df, 'Comment', STOPLIST, type_list=["名詞"], save_path="results/plots/wordcloud2.jpg") #Noun 

    # Word Frequency
    rank_words_from_dataframe(chats_df, "Chat", STOPLIST, type_list=["形容詞"], save_path="results/plots/wordfrequency1.jpg") #Adjective 
    rank_words_from_dataframe(comments_df, "Comment", STOPLIST, type_list=["形容詞"], save_path="results/plots/wordfrequency2.jpg") #Adjective

    # Emoji
    extract_and_convert_to_emojis(chats_df, "Chat", save_path =f"data/{video_id}_emoji.csv")
