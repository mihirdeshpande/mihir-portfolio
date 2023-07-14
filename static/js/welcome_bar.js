const messages = ["Welcome!", "Thank you for visiting my website!"];
const characterDelay = 0.1; // Delay between each character in seconds
const messageDelay = 3;
let messageIndex = 0;
let charIndex = 0;

function displayMessages() {
  const div = document.getElementById("welcome-div");

  function typeMessage() {
    const message = messages[messageIndex];
    const displayedText = message.substring(0, charIndex + 1);
    div.textContent = displayedText;

    if (charIndex < message.length) {
      charIndex++;
      setTimeout(typeMessage, characterDelay * 1000);
    } else {
      charIndex = 0;
      messageIndex = (messageIndex + 1) % messages.length;
      setTimeout(displayMessages, messageDelay * 1000);
    }
  }

  typeMessage();
}

// Call the function to start displaying messages with typing effect
displayMessages();
