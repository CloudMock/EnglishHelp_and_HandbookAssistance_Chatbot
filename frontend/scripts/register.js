// register.js - 注册页面脚本

document.addEventListener("DOMContentLoaded", function () {
  // 获取注册表单元素
  const signUpButton = document.querySelector(".sign-in-btn");

  // 添加点击事件监听器
  signUpButton.addEventListener("click", function (event) {
    event.preventDefault(); // 阻止表单默认提交行为

    // 获取表单输入值
    const fullName = document.getElementById("fullName").value.trim();
    const studentId = document.getElementById("studentId").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // 简单验证
    if (!fullName || !studentId || !email || !password || !confirmPassword) {
      alert("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    // 构建要发送到API的数据
    const registrationData = {
      Curtin_ID: parseInt(studentId), // 确保ID是整数
      Password: password,
      Student_name: fullName,
      Student_email: email,
    };

    // 发送注册请求到后端API
    fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registrationData),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.error || "Registration failed");
          });
        }
        return response.json();
      })
      .then((data) => {
        alert("Registration successful! Please log in.");
        window.location.href = "login.html";
      })
      .catch((error) => {
        alert("Registration error: " + error.message);
        console.error("Registration error:", error);
      });
  });
});
