const video = document.getElementById('camera-feed');
const canvas = document.getElementById('output-canvas');
const ctx = canvas.getContext('2d');
let frameCounter = 0;
const PROCESS_EVERY_NTH_FRAME = 5; // Process every 5th frame

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;

        // Start processing frames when the video feed is ready
        video.addEventListener('loadeddata', () => {
            processFrame(); // Start live processing
        });
    })
    .catch(err => {
        console.error("Error accessing camera:", err);
        alert("Please allow camera access to use this feature.");
    });

function processFrame() {
    // Skip frames to reduce backend load
    frameCounter++;
    if (frameCounter % PROCESS_EVERY_NTH_FRAME !== 0) {
        requestAnimationFrame(processFrame);
        return;
    }

    const TARGET_WIDTH = 320; // Reduce to 320px width
    const TARGET_HEIGHT = (video.videoHeight / video.videoWidth) * TARGET_WIDTH;
    canvas.width = TARGET_WIDTH;
    canvas.height = TARGET_HEIGHT;

    // Draw the current video frame on the canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to Base64 image
    const frameData = canvas.toDataURL('image/jpeg');

    // Send frame to backend for processing
    fetch('/process_frames', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frame: frameData }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error from backend:", data.error);
                return;
            }

            // Render processed frame on the canvas
            const img = new Image();
            img.onload = () => {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            };
            img.src = 'data:image/jpeg;base64,' + data.processed_frame;
        })
        .catch(error => {
            console.error("Error processing frame:", error);
        });

    // Request next frame
    requestAnimationFrame(processFrame);
}
