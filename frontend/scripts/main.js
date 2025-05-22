let currentMode = "englishHelp";
let currentRequest = null;

document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }
  initModelSelector();
  initUserProfileButton();
  renderChatHistory();
  console.log("User is logged in, chat interface ready");
  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }
  const newChatBtn = document.getElementById("newChatBtn");
  if (newChatBtn) {
    newChatBtn.addEventListener("click", function () {
      if (currentRequest) {
        currentRequest.abort();
        currentRequest = null;
      }
      localStorage.removeItem("chat_history");
      renderChatHistory();
    });
  }
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

        const newChatBtn = document.getElementById("newChatBtn");
        if (newChatBtn) {
          newChatBtn.click();
        }
      }
    });
  });
}

function initUserProfileButton() {
  const userData = JSON.parse(localStorage.getItem("user_data"));
  if (!userData) {
    fetchUserData();
  } else {
    updateUserInitials(userData.name);
  }
}

function fetchUserData() {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    console.error("No token found");
    return;
  }

  fetch("http://127.0.0.1:5000/user/profile", {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  })
    .then((response) => {
      if (response.status === 401) {
        console.error("Session expired");
        return;
      }
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (!data) return;
      return fetch("http://127.0.0.1:5000/user/statistics", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((stats) => {
          const userData = {
            name: data.name,
            email: data.email,
            memberSince: data.memberSince,
            stats: stats,
          };
          localStorage.setItem("user_data", JSON.stringify(userData));
          updateUserInitials(userData.name);
          return userData;
        });
    })
    .catch((err) => {
      console.error("Error fetching user data:", err);
      const placeholderUserData = {
        name: "Student User",
        email: "student@curtin.edu.sg",
        memberSince: "January 2023",
        stats: {
          totalConversations: 0,
          messagesSent: 0,
          totalChatTime: "0 hours",
          avgResponseTime: "0 seconds",
        },
      };
      localStorage.setItem("user_data", JSON.stringify(placeholderUserData));
      updateUserInitials(placeholderUserData.name);
      return placeholderUserData;
    });
}

function updateUserInitials(name) {
  const initialsElement = document.getElementById("userInitialsSmall");
  if (!initialsElement) return;

  const nameParts = name.split(" ");
  let initials = "";

  if (nameParts.length >= 2) {
    initials = nameParts[0].charAt(0) + nameParts[1].charAt(0);
  } else {
    initials = nameParts[0].charAt(0);
  }

  initialsElement.textContent = initials.toUpperCase();
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
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    var loginMessage = document.createElement("div");
    loginMessage.classList.add("message", "bot", "new-message");
    loginMessage.textContent =
      "Please login to send messages. Click the user icon in the bottom left to login.";
    chatBody.appendChild(loginMessage);
    chatBody.scrollTop = chatBody.scrollHeight;
    return;
  }

  if (input.value.trim() !== "") {
    if (welcomeWords) {
      welcomeWords.style.display = "none";
    }

    var userMessage = document.createElement("div");
    userMessage.classList.add("message", "user", "new-message");
    userMessage.textContent = input.value;
    chatBody.appendChild(userMessage);
    saveMessageToHistory("user", input.value);

    var userInput = input.value;

    input.value = "";

    chatBody.scrollTop = chatBody.scrollHeight;

    var loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "bot", "loading");
    loadingMessage.textContent = "";
    chatBody.appendChild(loadingMessage);
    chatBody.scrollTop = chatBody.scrollHeight;

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
    const controller = new AbortController();
    currentRequest = controller;

    fetch(endpoint, {
      method: "POST",
      headers: headers,
      body: requestBody,
      signal: controller.signal,
    })
      .then((response) => {
        if (response.status === 401) {
          if (loadingMessage && loadingMessage.parentNode) {
            chatBody.removeChild(loadingMessage);
          }
          var sessionMessage = document.createElement("div");
          sessionMessage.classList.add("message", "bot", "new-message");
          sessionMessage.textContent =
            "Your session has expired. Please login again by clicking the user icon in the bottom left.";
          chatBody.appendChild(sessionMessage);
          chatBody.scrollTop = chatBody.scrollHeight;
          return;
        }
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        chatBody.removeChild(loadingMessage);
        var botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot", "new-message");
        botMessage.textContent = "";
        chatBody.appendChild(botMessage);

        let botContent = "";
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function readStream() {
          reader.read().then(({ done, value }) => {
            if (done) {
              saveMessageToHistory("bot", botContent);
              updateChatStatistics();
              currentRequest = null;
              return;
            }
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk
              .split("\n")
              .filter((l) => l.startsWith("data: "));
            for (let line of lines) {
              const text = line.slice(6);
              botMessage.textContent += text;
              botContent += text;
            }
            chatBody.scrollTop = chatBody.scrollHeight;
            readStream();
          });
        }

        readStream();
      })
      .catch((err) => {
        if (err.name === "AbortError") {
          if (loadingMessage && loadingMessage.parentNode) {
            chatBody.removeChild(loadingMessage);
          }
          return;
        }
        console.error("Error:", err);
        if (loadingMessage && loadingMessage.parentNode) {
          chatBody.removeChild(loadingMessage);
        }
        var errorMessage = document.createElement("div");
        errorMessage.classList.add("message", "bot", "new-message");
        errorMessage.textContent =
          "Sorry, there was an error processing your request. Please try again.";
        chatBody.appendChild(errorMessage);
      })
      .finally(() => {
        currentRequest = null;
      });
  }
}

function updateChatStatistics() {
  const userData = JSON.parse(localStorage.getItem("user_data"));
  if (!userData) return;
  userData.stats.messagesSent += 1;
  localStorage.setItem("user_data", JSON.stringify(userData));
}

function resetAnimation(element) {
  element.style.animation = "none";
  element.offsetHeight;
  element.style.animation = null;
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

function renderChatHistory() {
  const chatBody = document.getElementById("chatBody");
  const welcomeWords = document.getElementById("wel");
  const chatHistory = JSON.parse(localStorage.getItem("chat_history")) || [];
  const messages = chatBody.querySelectorAll(".message");
  messages.forEach((message) => {
    chatBody.removeChild(message);
  });
  chatHistory.forEach((msg) => {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", msg.role, "new-message");
    messageDiv.textContent = msg.content;
    chatBody.appendChild(messageDiv);
  });
  const hasMessages = chatBody.querySelector(".message") !== null;
  if (welcomeWords) {
    welcomeWords.style.display = hasMessages ? "none" : "block";
  }
}

function saveMessageToHistory(role, content) {
  let history = [];
  try {
    history = JSON.parse(localStorage.getItem("chat_history")) || [];
  } catch (e) {
    history = [];
  }
  history.push({ role, content });
  if (history.length > 100) history = history.slice(history.length - 100);
  localStorage.setItem("chat_history", JSON.stringify(history));
}
