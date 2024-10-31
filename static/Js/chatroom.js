// chatroom.js

// Replace with actual room ID and user name
const wsUrl = `ws://localhost:8000/ws/chats/${roomId}/`;  // WebSocket endpoint URL
const socket = new WebSocket(wsUrl);

// WebSocket event listeners
socket.onopen = function() {
  console.log('Connected to WebSocket');
};

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  if (data.type === 'chat_message') {
    addMessageToChat(data.username, data.message);
  }
};

socket.onclose = function() {
  console.log('WebSocket closed');
};



// Send message through WebSocket
function sendMessage() {
  const input = document.getElementById('message-input');
  const message = input.value.trim();
  if (message) {
    socket.send(JSON.stringify({
      'type': 'chat_message',
      'message': message,
      'username': currentUser,  // Current user sending the message
      'room': roomId            // Room ID to specify chat room
    }));
    
    input.value = '';
  }
}


// Add message to chat room
function addMessageToChat(sender, message) {
  const messagesDiv = document.getElementById('messages');
  const messageEl = document.createElement('div');
  messageEl.classList.add('message');
  messageEl.innerHTML = `<strong>${sender}:</strong> ${message}`;
  messagesDiv.appendChild(messageEl);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;  // Auto-scroll to the bottom
}