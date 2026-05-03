const API_URL = "http://127.0.0.1:8000/chat";
const API_KEY = "mysecret123";

function addMessage(text, className) {
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerText = text;
    document.getElementById("chatBox").appendChild(div);

    // Auto scroll to latest message
    div.scrollIntoView({ behavior: "smooth" });
}

async function sendMessage() {
    const input = document.getElementById("query");
    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    input.focus();

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            },
            body: JSON.stringify({ query: text })
        });

        const data = await res.json();
        addMessage(data.response, "bot");

    } catch (error) {
        addMessage("Error connecting to server", "bot");
        console.error(error);
    }
}

// 🔥 ENTER KEY SUPPORT
document.getElementById("query").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault(); // prevents weird form behavior
        sendMessage();
    }
});