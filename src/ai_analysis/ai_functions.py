import base64
import openai
import random
from textblob import TextBlob
import nltk
nltk.download('punkt')

def compare_two_images(image_path1, image_path2, opemai_api_key):
    """
    Analyses the differeces between two images
    input:
      image_path1 (str): path to one image
      image_path2 (str): path to another image
      opemai_api_key (str): opemai api key
    output:
      str: analysis text
    """
    with open(image_path1, "rb") as image_file:
        base64_image_1 = base64.b64encode(image_file.read()).decode("utf-8")
    with open(image_path2, "rb") as image_file:
        base64_image_2 = base64.b64encode(image_file.read()).decode("utf-8")
    client = openai.OpenAI(api_key=opemai_api_key)
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "You are a text analyst specialising in youtube comment. Based on the two images of youtube live chats and comments, analyse the difference between them and report it in one paragraph",
            },
            {
              "type": "image_url",
              "image_url": {"url": f"data:image/png;base64,{base64_image_1}"},
            },
            {
              "type": "base64",
              "image_url": {"url": f"data:image/png;base64,{base64_image_2}"},
            },
          ],
        }
      ],
      max_tokens=300,
    )
    return response.choices[0].message.content


def analyse_emoji(chat_emoji_df, opemai_api_key):
    """
    Analyses the emoji frequency data with GPT4o-model
    input:
      chat_emoji_df (pd.DataFrame): dataframe of emojis
      opemai_api_key (str): opemai api key
    output:
      str: analusis of emoji usage
    """
    client = openai.OpenAI(api_key=opemai_api_key)
    comparison_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", 
                   "content": f"You are a text analyst specialising in youtube comment. This is a dataframe of emoji appeared on live chat comments. What can you infer from this? Provide a concise analysis of one paragraph.:{chat_emoji_df.to_markdown()}"}],
        temperature=0.7
    )
    return comparison_response.choices[0].message.content


def gpt_summary(text_list, opemai_api_key):
    """
    Summarizes the texts as a whole using GPT4o-model
    input:
      text_list (list): list of texts to summarize
    output:
      str: summary text of the list
    """
    sample_size = min(500, len(text_list))  # Ensure we don't sample more than available
    selected_text = random.sample(text_list, sample_size)
    combined_text = "\n".join(selected_text) #take 500 random samples

    prompt = f"""
        You are a text analyst specialising in youtube comments. 
        Summarize the following YouTube messages into a concise paragraph that captures the main themes, sentiments, and topics. 
        Output must be in English. Report in Markdown format but do not use headings.:

        {combined_text}

        """
    client = openai.OpenAI(api_key=opemai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def get_sentiment_polarity(text):
    """
    Returns the polarity of a text string using TextBlob
    Input:
      text (str): text to get the polarity
    Output:
      float: polarity numer (ranges from -1 (negative) to 1 (positive))
    """
    return TextBlob(text).sentiment.polarity


def categorize_sentiment(polarity):
    """
    Returns the polarity category
    input:
      polarity (int): polarity number
    output:
      str: category of the polarity
    """
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


def sentiment_analysis(text_list, sample_num=100):
    """
    Returns numerical information of each polarity categories
    input:
      text_list (list): list of texts to summarize
    output:
      dict: counts and percentage of each polarity category
    """
    sentiments = [categorize_sentiment(get_sentiment_polarity(t)) for t in text_list]
    total = len(sentiments)
    if total == 0:
        return {"positive":0, "negative":0, "neutral":0, "percent_positive":0, "percent_negative":0, "percent_neutral":0}

    pos_count = sentiments.count("positive")
    neg_count = sentiments.count("negative")
    neu_count = sentiments.count("neutral")

    return {
        "positive": pos_count,
        "negative": neg_count,
        "neutral": neu_count,
        "percent_positive": (pos_count / total)*100,
        "percent_negative": (neg_count / total)*100,
        "percent_neutral":  (neu_count / total)*100
    }


def compare_chats_and_comments(chats_summary, comments_summary, chats_sentiment, comments_sentiment, other_analysis, opemai_api_key):
    """
    Highlights the difference between chat and comment messages based on summaries and sentimental analysis using GPT-4o
    input:
      chats_summary (str): summary text of chats
      comments_summary (str): summary text of comments
      chats_sentiment (dict): counts and percentages of chat sentiment categories
      comments_sentiment (dict): counts and percentages of comment sentiment categories
      other_analysis (list): list of other analysis texts
    output:
      str: comparison analysis result made by GPT-4o
    """
    comparison_prompt = f"""
        You are a text analyst specialising in youtube comment. I have two sets of information:
      

        1. Chats summary:
        {chats_summary}

        Messages sentiment distribution:
        - Positive: {chats_sentiment['percent_positive']:.2f}%
        - Negative: {chats_sentiment['percent_negative']:.2f}%
        - Neutral: {chats_sentiment['percent_neutral']:.2f}%

        2. Comments summary:
        {comments_summary}

        Comments sentiment distribution:
        - Positive: {comments_sentiment['percent_positive']:.2f}%
        - Negative: {comments_sentiment['percent_negative']:.2f}%
        - Neutral: {comments_sentiment['percent_neutral']:.2f}%

        3. Other analysis:
        {' '.join(other_analysis)}

        Provide a concise summary highlighting the main differences in themes, sentiments, and words used between the comments and the messages.
        """
      
    client = openai.OpenAI(api_key=opemai_api_key)
    comparison_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": comparison_prompt}],
        temperature=0.7
    )
    difference_summary = comparison_response.choices[0].message.content
    return difference_summary


