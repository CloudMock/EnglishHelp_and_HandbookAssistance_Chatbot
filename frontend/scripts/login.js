document.addEventListener("DOMContentLoaded", function () {
  const signInButton = document.querySelector(".sign-in-btn");
  signInButton.addEventListener("click", function (event) {
    event.preventDefault();

    const userInput = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!userInput || !password) {
      alert("Please enter your Student ID/Email and password");
      return;
    }

    const loginData = {
      Curtin_ID: parseInt(userInput),
      Password: password,
    };

    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.error || "Login failed");
          });
        }
        return response.json();
      })
      .then((data) => {
        localStorage.setItem("jwt_token", data.token);
        alert("Login successful!");
        window.location.href = "index.html";
      })
      .catch((error) => {
        alert("Login error: " + error.message);
        console.error("Login error:", error);
      });
  });
});
