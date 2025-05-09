// Load header
fetch('../components/header.html')  // Fixed the folder name to "components"
.then(res => res.text())
.then(data => {
  document.getElementById('header').innerHTML = data;
});

// Load footer
fetch('../components/footer.html')  // Fixed the folder name to "components"
.then(res => res.text())
.then(data => {
  document.getElementById('footer').innerHTML = data;
});
