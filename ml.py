import http.client, urllib.request, urllib.parse, urllib.error, base64, json, os, openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("openai_api_key")

def get_dense_captions(image_url): 
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

  # Set up the image URL to analyze
  body = json.dumps({"url": image_url})

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