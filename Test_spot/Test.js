const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");
const searchInput = document.getElementById("searchInput");
const filterToggle = document.getElementById("filterToggle");
const filterModal = document.getElementById("filterModal");
const closeFilter = document.getElementById("closeFilter");
const rangeSlider = document.getElementById("rangeSlider");
const rangeValue = document.getElementById("rangeValue");

// Toggle nav
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});

// Search filter
searchInput.addEventListener("keyup", () => {
  const filter = searchInput.value.toLowerCase();
  const items = navLinks.getElementsByTagName("li");

  for (let i = 0; i < items.length; i++) {
    const link = items[i].querySelector("a");
    const text = link.textContent.toLowerCase();
    items[i].style.display = text.includes(filter) ? "" : "none";
  }
});

// Filter modal toggle
filterToggle.addEventListener("click", () => {
  filterModal.style.display = filterModal.style.display === "block" ? "none" : "block";
});

closeFilter.addEventListener("click", () => {
  filterModal.style.display = "none";
});

// Range slider label
rangeSlider.addEventListener("input", () => {
  rangeValue.textContent = rangeSlider.value;
});
