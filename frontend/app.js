const API_URL = "http://127.0.0.1:8000";

const userId = "learner_001";
const threadId = "thread_" + Date.now();

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");


function addMessage(message, type, metadata = null) {

    const wrapper = document.createElement("div");
    wrapper.className = `message ${type}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = type === "user" ? "You" : "AI";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    const text = document.createElement("div");

    if (type === "bot" && typeof marked !== "undefined") {
        text.innerHTML = marked.parse(message);
    } else {
        text.textContent = message;
    }

    bubble.appendChild(text);


    // Metadata
    if (metadata && type === "bot") {

        if (
            metadata.confidence !== undefined
        ) {

            const confidence =
                document.createElement("div");

            confidence.className =
                "response-confidence";

            confidence.textContent =
                `🎯 Confidence: ${Math.round(
                    metadata.confidence * 100
                )}%`;

            bubble.appendChild(confidence);
        }


        if (
            metadata.citations &&
            metadata.citations.length > 0
        ) {

            const sources =
                document.createElement("div");

            sources.className =
                "response-sources";

            const title =
                document.createElement("strong");

            title.textContent =
                "📚 Sources";

            sources.appendChild(title);


            const list =
                document.createElement("ul");

            metadata.citations.forEach(source => {

                const item =
                    document.createElement("li");

                item.textContent = source;

                list.appendChild(item);

            });

            sources.appendChild(list);

            bubble.appendChild(sources);
        }


        if (
            metadata.learning_resources &&
            metadata.learning_resources.length > 0
        ) {

            const resources =
                document.createElement("div");

            resources.className =
                "learning-resources";

            const title =
                document.createElement("strong");

            title.textContent =
                "📖 Related learning";

            resources.appendChild(title);


            const list =
                document.createElement("ul");

            metadata.learning_resources.forEach(resource => {

                const item =
                    document.createElement("li");

                item.textContent = resource;

                list.appendChild(item);

            });

            resources.appendChild(list);

            bubble.appendChild(resources);
        }
    }


    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);

    chatMessages.appendChild(wrapper);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return wrapper;
}


function appendAssistantMessage(text) {

    addMessage(text, "bot");
}


function handleStreamEvent(event) {

    if (event.type === "update") {

        const data = event.data;

        console.log(
            "Graph update:",
            data
        );

        const responseNodes = [
            "rag",
            "web",
            "moderator",
            "blocked",
            "unblocked",
        ];

        responseNodes.forEach(nodeName => {

            const result = data[nodeName];

            if (result && result.answer) {
                appendAssistantMessage(result.answer);
            }
        });
    }

    if (event.type === "done") {
        console.log(
            "Streaming completed."
        );
    }

    if (event.type === "error") {
        console.error(
            "Streaming error:",
            event.message
        );

        appendAssistantMessage(
            `Error: ${event.message}`
        );
    }
}


async function sendStreamingMessage(message) {

    const response = await fetch(
        `${API_URL}/chat/stream`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                thread_id: threadId,
                message: message
            })
        }
    );

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    if (!response.body) {
        throw new Error("Streaming response body is unavailable.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {

        const { value, done } =
            await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(
            value,
            { stream: true }
        );

        const lines = buffer.split("\n");

        buffer = lines.pop();

        for (const line of lines) {

            if (!line.trim()) {
                continue;
            }

            try {

                const event = JSON.parse(line);

                console.log(
                    "Stream event:",
                    event
                );

                handleStreamEvent(event);

            } catch (error) {

                console.error(
                    "Invalid stream JSON:",
                    line
                );
            }
        }
    }
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    messageInput.value = "";
    sendButton.disabled = true;

    try {

        await sendStreamingMessage(message);

    } catch (error) {

        console.error(error);

        appendAssistantMessage(
            `Error: ${error.message}`
        );

    } finally {

        sendButton.disabled = false;
        messageInput.focus();
    }
}


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);