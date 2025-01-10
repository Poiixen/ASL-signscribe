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
        console.error("Error accessing the camera:", err);
    });
    
function processFrames() {
    if (!isProcessing) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    requestAnimationFrame(processFrames);

    const frameData = canvas.toDataURL('image/jpeg');

    video.addEventListener('loadedmetadata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
    });

    startButton.addEventListener('click', () => {
        isProcessing = !isProcessing;
        startButton.textContent = isProcessing ? 'Stop Detection' : 'Start Detection';
        if (isProcessing) {
            processFrames();
        }
    });
};