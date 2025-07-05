from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)
CORS(app, resources={r"/caption": {"origins": "*"}})

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/caption', methods=['POST'])
def caption_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    print("📷 Received image:", image_file.filename)

    try:
        image = Image.open(image_file.stream).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

    # Process image and generate caption
    inputs = processor(images=image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)

    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
