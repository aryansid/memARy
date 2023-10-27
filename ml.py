import http.client, urllib.request, urllib.parse, urllib.error, base64, json, os, openai
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("openai_api_key")

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
    response = openai.ChatCompletion.create(**api_params)
    response_content = response['choices'][0]['message']['content'].strip()

    return response_content

  except Exception as e:
    raise RuntimeError(f"An error occurred while making an API call: {e}")
  
def text_to_audio(text, audio_filename, subscription_key, region):
    """Converts text to audio and saves it to a file.

    Parameters:
    - text (str): The text to convert.
    - audio_filename (str): The name of the audio file to save.
    - subscription_key (str): Azure subscription key for Text to Speech.
    - region (str): Azure region where your Text to Speech service is hosted.
    """

    # Configure speech synthesis
    speech_config = SpeechConfig(subscription=subscription_key, region=region)
    audio_config = AudioConfig(filename=audio_filename)

    # Create a speech synthesizer
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Convert text to speech
    result = synthesizer.speak_text_async(text).get()

    # Check for successful conversion
    if result.reason == 0:  # 0 denotes failure
        raise Exception(f"Text-to-speech failed: {result.error_details}")

    print(f"Text-to-speech succeeded. Audio saved as {audio_filename}")