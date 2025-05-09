document.addEventListener('DOMContentLoaded', function () {
    const password = document.querySelector('input[type="password"]:nth-of-type(1)');
    const confirm = document.querySelector('input[type="password"]:nth-of-type(2)');
  
    confirm.addEventListener('blur', () => {
      if (password.value !== confirm.value) {
        confirm.setCustomValidity("Passwords do not match.");
      } else {
        confirm.setCustomValidity("");  // Clear the custom validity message if the passwords match
      }

      // Trigger the form validation
      confirm.checkValidity();
    });

    // Optionally, you can prevent form submission if passwords don't match
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();  // Prevent form submission if invalid
      }
    });
});

  