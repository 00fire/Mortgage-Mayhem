// Example: Prevent default form submission for demo
document.querySelector('form').addEventListener('submit', e => {
    e.preventDefault();
    alert('Logged in! (Demo)');
  });
  