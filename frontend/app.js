const API_URL = "http://127.0.0.1:8000";
 
const sessionId = crypto.randomUUID();
 
const conversation = document.getElementById("conversation");
const micButton = document.getElementById("micButton");
const sendButton = document.getElementById("sendButton");
const messageInput = document.getElementById("messageInput");
const voiceStatus = document.getElementById("voiceStatus");
 
 
// ------------------------------------
// 1. Voice recording setup (MediaRecorder -> Whisper backend)
// ------------------------------------
 
let mediaRecorder = null;
let mediaStream = null;
let audioChunks = [];
let isListening = false;
 
// Pick a recording format the current browser supports.
function getSupportedMimeType() {
 
    const candidates = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/mp4",          // Safari
        "audio/ogg;codecs=opus"
    ];
 
    for (const type of candidates) {
        if (window.MediaRecorder && MediaRecorder.isTypeSupported(type)) {
            return type;
        }
    }
 
    return "";
}
 
function getFileExtension(mimeType) {
 
    if (mimeType.includes("mp4")) return "mp4";
    if (mimeType.includes("ogg")) return "ogg";
    return "webm";
}
 
function stopMicStream() {
 
    if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
        mediaStream = null;
    }
}
 
function setListeningUI(listening) {
 
    isListening = listening;
    micButton.classList.toggle("listening", listening);
}
 
if (!navigator.mediaDevices || !window.MediaRecorder) {
 
    voiceStatus.textContent =
        "Voice recording is not supported in this browser.";
}
 
 
async function startRecording() {
 
    // Stop AI speech so it doesn't get recorded.
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }
 
    try {
 
        mediaStream = await navigator.mediaDevices.getUserMedia({
            audio: {
                echoCancellation: true,
                noiseSuppression: true
            }
        });
 
    } catch (error) {
 
        console.error("Microphone permission error:", error);
 
        voiceStatus.textContent =
            error.name === "NotAllowedError"
                ? "Microphone permission denied. Allow it in the browser address bar."
                : "Unable to access the microphone.";
 
        return;
    }
 
    const mimeType = getSupportedMimeType();
 
    mediaRecorder = new MediaRecorder(
        mediaStream,
        mimeType ? { mimeType } : undefined
    );
 
    audioChunks = [];
 
    mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };
 
    mediaRecorder.onstop = async () => {
 
        stopMicStream();
 
        const finalType = mediaRecorder.mimeType || mimeType || "audio/webm";
        const audioBlob = new Blob(audioChunks, { type: finalType });
 
        // Ignore accidental taps with almost no audio.
        if (audioBlob.size < 1000) {
            voiceStatus.textContent = "Didn't catch that. Click the microphone and try again.";
            return;
        }
 
        await transcribeAndSend(audioBlob, finalType);
    };
 
    mediaRecorder.start();
 
    setListeningUI(true);
    voiceStatus.textContent = "Listening... Click the microphone again when done";
}
 
 
function stopRecording() {
 
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
 
    setListeningUI(false);
}
 
 
async function transcribeAndSend(audioBlob, mimeType) {
 
    voiceStatus.textContent = "Transcribing...";
 
    sendButton.disabled = true;
    micButton.disabled = true;
 
    let transcript = "";
 
    try {
 
        const formData = new FormData();
 
        // Field name must be "file" to match the FastAPI endpoint.
        formData.append(
            "file",
            audioBlob,
            `speech.${getFileExtension(mimeType)}`
        );
 
        const response = await fetch(`${API_URL}/transcribe`, {
            method: "POST",
            body: formData
        });
 
        if (!response.ok) {
            throw new Error(`Transcription error: ${response.status}`);
        }
 
        const data = await response.json();
        transcript = (data.transcript || "").trim();
 
    } catch (error) {
 
        console.error("Transcription error:", error);
 
        voiceStatus.textContent =
            "Transcription failed. Check whether the backend is running.";
 
        sendButton.disabled = false;
        micButton.disabled = false;
        return;
    }
 
    sendButton.disabled = false;
    micButton.disabled = false;
 
    if (!transcript) {
        voiceStatus.textContent = "Didn't catch that. Click the microphone and try again.";
        return;
    }
 
    messageInput.value = transcript;
 
    await sendMessage(transcript);
}
 
 
// ------------------------------------
// 2. Add messages to conversation UI
// ------------------------------------
 
