import ml 
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

@app.route('/process', methods=['POST'])
def process(): 
  try: 
    # image_url = request.form['image_url']
    
    print("Received request to process image.")
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(filepath)
      print(f"Saved file to {filepath}")
  
      dense_captions = ml.get_dense_captions(filepath)
      print("Received dense captions from Azure.")
    
      PROMPT = """You are a precise narrator assisting a blind individual in real-time. Your task is to create a brief, yet spatially organized and immersize description of their surroundings based on the data provided. Start by describing what's near them and then systematically move to distant objects. Prioritize and include only essential details that signficantly contribute to an immersive experience. Aim for brevity but don't sacrifice the essence of the experience."""
      gpt_response = ml.call_gpt_model(PROMPT, json.dumps(dense_captions, indent=4), "gpt-3.5-turbo")
      print("GPT-3 response received.")
      
      audio_directory = './audio_files'  # Choose a directory to save audio files
      if not os.path.exists(audio_directory):
          os.makedirs(audio_directory)

      audio_filename = os.path.join(audio_directory, f"audio_{uuid.uuid4()}.wav")
      ml.text_to_audio(gpt_response, audio_filename, os.getenv("tts_subscription_key"), os.getenv("tts_region"))
      print(f"Audio file generated.")
    
      return send_from_directory(directory=os.path.dirname(audio_filename), 
                                   filename=os.path.basename(audio_filename), 
                                   as_attachment=True,
                                   mimetype='audio/wav')
  
  except Exception as e: 
    return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__": 
  app.run(debug=True)
  
  # TODO: Decide whether to temporarily storage image or send direct byte stream