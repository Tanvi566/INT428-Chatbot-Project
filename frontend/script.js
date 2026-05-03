const API_URL = "http://127.0.0.1:8000/chat";
const API_KEY = "mysecret123";

function addMessage(text, className) {
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerText = text;
    document.getElementById("chatBox").appendChild(div);
}

async function sendMessage() {
    const input = document.getElementById("query");
    const text = input.value;

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

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
}