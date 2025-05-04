let currentMode = "englishHelp";

document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("jwt_token");

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  initModelSelector();

  console.log("User is logged in, chat interface ready");
});

function initModelSelector() {
  updateSelectedModel(currentMode);

  document.querySelectorAll(".model-option").forEach((option) => {
    option.addEventListener("click", function (e) {
      e.preventDefault();
      const selectedModel = this.getAttribute("data-model");

      if (selectedModel !== currentMode) {
        currentMode = selectedModel;
        updateSelectedModel(currentMode);

        let modelDisplayName = "English Help";
        if (currentMode === "studentHandbook") {
          modelDisplayName = "Student Handbook";
        }
        document.getElementById("currentModelText").textContent =
          modelDisplayName;
      }
    });
  });
}

function updateSelectedModel(modelName) {
  document.querySelectorAll(".selected-icon").forEach((icon) => {
    icon.classList.remove("visible");
  });

  const selectedCheck = document.getElementById(`${modelName}-check`);
  if (selectedCheck) {
    selectedCheck.classList.add("visible");
  }
}

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

    const token = localStorage.getItem("jwt_token");

    let endpoint, requestBody, headers;

    if (currentMode === "englishHelp") {
      endpoint = "http://127.0.0.1:5000/chat";
      requestBody = JSON.stringify({ message: userInput });
      headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
    } else {
      endpoint = "http://127.0.0.1:5000/search";
      requestBody = JSON.stringify({ query: userInput });
      headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      };
    }

    fetch(endpoint, {
      method: "POST",
      headers: headers,
      body: requestBody,
    })
    .then((response) => {
      if (response.status === 401) {
        localStorage.removeItem("jwt_token");
        window.location.href = "login.html";
        throw new Error("Session expired. Please login again.");
      }
    
      // 删除加载动画
      chatBody.removeChild(loadingMessage);
    
      // 初始化 bot 响应块
      var botMessage = document.createElement("div");
      botMessage.classList.add("message", "bot");
      botMessage.textContent = "";
      chatBody.appendChild(botMessage);
    
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
    
      function readStream() {
        reader.read().then(({ done, value }) => {
          if (done) return;
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n").filter((l) => l.startsWith("data: "));
          for (let line of lines) {
            botMessage.textContent += line.slice(6);
          }
          chatBody.scrollTop = chatBody.scrollHeight;
          readStream();
        });
      }
    
      readStream();
    })
    .catch(err => {
      console.error('Error:', err);
    });
    
  }
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function logout() {
  localStorage.removeItem("jwt_token");
  window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", function () {
  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }
});
