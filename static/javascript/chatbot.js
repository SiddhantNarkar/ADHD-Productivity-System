function toggleChat() {
    const chat = document.getElementById('aiChatWidget');
    chat.style.display = (chat.style.display === 'flex') ? 'none' : 'flex';
}

function handleEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');
    const message = input.value.trim();

    if (!message) return;

    // User bubble
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user';
    userBubble.textContent = message;
    chatBody.appendChild(userBubble);

    input.value = "";
    chatBody.scrollTop = chatBody.scrollHeight;

    // Typing indicator
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-bubble bot';
    typingBubble.textContent = "🤖 typing…";
    chatBody.appendChild(typingBubble);
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        typingBubble.textContent = data.reply;

    } catch (error) {
        typingBubble.textContent = "Oops 😅 something went wrong. Try again?";
    }

    chatBody.scrollTop = chatBody.scrollHeight;
}

function getCSRFToken() {
    const name = "csrftoken=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name)) {
            return cookie.substring(name.length);
        }
    }
    return "";
}


async function clearChatMemory() {
    const chatBody = document.getElementById('chatBody');

    try {
        await fetch("/api/chat/clear/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        });
    } catch (error) {
        console.error("Failed to clear chat memory");
    }

    // Clear UI chat
    chatBody.innerHTML = `
        <div class="chat-bubble bot">
            👋 Fresh start! How can I help you now?
        </div>
    `;
}
