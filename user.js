document.addEventListener('DOMContentLoaded', () => {
    const studentName = "Student Name"; 
    const totalConversations = 114;
    const totalUsageDays = 51;
  
    document.getElementById('student-name').textContent = studentName;
    document.getElementById('conversation-count').textContent = totalConversations;
    document.getElementById('usage-days').textContent = totalUsageDays;
  
    const avatarImg = document.getElementById('avatar-img');
    const avatarUpload = document.getElementById('avatar-upload');
  
    avatarImg.addEventListener('click', () => {
      avatarUpload.click();
    });
  
    avatarUpload.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          avatarImg.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  
    avatarImg.onerror = function() {
      avatarImg.src = 'https://via.placeholder.com/100';
    };
  });
  
  