# Image Caption Generator

This project is a web application that automatically generates captions for images uploaded by users. It uses a powerful AI model from Salesforce, which is **BLIP (Bootstrapping Language-Image Pretraining)**, integrated with **Flask** (Python), **HTML**, **Tailwind CSS**, and **JavaScript**.

## Features

- Generate the caption based on user's uploaded image

## Tech Stack

| Frontend     | Backend           | AI/ML Model       |
|--------------|-------------------|-------------------|
| HTML, JS     | Python (Flask)    | BLIP (HuggingFace Transformers) |
| Tailwind CSS | Flask-CORS        | Salesforce/blip-image-captioning-base |

## Hw It Works

1. User uploads an image through the frontend.
2. Image is sent to `/caption` API endpoint (`POST` method).
3. Flask reads the image and uses BLIP to generate a caption.
4. Caption is returned as a JSON response and displayed to the user.
