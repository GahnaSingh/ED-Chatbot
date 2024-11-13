async function captureMedia() {
    try {
        // Access camera and microphone
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        
        // Capture image from video
        const video = document.createElement('video');
        video.srcObject = stream;
        await new Promise(resolve => (video.onloadedmetadata = resolve));
        video.play();
        
        // Take a snapshot
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const imageData = canvas.toDataURL('image/png');
        
        // Capture audio
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.start();
        
        setTimeout(() => {
            mediaRecorder.stop();
        }, 3000); // Record for 3 seconds
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioBase64 = await blobToBase64(audioBlob);

            // Send data to server
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData, audio: audioBase64 })
            });
            const data = await response.json();
            document.getElementById('response').innerText = `Bot says: ${data.response} (Emotion: ${data.emotion})`;
        };

    } catch (error) {
        console.error("Error accessing media devices:", error);
    }
}

function blobToBase64(blob) {
    return new Promise((resolve, _) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(blob);
    });
}

