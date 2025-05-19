function toggleChatbot() {
  const chatbotWindow = document.getElementById('chatbot-window');
  chatbotWindow.style.display = chatbotWindow.style.display === 'flex' ? 'none' : 'flex';
}

function sendChatbotMessage() {
  const input = document.getElementById('chatbot-input');
  const messages = document.getElementById('chatbot-messages');

  if (input.value.trim() === '') return;

  // Add user message
  const userMessage = document.createElement('div');
  userMessage.className = 'message user';
  userMessage.textContent = input.value;
  messages.appendChild(userMessage);

  // Simulate bot response
  const botMessage = document.createElement('div');
  botMessage.className = 'message bot';
  botMessage.textContent = "Thanks for your message! I'll get back to you soon.";
  messages.appendChild(botMessage);

  // Clear input field
  input.value = '';

  // Scroll to the latest message
  messages.scrollTop = messages.scrollHeight;
}
