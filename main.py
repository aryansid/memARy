import ml, utils 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import json, os, uuid

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

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
    
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(filepath)
      print(f"Saved file to {filepath}")
      
      base64_image = utils.encode_image(filepath)
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
