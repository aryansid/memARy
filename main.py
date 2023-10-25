import ml 
from flask import Flask, request, jsonify, send_file, render_template, make_response
import json 

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process(): 
  try: 
    image_url = request.form['image_url']
  
    dense_captions = ml.get_dense_captions(image_url)
    
    PROMPT = """You are a precise narrator assisting a blind individual in real-time. Your task is to create a brief, yet spatially organized and immersize description of their surroundings based on the data provided. Start by describing what's near them and then systematically move to distant objects. Prioritize and include only essential details that signficantly contribute to an immersive experience. Aim for brevity but don't sacrifice the essence of the experience."""
    
    gpt_response = ml.call_gpt_model(PROMPT, json.dumps(dense_captions, indent=4), "gpt-3.5-turbo")
    
    return make_response(render_template('response.html', gpt_response=gpt_response), 200)
  
  except Exception as e: 
    return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__": 
  app.run(debug=True)
  
  # TODO: Decide whether to temporarily storage image or send direct byte stream