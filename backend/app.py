from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer
import torch
import re

app = Flask(_name_)
CORS(app, resources={r"/caption": {"origins": "*"}})

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

LANGUAGE_MODELS = {
    'es': 'Helsinki-NLP/opus-mt-en-es',
    'fr': 'Helsinki-NLP/opus-mt-en-fr',
    'de': 'Helsinki-NLP/opus-mt-en-de',
    'it': 'Helsinki-NLP/opus-mt-en-it',
    'pt': 'Helsinki-NLP/opus-mt-en-pt',
    'ru': 'Helsinki-NLP/opus-mt-en-ru',
    'nl': 'Helsinki-NLP/opus-mt-en-nl',
    'zh': 'Helsinki-NLP/opus-mt-en-zh',
    'jp': 'Helsinki-NLP/opus-mt-en-ja',
    'ko': 'Helsinki-NLP/opus-mt-en-ko',
    'ar': 'Helsinki-NLP/opus-mt-en-ar',
    'id': 'Helsinki-NLP/opus-mt-en-id'
}

translation_models = {}
translation_tokenizers = {}

def get_translation_model(language_code):
    if language_code not in translation_models:
        if language_code in LANGUAGE_MODELS:
            model_name = LANGUAGE_MODELS[language_code]
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            translation_models[language_code] = model
            translation_tokenizers[language_code] = tokenizer
        else:
            return None, None
    return translation_models.get(language_code), translation_tokenizers.get(language_code)

def translate_text(text, language_code):
    if language_code == 'en':
        return text
    model, tokenizer = get_translation_model(language_code)
    if not model or not tokenizer:
        return text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def apply_tone_to_caption(caption, tone):
    caption = re.sub(r'^(a picture of |an image of |a photo of )', '', caption, flags=re.IGNORECASE)
    modifiers = {
        'Neutral': lambda x: x,
        'Playful': lambda x: f"{x} - how fun is that!",
        'Professional': lambda x: f"This image depicts {x} with clear visual composition.",
        'Humorous': lambda x: f"Looks like {x} decided to show up for the party!",
        'Poetic': lambda x: f"Behold, a moment of {x}, frozen in time and beauty.",
        'Dramatic': lambda x: f"BEHOLD! {x.upper()} — a spectacle of epic proportions!"
    }
    return modifiers.get(tone, lambda x: x)(caption)

def generate_conditional_caption(image, tone):
    inputs = processor(images=image, return_tensors="pt")
    params = {
        'max_length': 50,
        'num_beams': 5,
        'early_stopping': True,
        'do_sample': True,
        'temperature': 0.7
    }

    if tone == 'Professional':
        params.update({'temperature': 0.5, 'do_sample': False, 'num_beams': 3})
    elif tone == 'Playful':
        params.update({'temperature': 0.9, 'top_p': 0.9})
    elif tone == 'Poetic':
        params.update({'temperature': 0.8, 'top_p': 0.95, 'max_length': 60})

    with torch.no_grad():
        output = model.generate(**inputs, **params)

    return processor.decode(output[0], skip_special_tokens=True)

@app.route('/caption', methods=['POST'])
def caption_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    tone = request.form.get('tone', 'Neutral')
    language = request.form.get('language', 'en')

    try:
        image = Image.open(image_file.stream).convert('RGB')
        base_caption = generate_conditional_caption(image, tone)
        toned_caption = apply_tone_to_caption(base_caption, tone)
        final_caption = translate_text(toned_caption, language)

        return jsonify({
            'caption': final_caption,
            'tone': tone,
            'language': language,
            'original_caption': base_caption
        })
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Captioning API running'})

@app.route('/supported-languages', methods=['GET'])
def supported_languages():
    return jsonify({
        'languages': ['en'] + list(LANGUAGE_MODELS.keys()),
        'tones': ['Neutral', 'Playful', 'Professional', 'Humorous', 'Poetic', 'Dramatic']
    })

if __name__ == '__main__':
    print("Starting server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
