const video = document.getElementById('camera-feed');
const canvas = document.getElementById('output-canvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('start-button');
let isProcessing = false;

// Access the camera feed
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Camera access error:", err);
    });

function processFrame() {
    if (!isProcessing) return;

    // Draw the video frame to the canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameData = canvas.toDataURL('image/jpeg');

    // Send the frame to the Flask backend
    fetch('/process_frame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frame: frameData }),
    })
    .then(response => response.json())
    .then(data => {
        const img = new Image();
        img.onload = () => {
            // Draw the processed frame back to the canvas
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            requestAnimationFrame(processFrame);
        };
        img.src = 'data:image/jpeg;base64,' + data.processed_frame;
    })
    .catch(error => {
        console.error('Error processing frame:', error);
        requestAnimationFrame(processFrame);
    });
}

// Set canvas size once video metadata is loaded
video.addEventListener('loadedmetadata', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
});

// Start/stop the detection loop
startButton.addEventListener('click', () => {
    isProcessing = !isProcessing;
    startButton.textContent = isProcessing ? 'Stop Detection' : 'Start Detection';
    if (isProcessing) {
        processFrame();
    }
});
