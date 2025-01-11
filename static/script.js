const video = document.getElementById('camera-feed');
const canvas = document.getElementById('output-canvas');
const ctx = canvas.getContext('2d');
let frameCounter = 0;
const PROCESS_EVERY_NTH_FRAME = 5; // Process every 5th frame

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;

        video.addEventListener('loadeddata', () => {
            processFrame(); 
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

    const TARGET_WIDTH = 320; 
    const TARGET_HEIGHT = (video.videoHeight / video.videoWidth) * TARGET_WIDTH;
    canvas.width = TARGET_WIDTH;
    canvas.height = TARGET_HEIGHT;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const frameData = canvas.toDataURL('image/jpeg');

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

            const img = new Image();
            img.onload = () => {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            };
            img.src = 'data:image/jpeg;base64,' + data.processed_frame;
        })
        .catch(error => {
            console.error("Error processing frame:", error);
        });

    requestAnimationFrame(processFrame);
}


