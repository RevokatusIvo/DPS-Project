document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('imageInput');
  const uploadButton = document.getElementById('uploadButton');
  const resultText = document.getElementById('result');
  const loadingText = document.getElementById('loading');
  const preview = document.getElementById('preview');
  uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
      resultText.textContent = 'Please select an image.';
      return;
    }
       // 👉 Show image preview
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';

    const formData = new FormData();
    formData.append('image', file);

    const backendURL = 'http://localhost:5000/caption';

    loadingText.style.display = 'block';
    resultText.textContent = '';

    try {
      const res = await fetch(backendURL, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        throw new Error('Server error');
      }

      const data = await res.json();
      resultText.textContent = `Caption: ${data.caption}`;
    } catch (err) {
      console.error(err);
      resultText.textContent = '❌ Failed to generate caption.';
    } finally {
      loadingText.style.display = 'none';
    }
  });
});
