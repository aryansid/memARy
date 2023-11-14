# Dump of functions I'm testing right now 
# Ignore 

from pathlib import Path
from openai import OpenAI
import ml
import os 
import base64
import requests

from dotenv import load_dotenv
import openai

load_dotenv()
openai_api_key = os.getenv("openai_api_key")

client = OpenAI()

# # TODO: Do not want to keep overwriting audio files. You may want to delete them at the end. 
# def text_to_speech(text, filename): 
#   # Construct the path to the directory where the file will be saved
#   audio_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_files")
#   # Ensure the directory exists
#   if not os.path.exists(audio_files_dir):
#     os.makedirs(audio_files_dir)
    
#   # Construct the full path for the audio file
#   speech_file_path = os.path.join(audio_files_dir, filename)
  
#   response = client.audio.speech.create(
#     model="tts-1",
#     voice="shimmer",
#     input=text
#   )
  
#   response.stream_to_file(speech_file_path)
 
# def speech_to_text(filepath):
#   try: 
#     audio_file = open(filepath, "rb")
#     transcript = client.audio.transcriptions.create(
#     model="whisper-1", 
#     file=audio_file, 
#     prompt="The transcript is about a blind person asking about their environment",
#     response_format="text"
#     )
#   except Exception as e: 
#     return f"An unexpected error occurred: {str(e)}"
  
# Don't delete
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# if __name__ == "__main__": 
#   image_path = "biker.jpg"
#   base64_image = encode_image(image_path)
  
#   headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {openai.api_key}"
#   }
  
#   payload = {
#     "model": "gpt-4-vision-preview",
#     "messages": [
#       {
#         "role": "system", 
#         "content": "You are tasked with answering a blind individual's question about their current environment. Aim for brevity without sacrificing the immersive experience."
#       },
#       {
#         "role": "user",
#         "content": [
#           {
#             "type": "text",
#             "text": "What's happening around me?"
#           },
#           {
#             "type": "image_url",
#             "image_url": {
#               "url": f"data:image/jpeg;base64,{base64_image}"
#             }
#           }
#         ]
#       }
#     ],
#     "max_tokens": 300
#   }
  
#   response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  
#   print(response.json()['choices'][0]['message']['content'])
  
  
 
  

