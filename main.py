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
  
      dense_captions = ml.get_dense_captions(filepath)
      print("Received dense captions from Azure.")
    
      PROMPT = "You are tasked with answering a blind individual's question based on dense captions that describe their current environment. Use these captions to construct a spatially organized and immersive answer. Prioritize objects with the highest confidence scores. Aim for brevity without sacrificing the experience."
      # PROMPT = "You are a sophisticated AI guide who translates the visually descriptive dense captions into precise and straightforward answers to a blind individual's questions. Your task is to weave these dense captions into a concise yet informative response, focusing on objects with higher confidence scores or those most relevant to the question. The goal is to make the experience as seamless and immersive as possible for the blind user."
      if question: 
        PROMPT += f"\n\nUser's Question: {question}"
      gpt_response = ml.call_gpt_model(PROMPT, json.dumps(dense_captions, indent=4), "gpt-3.5-turbo")
      print("GPT-3 response received.")
      
      audio_directory = './audio_files'  
      if not os.path.exists(audio_directory):
          os.makedirs(audio_directory)

      audio_filename = os.path.join(audio_directory, f"audio_{uuid.uuid4()}.wav")
      ml.text_to_audio(gpt_response, audio_filename, os.getenv("tts_subscription_key"), os.getenv("tts_region"))
      print(f"Audio file generated.")
      print(f"Directory: {os.path.dirname(audio_filename)}, Filename: {os.path.basename(audio_filename)}")
    
      audio_url = f"/audio/{os.path.basename(audio_filename)}"
      return jsonify({"audio_url": audio_url})
  
  except Exception as e: 
    print(f"Caught exception: {e}")  
    return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__": 
  app.run(debug=True)
  
  # TODO: Decide whether to temporarily storage image or send direct byte stream