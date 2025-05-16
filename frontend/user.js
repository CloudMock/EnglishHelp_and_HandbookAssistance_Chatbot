document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }
  loadUserProfile();
  setupEventListeners();
});

function loadUserProfile() {
  showLoadingState();
  fetchUserProfileFromServer();
}

function showLoadingState() {
  const elements = ["userName", "userEmail", "totalConversations"];
  elements.forEach((id) => {
    const element = document.getElementById(id);
    if (element) {
      element.innerHTML = '<div class="loading-placeholder"></div>';
    }
  });
}

function hideLoadingState() {
  const placeholders = document.querySelectorAll(".loading-placeholder");
  placeholders.forEach((placeholder) => placeholder.remove());
}

function fetchUserProfileFromServer() {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  fetch("http://127.0.0.1:5000/user/profile", {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.status === 401) {
        localStorage.removeItem("jwt_token");
        window.location.href = "login.html";
        throw new Error("Session expire, please login.");
      }
      if (!response.ok) {
        throw new Error(`httpError: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      updateUserInfo(data);
      hideLoadingState();
      localStorage.setItem("user_data", JSON.stringify(data));
    })
    .catch((err) => {
      console.error("No user data:", err);
      hideLoadingState();
      document.getElementById("userName").textContent = "Error loading profile";
      document.getElementById("userEmail").textContent =
        "Please try again later";
      document.getElementById("totalConversations").textContent = "0";
    });
}

function updateUserInfo(userData) {
  document.getElementById("userName").textContent = userData.name || "";
  document.getElementById("userEmail").textContent = userData.email || "";
  document.getElementById("totalConversations").textContent =
    userData.total_conversations || 0;

  if (userData.avatar_url) {
    const avatarImage = document.getElementById("avatarImage");
    avatarImage.src = userData.avatar_url;
    avatarImage.style.display = "block";
    document.getElementById("userInitials").style.display = "none";
  } else {
    const nameParts = (userData.name || "").split(" ");
    let initials = "";
    if (nameParts.length >= 2) {
      initials = nameParts[0].charAt(0) + nameParts[1].charAt(0);
    } else if (nameParts[0]) {
      initials = nameParts[0].charAt(0);
    }
    document.getElementById("userInitials").textContent =
      initials.toUpperCase();
    document.getElementById("userInitials").style.display = "flex";
    document.getElementById("avatarImage").style.display = "none";
  }
}

function setupEventListeners() {
  const logoutButton = document.getElementById("logoutButton");
  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      localStorage.removeItem("jwt_token");
      localStorage.removeItem("user_data");
      localStorage.removeItem("chat_history");
      window.location.href = "login.html";
    });
  }
}

function showAlert(message, type = "info") {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  alertDiv.style.top = "20px";
  alertDiv.style.right = "20px";
  alertDiv.style.zIndex = "9999";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  document.body.appendChild(alertDiv);
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.parentNode.removeChild(alertDiv);
    }
  }, 3000);
}
