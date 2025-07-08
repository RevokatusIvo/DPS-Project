document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('imageInput');
  const uploadButton = document.getElementById('uploadButton');
  const resultText = document.getElementById('resultText');
  const resultContainer = document.getElementById('result');
  const loadingText = document.getElementById('loading');
  const preview = document.getElementById('preview');

  const toneSelect = document.getElementById('toneSelect');
  const languageSelect = document.getElementById('languageSelect');

  uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    const tone = toneSelect.value;
    const language = languageSelect.value;

    resultText.textContent = '';
    resultContainer.classList.add('hidden');

    if (!file) {
      resultText.textContent = 'Please select an image.';
      resultContainer.classList.remove('hidden');
      return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';

    const formData = new FormData();
    formData.append('image', file);
    formData.append('tone', tone);
    formData.append('language', language);

    const backendURL = 'http://localhost:5000/caption';

    loadingText.style.display = 'block';

    try {
      const res = await fetch(backendURL, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Server error');

      const data = await res.json();
      resultText.textContent = data.caption
      ? Caption: ${data.caption}
      : 'No caption returned.';

      resultText.classList.remove('hidden');
      resultText.style.display = 'block'; 
      resultContainer.classList.remove('hidden');


    } catch (err) {
      console.error(err);
      resultText.textContent = 'Failed to generate caption.';
      resultContainer.classList.remove('hidden');
    } finally {
      loadingText.style.display = 'none';
    }
  });
});
