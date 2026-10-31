// Guardian info hover
const gIcon = document.getElementById("guardianInfoIcon");
const gBox = document.getElementById("guardianInfoBox");

gIcon.addEventListener("mouseenter", () => gBox.style.display = "block");
gIcon.addEventListener("mouseleave", () => gBox.style.display = "none");

// Personal info hover
const pIcon = document.getElementById("personalInfoIcon");
const pBox = document.getElementById("personalInfoBox");

pIcon.addEventListener("mouseenter", () => pBox.style.display = "block");
pIcon.addEventListener("mouseleave", () => pBox.style.display = "none");