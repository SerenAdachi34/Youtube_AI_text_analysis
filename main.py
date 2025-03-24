import os
import subprocess
from getpass import getpass


# Retrieve API keys and video id
youtube_api_key = getpass("Enter your YouTube API Key: ")
openai_api_key = getpass("Enter your OpenAI API Key: ")
video_id = input("Enter the YouTube Video ID: ")
print("API keys and video id have been set successfully. Running scripts...\n")

# Youtube API
env_data_collection = os.environ.copy()
env_data_collection["YOUTUBE_API_KEY"] = youtube_api_key
# OPENAI API
env_ai_analysis = os.environ.copy()
env_ai_analysis["OPENAI_API_KEY"] = openai_api_key

# Run the YouTube data collection script-----------
print("Extracting YouTube live chats and comments...")
subprocess.run(["python", "src/data_collection/data_collection.py", video_id], check=True, env=env_data_collection)
print("YouTube data extraction completed.\n")

# Run the NLP script-----------
print("Processing text data and generating plots...")
subprocess.run(["python", "src/nlp_analysis/process_text.py", video_id], check=True)
print("NLP processing completed.\n")

# Run the AI analysis script-----------
print("Running AI-based analysis...")
subprocess.run(["python", "src/ai_analysis/ai_analysis.py", video_id], check=True, env=env_ai_analysis)
print("AI analysis completed.\n")

print("All processes completed successfully!")  