from pathlib import Path
from openai import OpenAI
import ml
import os 

# TODO: Do not want to keep overwriting audio files. You may want to delete them at the end. 
def text_to_speech(text, filename): 
  # Construct the path to the directory where the file will be saved
  audio_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_files")
  # Ensure the directory exists
  if not os.path.exists(audio_files_dir):
    os.makedirs(audio_files_dir)
    
  # Construct the full path for the audio file
  speech_file_path = os.path.join(audio_files_dir, filename)
  
  response = client.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input=text
  )
  
  response.stream_to_file(speech_file_path)
  

if __name__ == "__main__": 
  client = OpenAI()
  
  # text = "Joy is a Stanford sophomore who likes saying the word based and index a lot. His new glasses make him look like harry potter. He is also a part time rizz god. "
  # filename = "test_speech.mp3"
  
  # text_to_speech(text=text, filename=filename)
  
  response = ml.call_gpt_model("What is the ending balance in this bank statement?", "Month: June, Ending balance: 200", "gpt-4")
  print(response.choices[0].message.content)
  

