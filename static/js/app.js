let mediaRecorder;
let socket;
let audioChunks = [];

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statusDiv = document.getElementById('status');
const conversationDiv = document.getElementById('conversation');

// Initialize WebSocket
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    socket = new WebSocket(`${protocol}//${window.location.host}/ws/audio_stream`);

    socket.onopen = () => {
        console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
        const message = event.data;
        
        try {
            const data = JSON.parse(message);
            if (data.type === 'audio_response') {
                playAudio(data.url);
                statusDiv.textContent = "Reproduzindo resposta...";
            }
        } catch (e) {
            // It's a plain text log/message
            logMessage(message);
        }
    };

    socket.onclose = () => {
        console.log("WebSocket disconnected. Reconnecting...");
        setTimeout(connectWebSocket, 1000);
    };
}

startBtn.onclick = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' }); // Chrome uses webm

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
                socket.send(event.data);
            }
        };

        mediaRecorder.start(250); // Send chunks every 250ms
        
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusDiv.textContent = "Gravando...";
        
    } catch (err) {
        console.error("Error accessing microphone", err);
        statusDiv.textContent = "Erro no microfone: " + err.message;
    }
};

stopBtn.onclick = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        
        // Send end signal
        if (socket.readyState === WebSocket.OPEN) {
            socket.send("END");
        }
        
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusDiv.textContent = "Processando...";
    }
};

function logMessage(text) {
    const p = document.createElement('p');
    if (text.startsWith("You said:")) {
        p.className = 'user-msg';
    } else if (text.startsWith("GPT:")) {
        p.className = 'bot-msg';
    }
    p.textContent = text;
    conversationDiv.appendChild(p);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

function playAudio(url) {
    const audio = new Audio(url);
    audio.play();
    audio.onended = () => {
        statusDiv.textContent = "Pronto";
    };
}

connectWebSocket();
