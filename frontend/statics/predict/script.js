// script.js
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', function() {
    // Toggle active/inactive classes on sidebar
    if (navLinks.classList.contains('inactive')) {
        navLinks.classList.remove('inactive');
        navLinks.classList.add('active');
    } else {
        navLinks.classList.remove('active');
        navLinks.classList.add('inactive');
    }
});

// Handle form submission
document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    // Create FormData to send the image file
    const formData = new FormData();
    formData.append('file', file);

    // Send the file to the backend for prediction
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the result
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
        } else {
            resultDiv.textContent = `Prediction: ${data.prediction}, Confidence: ${data.confidence.toFixed(2)}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
