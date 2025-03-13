function sendMessage() {
  var input = document.getElementById("messageInput");
  var chatBody = document.getElementById("chatBody");
  var welcomeWords = document.getElementById("wel");

  if (input.value.trim() !== "") {
    if (welcomeWords) {
      welcomeWords.style.display = "none";
    }

    var userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");
    userMessage.textContent = input.value;
    chatBody.appendChild(userMessage);

    var userInput = input.value;

    input.value = "";

    chatBody.scrollTop = chatBody.scrollHeight;

    var loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "bot", "loading");
    loadingMessage.textContent = "...";
    chatBody.appendChild(loadingMessage);

    fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput }),
    })
      .then((response) => response.json())
      .then((data) => {
        chatBody.removeChild(loadingMessage);

        var botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");
        botMessage.textContent = data.response;
        chatBody.appendChild(botMessage);

        chatBody.scrollTop = chatBody.scrollHeight;
      })
      .catch((error) => {
        chatBody.removeChild(loadingMessage);

        var errorMessage = document.createElement("div");
        errorMessage.classList.add("message", "bot");
        errorMessage.textContent =
          "Sorry, I couldn't process your request. Please try again.";
        chatBody.appendChild(errorMessage);

        console.error("Error:", error);
      });
  }
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}
