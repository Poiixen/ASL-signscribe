
const webcamVideo = document.getElementById("webcamVideo");
const canvas = document.getElementById("canvas");

/*const constraints = {
    video: {
        width: {min: 300, ideal: 500},
        height: {min: 500, ideal: 720}
    }
}*/

navigator.mediaDevices.getUserMedia({ video: true}).then((stream) => {
    webcamVideo.srcObject = stream;
}).catch((error) => {
    console.error(error);
})

