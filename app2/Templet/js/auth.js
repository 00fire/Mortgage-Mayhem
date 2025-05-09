// Example: Simple password match checker on blur (can enhance UX)
document.addEventListener('DOMContentLoaded', function () {
    const password = document.querySelector('input[type="password"]:nth-of-type(1)');
    const confirm = document.querySelector('input[type="password"]:nth-of-type(2)');
  
    confirm.addEventListener('blur', () => {
      if (password.value !== confirm.value) {
        confirm.setCustomValidity("Passwords do not match.");
      } else {
        confirm.setCustomValidity("");
      }
    });
  });
  