document.addEventListener('DOMContentLoaded', () => {
    const conversationId = 'conv_' + Math.random().toString(36).substring(2, 11);
    let currentMode = 'tutor';
    let useRag = true;
    let isGenerating = false;

    // Warm up the model by hitting the background warmup endpoint
    fetch('/api/warmup').catch(() => {});

    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const ragToggle = document.getElementById('ragToggle');
    const ragBadge = document.getElementById('ragBadge');
    const modeCards = document.querySelectorAll('.mode-card');
    const currentModeIcon = document.getElementById('currentModeIcon');
    const currentModeTitle = document.getElementById('currentModeTitle');

    // Modal elements
    const uploadModalBtn = document.getElementById('uploadModalBtn');
    const uploadModal = document.getElementById('uploadModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');

    const modeDetails = {
        tutor: { icon: '🎓', title: 'Tutor Mode' },
        quiz: { icon: '❓', title: 'Quiz Mode' },
        interview: { icon: '💼', title: 'Interview Mode' }
    };

    // Mode Selection Handler
    modeCards.forEach(card => {
        card.addEventListener('click', () => {
            modeCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            currentMode = card.dataset.mode;
            currentModeIcon.textContent = modeDetails[currentMode].icon;
            currentModeTitle.textContent = modeDetails[currentMode].title;
        });
    });

    // RAG Toggle Handler
    ragToggle.addEventListener('change', (e) => {
        useRag = e.target.checked;
        if (useRag) {
            ragBadge.textContent = 'RAG Enabled';
            ragBadge.className = 'badge badge-rag';
        } else {
            ragBadge.textContent = 'RAG Disabled';
            ragBadge.className = 'badge badge-rag off';
        }
    });

    // New Session
    newChatBtn.addEventListener('click', () => {
        location.reload();
    });

    // Input auto-resize
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const text = userInput.value ? userInput.value.trim() : '';
        if (!text || isGenerating) return;

        const welcomeMsg = document.querySelector('.welcome-message');
        if (welcomeMsg) welcomeMsg.remove();

        appendMessage('user', text);
        userInput.value = '';
        userInput.style.height = 'auto';

        const assistantBubble = appendMessage('assistant', '');
        const textContainer = assistantBubble.querySelector('.message-text');
        const cursor = document.createElement('span');
        cursor.className = 'cursor-blink';
        textContainer.appendChild(cursor);

        isGenerating = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch('/chat/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    message: text,
                    mode: currentMode,
                    use_rag: useRag
                })
            });

            if (!response.ok) {
                throw new Error(`Server returned status ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let rawText = '';
            let lastUpdate = Date.now();

            function updateUI(force = false) {
                const now = Date.now();
                // Throttle updates to ~20fps to prevent robotic flickering
                if (!force && now - lastUpdate < 50) return;
                lastUpdate = now;

                if (window.marked) {
                    textContainer.innerHTML = marked.parse(rawText);
                } else {
                    textContainer.textContent = rawText;
                }
                textContainer.appendChild(cursor);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                rawText += chunk;
                updateUI();
            }

            // Final render pass
            updateUI(true);
            cursor.remove();
        } catch (err) {
            cursor.remove();
            textContainer.innerHTML += `<br><span style="color:#ef4444;">⚠️ Error: ${err.message}. Ensure backend & Ollama services are running.</span>`;
        } finally {
            isGenerating = false;
            sendBtn.disabled = false;
        }
    }

    function appendMessage(role, content) {
        const row = document.createElement('div');
        row.className = `message-row ${role}`;

        const avatar = document.createElement('div');
        avatar.className = `avatar ${role}`;
        avatar.textContent = role === 'user' ? '👤' : '🤖';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        if (content) {
            textDiv.innerHTML = window.marked ? marked.parse(content) : content;
        }

        bubble.appendChild(textDiv);

        if (role === 'user') {
            row.appendChild(bubble);
            row.appendChild(avatar);
        } else {
            row.appendChild(avatar);
            row.appendChild(bubble);
        }

        chatMessages.appendChild(row);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return bubble;
    }

    // Modal Events
    uploadModalBtn.addEventListener('click', () => uploadModal.classList.add('active'));
    closeModalBtn.addEventListener('click', () => uploadModal.classList.remove('active'));
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', handleFileUpload);

    async function handleFileUpload() {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        uploadStatus.className = 'upload-status';
        uploadStatus.textContent = `Uploading & indexing '${file.name}'...`;

        try {
            const res = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (res.ok) {
                uploadStatus.className = 'upload-status success';
                uploadStatus.textContent = `✅ ${data.message} (${data.chunks_added} chunks indexed)`;
            } else {
                throw new Error(data.detail || 'Upload failed');
            }
        } catch (err) {
            uploadStatus.className = 'upload-status error';
            uploadStatus.textContent = `❌ Upload Error: ${err.message}`;
        }
    }
});
