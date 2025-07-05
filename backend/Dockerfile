FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from transformers import BlipProcessor, BlipForConditionalGeneration; \
    BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base'); \
    BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')"

CMD ["python", "app.py"]
