import pandas as pd
import matplotlib.pyplot as plt
import re
import emoji
import MeCab
import japanize_matplotlib
from collections import Counter
from wordcloud import WordCloud

def load_stopwords(file_path="src/nlp_analysis/stopwords.txt"):
    """Loads stopwords from a text file.
    inputs:
        file_path (str): file path to the stop word text file
    outputs:
        list: list of stop words in the text file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            stopwords = {line.strip() for line in f if line.strip()}  # Use a set for faster lookup
        return stopwords
    except FileNotFoundError:
        print(f"Warning: Stopwords file not found at {file_path}. Using an empty stoplist.")
        return set()


def extract_word_of_speeches(dataframe, column_name, stoplist, type_list):
    """
    Extracts a column from a dataframe, separate them by gramatical parts,
    and select meaningful Japanese words that matches the type of gramatical parts.
    inputs:
        dataframe (pd.DataFrame): input dataframe
        column_name (str): column that contains text to extract
        stoplist (list): list of stopwords
        type_list (list): list of part of speeches to be extracted
    outputs:
        list: list of words that matches the part of speech types
    """
    # Initiallise MeCab
    mecab = MeCab.Tagger('-r /usr/local/etc/mecabrc -d /usr/local/lib/mecab/dic/ipadic')

    # Extract and save word that matches type of speeches
    words = []
    for text in dataframe[column_name]:
        if pd.isna(text):
            continue

        # Remove extracted English words from text before passing to MeCab
        cleaned_text = re.sub(r':([A-Za-z_.]+):', '', text)
        node = mecab.parseToNode(cleaned_text)

        # Check each word
        while node:
            word_type = node.feature.split(",")[0]
            if word_type in type_list:
                if node.surface not in stoplist and not node.surface.isdigit():
                    words.append(node.surface.upper())
            node = node.next

    return words


def generate_wordcloud_from_dataframe(dataframe, column_name, stoplist, type_list=["名詞", "形容詞", "動詞"], save_path=None):
    """
    Creage a wordcloud plot for the words that matches the selected part of speeches
    inputs:
        dataframe (pd.DataFrame): input dataframe
        column_name (str): column that includes text to visualise
        stoplist (list): list of stopwords
        type_list (list): list of part of speeches to be extracted. Default is ["Noun", "Verb", "Adjective"]
        save_path (str): path to save the wordcloud. Default does not save the plot.
    outputs:
        None: Visualises the wordcloud
    """
    words = extract_word_of_speeches(dataframe, column_name, stoplist, type_list)

    # Create wordcloud
    wordcloud = WordCloud(
        width=800, height=400, background_color="white",
        font_path="/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"
    ).generate(" ".join(words))

    # Plot wordcloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Wordcloud ({column_name})")
    if save_path:
      plt.savefig(save_path)


def rank_words_from_dataframe(dataframe, column_name, stoplist, top_num=10, type_list=["名詞", "形容詞", "動詞"], save_path=None):
    """
    Create a ranking bar graph that shows the most common words extracted and their frequency
    inputs:
        dataframe (pd.DataFrame): input dataframe
        column_name (str): column that includes text to visualise
        top_num: number of most common words to visualise
        stoplist (list): list of stopwords
        type_list (list): list of part of speeches to be extracted. Default is ["Noun", "Verb", "Adjective"]
        save_path (str): path to save the wordcloud. Default does not save the plot.
    outputs:
        None: Visualise the bar graph
    """
    words = extract_word_of_speeches(dataframe, column_name, stoplist, type_list)

    # Count the frequencies
    word_counts = Counter(words)

    # Extract the top words and their frequency
    top_words = word_counts.most_common(top_num)

    # Plot the bar graph
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title(f"Top {top_num} Words by Frequency ({column_name})")
    plt.xticks(rotation=45)
    if save_path:
      plt.savefig(save_path)

def extract_and_convert_to_emojis(dataframe, column_name, save_path=None):
    """
    Extracts emoji strings in the given column of the dataframe, counts their frequency, and save the data as csv.
    inputs:
        dataframe (pd.DataFrame): Input dataframe
        column_name (str): Name of the column containing text to process
    outputs:
        pd.DataFrame: A dataframe with two columns: "Emoji" and "Frequency", sorted by frequency.
    """
    all_words = []

    # Extract emoji strings in column
    for text in dataframe[column_name]:
        if pd.isna(text):
            continue
        extracted_words = re.findall(r':([A-Za-z_]+):', text) #Assuming all emojis will be in the format of :emoji:
        all_words.extend(extracted_words)

    # Count the frequency of each word
    word_counts = Counter(all_words)

    # Convert words to emojis
    emoji_data = []
    for word, count in word_counts.items():
        emoji_char = emoji.emojize(f":{word.lower()}:", language="alias")
        emoji_data.append((emoji_char, count))

    # Create a dataframe sorted by frequency and save it as csv
    emoji_df = pd.DataFrame(emoji_data, columns=["Emoji", "Frequency"]).sort_values(by="Frequency", ascending=False)
    if save_path:
        emoji_df.to_csv(save_path, index=False, encoding="utf-8")

    return emoji_df