 // Load header
fetch('../components/header.html')
.then(res => res.text())
.then(data => {
  document.getElementById('header').innerHTML = data;
});

// Load footer
fetch('../components/footer.html')
.then(res => res.text())
.then(data => {
  document.getElementById('footer').innerHTML = data;
});
