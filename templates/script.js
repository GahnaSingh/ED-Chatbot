let name = "";
let age = "";

// Handle form submission to start chat
document.getElementById("startForm").addEventListener("submit", function (event) {
    event.preventDefault();
    name = document.getElementById("name").value;
    age = document.getElementById("age").value;

    fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, age: age }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("user-info-form").style.display = "none";
        document.getElementById("chat-container").style.display = "block";
        addMessage("bot", data.message);
    })
    .catch(error => console.error("Error starting chat:", error));
});

// Function to send user message to server
function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    addMessage("user", userInput);
    document.getElementById("userInput").value = "";

    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        const video = document.createElement("video");
        video.srcObject = stream;
        video.play();

        setTimeout(() => {
            const canvas = document.createElement("canvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext("2d");
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/jpeg");

            stream.getTracks().forEach((track) => track.stop());

            // Send message and image data to server
            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput, image_data: imageData }),
            })
            .then(response => response.json())
            .then(data => {
                addMessage("bot", data.response);
            })
            .catch(error => console.error("Error sending message:", error));
        }, 500);
    }).catch(error => {
        console.error("Error accessing camera:", error);
    });
}

// Function to add messages to chatbox
function addMessage(sender, text) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = text;
    document.getElementById("messages").appendChild(messageElement);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}

