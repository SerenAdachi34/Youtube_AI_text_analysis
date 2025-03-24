import pandas as pd

def convert_sentiment_dict_to_df(sentiment_data):
    """ Create a DataFrame from the sentiment dictionary"""
    df = pd.DataFrame({
        "": ["Count", "Percentage"],  # Row labels
        "Positive": [sentiment_data["positive"], f"{sentiment_data['percent_positive']:.2f}%"],
        "Neutral": [sentiment_data["neutral"], f"{sentiment_data['percent_neutral']:.2f}%"],
        "Negative": [sentiment_data["negative"], f"{sentiment_data['percent_negative']:.2f}%"],
    })
    return df


def clean_markdown_string(text):
    """Removes ```markdown at the start and ``` at the end of the string."""
    if text.startswith("```markdown") and text.endswith("```"):
        new_text = text[11:-3].strip()
        return new_text
    return text


def markdown_overall_summary(difference_summary, word_cloud_diff, word_freq_diff, chat_emoji_df, emoji_analysis, 
                             chats_summary, comments_summary, chats_sentiment, comments_sentiment):
    """Generates a well-structured Markdown summary of YouTube chat and comment analysis."""
    
    # Define the markdown content
    md_content = f"""# **YouTube Chat vs. Comment Analysis Report**  

## 🔍 **Key Differences**
{difference_summary}  

---

## **Word Cloud Analysis**
**Chats:**  
![Word Cloud - Chats](results/plots/wordcloud1.jpg)  

**Comments:**  
![Word Cloud - Comments](results/plots/wordcloud2.jpg)  

{word_cloud_diff}  

---

## **Word Frequency Analysis**
**Chats:**  
![Word Frequency - Chats](results/plots/wordfrequency1.jpg)  

**Comments:**  
![Word Frequency - Comments](results/plots/wordfrequency2.jpg)  

{word_freq_diff}  

---

## **Sentiment Analysis**
### **Chat Sentiments**
{convert_sentiment_dict_to_df(chats_sentiment).to_markdown(index=False)}  

### **Comment Sentiments**
{convert_sentiment_dict_to_df(comments_sentiment).to_markdown(index=False)}  

## **Emoji Analysis (Chats)**
{chat_emoji_df[:5].to_markdown(index=False)}  

{emoji_analysis}  

---
## **Summary of Chats**
{chats_summary}  

## **Summary of Comments**
{comments_summary}  

"""

    with open("final_report.md" , "w", encoding="utf-8") as md_file: 
        md_file.write(md_content)