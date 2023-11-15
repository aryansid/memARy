import ml, utils 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json, os, uuid
import googlemaps

load_dotenv()

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
google_maps_key = os.getenv("google_maps")
gmaps = googlemaps.Client(key=google_maps_key)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory(os.path.join('./audio_files'), filename, mimetype='audio/wav')

@app.route('/process', methods=['POST'])
def process(): 
  try: 
        
    print("Received request to process image.")
    file = request.files['file']
    question = request.form['question']
    
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    if latitude and longitude: 
      print(f"Received location data: Latitude = {latitude}, Longitude = {longitude}")
      reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
      readable_address = reverse_geocode_result[0]['formatted_address']
      print(f"The readable address is {readable_address}")
      print("Not implemented into ChatGPT yet")
    else: 
      print("")
    
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(filepath)
      print(f"Saved file to {filepath}")
      
      base64_image = ml.encode_image(filepath)
      gpt_response = ml.call_gpt_vision(base64_image, question)
      print("GPT-4 vision response recieved.")
      
      audio_directory = './audio_files'  
      if not os.path.exists(audio_directory):
          os.makedirs(audio_directory)

      audio_filename = f"audio_{uuid.uuid4()}.mp3"
      audio_path = os.path.join(audio_directory, audio_filename)
      ml.text_to_speech(gpt_response, audio_path)
      print(f"Audio file saved at {audio_path}")
    
      audio_url = request.url_root + "audio/" + audio_filename
      return jsonify({"audio_url": audio_url})
  
  except Exception as e: 
    print(f"Caught exception: {e}")  
    return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__": 
  app.run(debug=True)
  # app.run(host='0.0.0.0', port=5000)