function addMessage(text, sender) {
 
    const message = document.createElement("div");
 
    message.classList.add("message");
 
    message.classList.add(
        sender === "user"
            ? "user-message"
            : "assistant-message"
    );
 
    message.textContent = text;
 
    conversation.appendChild(message);
 
    // Automatically scroll to latest message.
    conversation.scrollTop = conversation.scrollHeight;
}
 
 
// ------------------------------------
// 3. Text-to-speech
// ------------------------------------
 
function speakResponse(text) {
 
    if (!("speechSynthesis" in window)) {
        console.warn("Speech synthesis is not supported.");
        return;
    }
 
    // Stop any previous speech.
    window.speechSynthesis.cancel();
 
    const utterance = new SpeechSynthesisUtterance(text);
 
    utterance.lang = "en-IN";
    utterance.rate = 1;
    utterance.pitch = 1;
 
    utterance.onstart = () => {
        voiceStatus.textContent = "AI is speaking...";
    };
 
    utterance.onend = () => {
        voiceStatus.textContent = "Click the microphone to speak";
    };
 
    utterance.onerror = (event) => {
        console.error("Speech synthesis error:", event.error);
        voiceStatus.textContent = "Response received. Speech playback failed.";
    };
 
    window.speechSynthesis.speak(utterance);
}
 
 
// ------------------------------------
// 4. Send message to FastAPI
// ------------------------------------
 
async function sendMessage(text) {
 
    const userMessage = text.trim();
 
    if (!userMessage) {
        return;
    }
 
    addMessage(userMessage, "user");
 
    messageInput.value = "";
 
    sendButton.disabled = true;
    micButton.disabled = true;
 
    voiceStatus.textContent = "AI is thinking...";
 
    try {
 
        const response = await fetch(`${API_URL}/chat`, {
 
            method: "POST",
 
            headers: {
                "Content-Type": "application/json"
            },
 
            body: JSON.stringify({
                session_id: sessionId,
                message: userMessage
            })
 
        });
 
        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }
 
        const data = await response.json();
 
        if (!data.response) {
            throw new Error("No response received from AI.");
        }
 
        // Display AI response.
        addMessage(data.response, "assistant");
 
        // Speak AI response.
        speakResponse(data.response);
 
    } catch (error) {
 
        console.error("Chat error:", error);
 
        addMessage(
            "I'm sorry, I'm unable to connect to the assistant right now. Please try again.",
            "assistant"
        );
 
        voiceStatus.textContent =
            "Connection failed. Check whether the backend is running.";
 
    } finally {
 
        sendButton.disabled = false;
        micButton.disabled = false;
 
    }
}
 
 
// ------------------------------------
// 5. Microphone button
// ------------------------------------
 
micButton.addEventListener("click", () => {
 
    if (!navigator.mediaDevices || !window.MediaRecorder) {
        alert("Your browser doesn't support audio recording. Please use a recent version of Chrome, Edge, Firefox or Safari.");
        return;
    }
 
    if (isListening) {
        stopRecording();
        return;
    }
 
    startRecording();
 
});
 
 
// ------------------------------------
// 6. Send button
// ------------------------------------
 
sendButton.addEventListener("click", () => {
 
    sendMessage(messageInput.value);
 
});
 
 
// ------------------------------------
// 7. Enter key support
// ------------------------------------
 
messageInput.addEventListener("keydown", (event) => {
 
    if (event.key === "Enter") {
        sendMessage(messageInput.value);
    }
 
});
 