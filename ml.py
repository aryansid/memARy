import http.client, urllib.request, urllib.parse, urllib.error, base64, json, os, openai
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, SpeechRecognizer, ResultReason
import openai
from openai import OpenAI
from dotenv import load_dotenv
import requests
import base64

load_dotenv()
openai_api_key = os.getenv("openai_api_key")

client = OpenAI()

def get_dense_captions(image_path=None): 
  # Set up the URL and request headers
  resource_path = '/computervision/imageanalysis:analyze'
  url_parameters = urllib.parse.urlencode({
      'api-version': '2023-04-01-preview',
      'features': 'denseCaptions',
      'language': 'en'
  })
  
  headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.getenv("cv_subscription_key")
  }

  if image_path:
        with open(image_path, 'rb') as f:
            body = f.read()
        headers['Content-Type'] = 'application/octet-stream'
  else:
    raise ValueError("No image path provided.")
  
  try:
      # Connect to the Azure endpoint
      conn = http.client.HTTPSConnection(os.getenv("cv_endpoint"))
      conn.request("POST", f"{resource_path}?{url_parameters}", body, headers)
      response = conn.getresponse()

      # Read and parse the response
      data = json.loads(response.read())
      dense_captions = data.get('denseCaptionsResult', {}).get('values', [])

      # Extract dense captions if available
      if dense_captions:
          return dense_captions
      else:
          print("No dense captions found.")

      # Close the connection
      conn.close()

  except Exception as e:
      print(f"An error occurred: {e}")
      
def call_gpt_model(prompt, data, model, temperature=None):
  messages = [
      {"role": "system", "content": prompt},
      {"role": "user", "content": data}
  ]

  api_params = {
      "model": model,
      "messages": messages
  }

  if temperature is not None:
    api_params["temperature"] = temperature

  try:
    response = client.chat.completions.create(**api_params)
    response_content = response.choices[0].message.content.strip()

    return response_content

  except Exception as e:
    raise RuntimeError(f"An error occurred while making an API call: {e}")
  
def call_gpt_vision(base64_image, user): 
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
  }
  
  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "system", 
        "content": "You are tasked with answering a blind individual's question about their current environment. Aim for brevity without sacrificing the immersive experience."
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": user
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }
  
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  
  return response.json()['choices'][0]['message']['content']
  
  
# def text_to_audio(text, audio_filename):
#     """Converts text to audio and saves it to a file.

#     Parameters:
#     - text (str): The text to convert.
#     - audio_filename (str): The name of the audio file to save.
#     - subscription_key (str): Azure subscription key for Text to Speech.
#     - region (str): Azure region where your Text to Speech service is hosted.
#     """

#     # Configure speech synthesis
#     speech_config = SpeechConfig(subscription=os.getenv("speech_subscription_key"), region=os.getenv("speech_region"))
#     audio_config = AudioConfig(filename=audio_filename)

#     # Create a speech synthesizer
#     synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

#     # Convert text to speech
#     result = synthesizer.speak_text_async(text).get()

#     # Check for successful conversion
#     if result.reason == 0:  # 0 denotes failure
#         raise Exception(f"Text-to-speech failed: {result.error_details}")

#     print(f"Text-to-speech succeeded. Audio saved as {audio_filename}")

def text_to_speech(text, filepath):   
  try: 
    response = client.audio.speech.create(
      model="tts-1",
      voice="shimmer",
      input=text
    )
    response.stream_to_file(filepath)
    
  except Exception as e: 
    raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    
# def audio_to_text(file_path): 
#   speech_config = SpeechConfig(subscription=os.getenv("speech_subscription_key"), region=os.getenv("speech_region"))
#   audio_config = AudioConfig(filename=file_path)
  
#   speech_recognizer = SpeechRecognizer(speech_config=speech_config)
  
#   print("Starting speech recognition ...")
#   result = speech_recognizer.recognize_once()
#   print("Speech recongition complete. Analyzing ...")
  
#   if result.reason == ResultReason.RecognizedSpeech:
#     return result.text
#   elif result.reason == ResultReason.NoMatch:
#     return "No speech could be recognized."
#   elif result.reason == ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     return f"Speech Recognition canceled: {cancellation_details.reason}"
#   else:
#     return "An unknown error occurred."

def speech_to_text(filepath):
  try: 
    audio_file = open(filepath, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file, 
      prompt="The transcript is about a blind person asking about their environment",
      response_format="text"
    )
  except Exception as e: 
    return f"An unexpected error occurred: {str(e)}"