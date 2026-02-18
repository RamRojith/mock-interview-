document.addEventListener('DOMContentLoaded', () => {
    const recordBtn = document.getElementById('record-btn');
    const stopBtn = document.getElementById('stop-btn');
    const statusDiv = document.getElementById('status');
    // Fix: ID in HTML is 'question-text', not 'question-box' for the inner text
    const questionText = document.getElementById('question-text');
    const feedbackContainer = document.getElementById('feedback-container');
    const feedbackText = document.getElementById('feedback-text');
    const scoreSpan = document.getElementById('score');
    const audioPlayer = document.getElementById('audio-player');

    // --- INITIALIZATION ---
    if (typeof INITIAL_QUESTION !== 'undefined' && INITIAL_QUESTION) {
        questionText.textContent = INITIAL_QUESTION;
    }

    if (typeof INITIAL_AUDIO_URL !== 'undefined' && INITIAL_AUDIO_URL) {
        audioPlayer.src = INITIAL_AUDIO_URL;
        audioPlayer.style.display = 'block';
        // Auto-play might be blocked by browser policy without interaction, but we can try
        audioPlayer.play().catch(e => console.log("Auto-play prevented (user interaction needed):", e));
    }
    // ---------------------

    let mediaRecorder;
    let audioChunks = [];

    // Helper to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Initialize Audio
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = sendAudio;
        })
        .catch(err => {
            console.error("Error accessing microphone:", err);
            statusDiv.textContent = "Error: Microphone access denied.";
            recordBtn.disabled = true;
        });

    recordBtn.addEventListener('click', () => {
        audioChunks = [];
        mediaRecorder.start();
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        statusDiv.textContent = "Recording...";
        recordBtn.textContent = "Recording...";
    });

    stopBtn.addEventListener('click', () => {
        mediaRecorder.stop();
        recordBtn.disabled = false;
        stopBtn.disabled = true;
        statusDiv.textContent = "Processing...";
        recordBtn.textContent = "🎤 Start Answer";
    });

    async function sendAudio() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' }); // Default browser mime might be webm/ogg. Backend handles it?
        // We'll trust backend (ffmpeg) to handle headers/conversion if needed or just save.

        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'response.wav');
        formData.append('session_id', SESSION_ID);
        // We can optionally pass question_id if we track it.

        try {
            const response = await fetch('/api/process-response/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            handleResponse(data);
        } catch (error) {
            console.error('Error:', error);
            statusDiv.textContent = "Error sending response.";
        }
    }

    function handleResponse(data) {
        statusDiv.textContent = "Ready";

        // Show Feedback
        if (data.feedback) {
            feedbackContainer.style.display = 'block';
            feedbackText.textContent = data.feedback;
            scoreSpan.textContent = data.score;
        }

        // Update Next Question
        if (data.next_question) {
            questionText.textContent = data.next_question.text;
        } else {
            questionText.textContent = "Interview Completed.";
            recordBtn.disabled = true;
        }

        // Play Audio
        if (data.audio_url) {
            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = 'block';
            audioPlayer.play().catch(e => console.log("Auto-play prevented:", e));
        }
    }
});
