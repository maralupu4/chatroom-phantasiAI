// Get data from a hidden element
const roomData = document.getElementById("room-data");
const roomId = roomData.getAttribute("data-room-id");
const username = roomData.getAttribute("data-username");
const userId = roomData.getAttribute("data-user-id");

// pick ws:// or wss:// depending on http/https
const scheme = window.location.protocol === "https:" ? "wss" : "ws";

// use the same host (IP/domain + port) the page was loaded from
const host = window.location.host; // 10.36.138.226:8000

// build WebSocket URL
const ws = new WebSocket(`${scheme}://${host}/ws/chat/${roomId}/${userId}?username=${username}`);

// set up WebSocket connection
//const ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/${userId}?username=${username}`);
// set up WebSocket connection - use current hostname so it works from any computer
//const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
//const ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${roomId}/${userId}?username=${username}`);

// event trackers 
ws.onopen = () => {
    console.log("Connection established");
};

ws.onclose = () => {
    console.log("Connection closed");
};

// receive messages
ws.onmessage = (event) => {
    const messages = document.getElementById("messages");
    const messageData = JSON.parse(event.data);
    const message = document.createElement("div");

    // Define styles depending on the sender
    if (messageData.is_self) {
        message.className = "p-2 my-1 bg-blue-500 text-white rounded-md self-end max-w-xs ml-auto";
    } else {
        message.className = "p-2 my-1 bg-gray-200 text-black rounded-md self-start max-w-xs";
    }

    message.textContent = messageData.text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight; // Auto scroll down
};

// send message
function sendMessage() {
    const input = document.getElementById("messageInput");
    if (input.value.trim()) {
        ws.send(input.value);
        input.value = '';
    }
}
document.getElementById("messageInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") { // sends message by enter
        sendMessage();
    }
});
