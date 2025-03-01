from flask import Flask, render_template, request, jsonify
from PIL import Image
from main import hotdogLinearModel
import torch

# Initialize your model (make sure its signature matches your usage)
model = hotdogLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=1)
model.load_state_dict(torch.load('hotdogModel.pt'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        try:
            # Open the image using the file stream instead of a file path
            image = Image.open(file.stream)
        except Exception as e:
            return jsonify({'error': 'Invalid image file'})
        
        # Call the classification function (replace with your model inference)
        result, confidence = model.predict(image)
        print(result)
        return jsonify({
            'result': 'hotdog' if result == 'hotdog' else 'not hotdog'
        })
    return jsonify({'error': 'Unknown error'})

if __name__ == '__main__':
    app.run(debug=True)
