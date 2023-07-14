const messages = ["Welcome", "Thank you for visiting my website!"];
const opacities = [0.8, 0.5]
const delayInSeconds = 10; // Number of seconds to display each message


function displayMessages() {
  const div = document.getElementById("welcome-div");
  let index = 0;

  function showMessage() {
    div.style.opacity = opacities[index];
    div.textContent = messages[index];
    index = (index + 1) % messages.length;
    setTimeout(showMessage, delayInSeconds * 1000);
  }

  // Initial call to start the loop
  showMessage();
}

// Call the function to start displaying messages in a loop
displayMessages();
